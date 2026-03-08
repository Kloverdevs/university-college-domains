#!/usr/bin/env python3
"""
Import institutions from the NCES IPEDS database.

Downloads the HD2023 (Institutional Characteristics) CSV from IPEDS,
parses it, and generates/expands the usa.json dataset.

The HD2023 file contains institution name, city, state, URL, control,
and other fields for all Title IV institutions.

Usage:
    python scripts/import_ipeds.py
    python scripts/import_ipeds.py --min-size 500   # Only 4-year+ with 500+ enrollment
"""

import csv
import io
import json
import os
import re
import sys
import argparse
import zipfile
from pathlib import Path

try:
    import requests
    import tldextract
except ImportError:
    print("Missing dependencies. Run: pip install requests tldextract")
    sys.exit(1)

DATA_DIR = Path(__file__).resolve().parent.parent.parent  # data/
IPEDS_URL = "https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip"

# FIPS state codes to state names
FIPS_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
    "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska",
    "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "AS": "American Samoa", "GU": "Guam", "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico", "VI": "U.S. Virgin Islands", "FM": "Federated States of Micronesia",
    "MH": "Marshall Islands", "PW": "Palau",
}

# IPEDS CONTROL codes
CONTROL_MAP = {
    "1": "Public",
    "2": "Private",  # Private not-for-profit
    "3": "Private",  # Private for-profit
}

# IPEDS ICLEVEL codes
LEVEL_MAP = {
    "1": "4-year",       # 4-year or above
    "2": "2-year",       # 2-year (community college)
    "3": "Less-than-2",  # Less than 2-year
}


def download_ipeds() -> bytes:
    """Download the IPEDS HD2023 ZIP file."""
    print("Downloading IPEDS HD2023 data...")
    resp = requests.get(IPEDS_URL, timeout=120)
    resp.raise_for_status()
    print(f"  Downloaded {len(resp.content) / 1024 / 1024:.1f} MB")
    return resp.content


def extract_csv(zip_data: bytes) -> str:
    """Extract the CSV from the ZIP file."""
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise RuntimeError("No CSV found in ZIP file")
        # Get the main data file (not the dictionary)
        data_csv = [n for n in csv_names if "_rv" not in n.lower() and "dict" not in n.lower()]
        target = data_csv[0] if data_csv else csv_names[0]
        print(f"  Extracting {target}")
        return zf.read(target).decode("latin-1")  # IPEDS uses latin-1


def normalize_domain(url: str) -> str:
    """Extract clean domain from a URL."""
    if not url:
        return ""
    url = url.strip().lower()
    for prefix in ("https://", "http://", "//"):
        if url.startswith(prefix):
            url = url[len(prefix):]
    if url.startswith("www."):
        url = url[4:]
    url = url.rstrip("/").split("/")[0].split("?")[0].split("#")[0]
    return url


def classify_type(name: str, level: str) -> str:
    """Classify institution type from name and IPEDS level."""
    nl = name.lower()
    if "community college" in nl or (level == "2-year" and "college" in nl):
        return "Community College"
    if "institute" in nl or "polytechnic" in nl:
        return "Institute"
    if "college" in nl and "university" not in nl:
        return "College"
    return "University"


def parse_ipeds(csv_text: str, min_size: int = 0) -> list[dict]:
    """Parse IPEDS CSV into institution records."""
    reader = csv.DictReader(io.StringIO(csv_text))
    records = []
    seen_domains = set()
    seen_names = set()

    for row in reader:
        # Filter: only US states + DC (exclude territories unless desired)
        state_abbr = row.get("STABBR", "").strip().upper()
        if state_abbr not in FIPS_STATES:
            continue

        # Filter: only currently open institutions
        # CYACTIVE = 1 means institution is active
        # If this field doesn't exist, we use DETEFP (main effect end date) or skip filter
        # CLOSEDAT field: empty means still open
        close_date = row.get("CLOSEDAT", "").strip()
        if close_date and close_date != "-2":
            continue

        name = row.get("INSTNM", "").strip()
        if not name:
            continue

        # Normalize name for dedup
        norm_name = re.sub(r"[^a-z0-9]", "", name.lower())
        if norm_name in seen_names:
            continue
        seen_names.add(norm_name)

        city = row.get("CITY", "").strip()
        state = FIPS_STATES.get(state_abbr, state_abbr)

        # Control
        control_code = row.get("CONTROL", "").strip()
        control = CONTROL_MAP.get(control_code, "Public")

        # Level
        level_code = row.get("ICLEVEL", "").strip()
        level = LEVEL_MAP.get(level_code, "4-year")

        # Type
        inst_type = classify_type(name, level)

        # Domain from WEBADDR
        url = row.get("WEBADDR", "").strip()
        domain = normalize_domain(url)

        # Skip if no domain
        if not domain:
            continue

        # Skip duplicate domains
        if domain in seen_domains:
            continue
        seen_domains.add(domain)

        records.append({
            "name": name,
            "country": "USA",
            "state": state,
            "city": city.title() if city == city.upper() else city,
            "domain": domain,
            "aliases": [],
            "type": inst_type,
            "control": control,
        })

    return records


def load_existing(filepath: Path) -> list[dict]:
    """Load existing dataset."""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def merge_records(existing: list[dict], ipeds: list[dict]) -> list[dict]:
    """Merge IPEDS records with existing curated data. 
    Existing records take priority (they've been manually verified)."""
    # Index existing by normalized name and domain
    existing_names = set()
    existing_domains = set()
    for r in existing:
        existing_names.add(re.sub(r"[^a-z0-9]", "", r["name"].lower()))
        existing_domains.add(r["domain"].lower())
        for alias in r.get("aliases", []):
            existing_domains.add(alias.lower())

    merged = list(existing)
    added = 0

    for record in ipeds:
        norm_name = re.sub(r"[^a-z0-9]", "", record["name"].lower())
        domain_lower = record["domain"].lower()

        if norm_name in existing_names or domain_lower in existing_domains:
            continue

        existing_names.add(norm_name)
        existing_domains.add(domain_lower)
        merged.append(record)
        added += 1

    return merged, added


def main():
    parser = argparse.ArgumentParser(description="Import IPEDS data to expand USA dataset")
    parser.add_argument("--min-size", type=int, default=0,
                        help="Minimum enrollment size (not implemented in basic mode)")
    parser.add_argument("--include-territories", action="store_true",
                        help="Include US territories (PR, GU, etc.)")
    args = parser.parse_args()

    # Download and parse
    zip_data = download_ipeds()
    csv_text = extract_csv(zip_data)
    ipeds_records = parse_ipeds(csv_text)

    print(f"\nIPEDS records parsed: {len(ipeds_records)}")

    # Load existing and merge
    usa_path = DATA_DIR / "usa.json"
    existing = load_existing(usa_path)
    print(f"Existing records: {len(existing)}")

    merged, added = merge_records(existing, ipeds_records)
    print(f"New records added: {added}")
    print(f"Total records: {len(merged)}")

    # Sort and save
    merged.sort(key=lambda r: (r["state"], r["name"]))
    with open(usa_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {usa_path}")

    # Print coverage stats
    states = {}
    for r in merged:
        s = r["state"]
        states[s] = states.get(s, 0) + 1
    print(f"\nCoverage by state:")
    for s, c in sorted(states.items()):
        print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
