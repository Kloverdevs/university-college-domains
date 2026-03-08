#!/usr/bin/env python3
"""
Full re-import from IPEDS with relaxed dedup to maximize coverage,
then restructure into country/universities.json and country/colleges.json.

Key change: allows multiple institutions to share the same domain
(branch campuses, system offices, etc.)

Usage:
    python scripts/full_reimport.py
"""

import csv
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing: pip install requests")
    sys.exit(1)

DATA_DIR = Path(__file__).resolve().parent.parent.parent  # data/
IPEDS_URL = "https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip"

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
    "PR": "Puerto Rico", "VI": "U.S. Virgin Islands",
    "FM": "Federated States of Micronesia", "MH": "Marshall Islands", "PW": "Palau",
}

CONTROL_MAP = {"1": "Public", "2": "Private", "3": "Private"}


def download_ipeds() -> str:
    print("Downloading IPEDS HD2023...")
    resp = requests.get(IPEDS_URL, timeout=120)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        data_csv = [n for n in csv_names if "dict" not in n.lower() and "_rv" not in n.lower()]
        target = data_csv[0] if data_csv else csv_names[0]
        print(f"  Extracted {target}")
        return zf.read(target).decode("latin-1")


def normalize_domain(url):
    if not url:
        return ""
    url = url.strip().lower()
    for p in ("https://", "http://", "//"):
        if url.startswith(p):
            url = url[len(p):]
    if url.startswith("www."):
        url = url[4:]
    url = url.rstrip("/").split("/")[0].split("?")[0].split("#")[0].rstrip(".")
    return url


def is_valid_domain(domain):
    if not domain or domain in ("https", "http", "-"):
        return False
    if "." not in domain:
        return False
    if ".k12." in domain:
        return False
    if domain.count(".") > 3:
        return False
    return True


def classify_type(name, level_code):
    nl = name.lower()
    is_2year = level_code in ("2", "3")
    if "community college" in nl:
        return "Community College"
    if is_2year and ("college" in nl or "community" in nl):
        return "Community College"
    if "institute" in nl or "polytechnic" in nl:
        return "Institute"
    if "college" in nl and "university" not in nl:
        return "College"
    return "University"


def parse_ipeds_full(csv_text):
    """Parse IPEDS with dedup by name+state (NOT by domain).
    Allows branch campuses sharing the same domain."""
    reader = csv.DictReader(io.StringIO(csv_text))
    records = []
    seen_keys = set()

    for row in reader:
        state_abbr = row.get("STABBR", "").strip().upper()
        if state_abbr not in FIPS_STATES:
            continue

        close_date = row.get("CLOSEDAT", "").strip()
        if close_date and close_date != "-2":
            continue

        name = row.get("INSTNM", "").strip()
        if not name:
            continue

        # Dedup by name + state so same-name branches in different states are kept
        norm_name = re.sub(r"[^a-z0-9]", "", name.lower())
        dedup_key = f"{norm_name}|{state_abbr}"
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)

        url = row.get("WEBADDR", "").strip()
        domain = normalize_domain(url)
        if not is_valid_domain(domain):
            continue

        city = row.get("CITY", "").strip()
        state = FIPS_STATES.get(state_abbr, state_abbr)
        control = CONTROL_MAP.get(row.get("CONTROL", "").strip(), "Public")
        level_code = row.get("ICLEVEL", "").strip()
        inst_type = classify_type(name, level_code)

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


def load_json(filepath):
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json(records, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    records.sort(key=lambda r: (r.get("state", ""), r.get("name", "")))
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def merge_by_name_state(base, additions):
    """Merge using name+state as key so same-name branches stay."""
    keys = set()
    for r in base:
        n = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        keys.add(f"{n}|{r.get('state', '')}")
    merged = list(base)
    for r in additions:
        n = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        k = f"{n}|{r.get('state', '')}"
        if k not in keys:
            keys.add(k)
            merged.append(r)
    return merged


def main():
    # ── USA from IPEDS ──
    csv_text = download_ipeds()
    ipeds_records = parse_ipeds_full(csv_text)
    print(f"IPEDS records (name-dedup only): {len(ipeds_records)}")

    # Load old flat files for any curated data 
    old_usa_flat = load_json(DATA_DIR / "usa.json")
    old_usa_uni = load_json(DATA_DIR / "usa" / "universities.json")
    old_usa_col = load_json(DATA_DIR / "usa" / "colleges.json")
    existing_usa = old_usa_flat + old_usa_uni + old_usa_col

    # Deduplicate existing by name+state
    seen = set()
    deduped_existing = []
    for r in existing_usa:
        n = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        k = f"{n}|{r.get('state', '')}"
        if k not in seen:
            seen.add(k)
            deduped_existing.append(r)
    print(f"Existing curated USA (deduped): {len(deduped_existing)}")

    # Merge: curated takes priority
    merged = merge_by_name_state(deduped_existing, ipeds_records)
    print(f"Merged USA total: {len(merged)}")

    # Split
    universities = [r for r in merged if r["type"] == "University"]
    colleges = [r for r in merged if r["type"] != "University"]

    save_json(universities, DATA_DIR / "usa" / "universities.json")
    save_json(colleges, DATA_DIR / "usa" / "colleges.json")

    # ── Canada (just split existing) ──
    old_canada_flat = load_json(DATA_DIR / "canada.json")
    old_canada_uni = load_json(DATA_DIR / "canada" / "universities.json")
    old_canada_col = load_json(DATA_DIR / "canada" / "colleges.json")
    existing_canada = old_canada_flat + old_canada_uni + old_canada_col

    seen_ca = set()
    deduped_canada = []
    for r in existing_canada:
        n = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        if n not in seen_ca:
            seen_ca.add(n)
            deduped_canada.append(r)

    ca_universities = [r for r in deduped_canada if r["type"] == "University"]
    ca_colleges = [r for r in deduped_canada if r["type"] != "University"]

    save_json(ca_universities, DATA_DIR / "canada" / "universities.json")
    save_json(ca_colleges, DATA_DIR / "canada" / "colleges.json")

    # ── Report ──
    total_usa = len(universities) + len(colleges)
    total_canada = len(ca_universities) + len(ca_colleges)
    ipeds_universe = 6086  # open US institutions in IPEDS

    print(f"\n{'='*60}")
    print(f"COVERAGE REPORT")
    print(f"{'='*60}")
    print(f"USA: {total_usa} / {ipeds_universe} = {total_usa*100/ipeds_universe:.1f}%")
    print(f"  Universities: {len(universities)}")
    print(f"  Colleges:     {len(colleges)}")
    print(f"Canada: {total_canada}")
    print(f"  Universities: {len(ca_universities)}")
    print(f"  Colleges:     {len(ca_colleges)}")
    print(f"{'='*60}")
    print(f"GRAND TOTAL: {total_usa + total_canada}")

    if total_usa * 100 / ipeds_universe >= 95:
        print(f"\n✅ USA coverage is ≥95%!")
    else:
        gap = int(ipeds_universe * 0.95) - total_usa
        print(f"\n⚠ USA needs {gap} more records for 95%")


if __name__ == "__main__":
    main()
