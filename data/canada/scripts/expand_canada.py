#!/usr/bin/env python3
"""
Expand the Canadian dataset with additional universities and colleges.

Adds missing Canadian institutions not already in data/canada.json.
Data sourced from Universities Canada directory and provincial lists.

Usage:
    python scripts/expand_canada.py
"""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent  # data/

# Additional Canadian institutions not in the initial dataset
ADDITIONAL_CANADA = [
    # Ontario
    {"name": "University of Toronto Mississauga", "country": "Canada", "state": "Ontario", "city": "Mississauga", "domain": "utm.utoronto.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Toronto Scarborough", "country": "Canada", "state": "Ontario", "city": "Scarborough", "domain": "utsc.utoronto.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Seneca College", "country": "Canada", "state": "Ontario", "city": "Toronto", "domain": "senecapolytechnic.ca", "aliases": ["senecacollege.ca"], "type": "College", "control": "Public"},
    {"name": "George Brown College", "country": "Canada", "state": "Ontario", "city": "Toronto", "domain": "georgebrown.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Humber College", "country": "Canada", "state": "Ontario", "city": "Toronto", "domain": "humber.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Centennial College", "country": "Canada", "state": "Ontario", "city": "Toronto", "domain": "centennialcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Sheridan College", "country": "Canada", "state": "Ontario", "city": "Oakville", "domain": "sheridancollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Conestoga College", "country": "Canada", "state": "Ontario", "city": "Kitchener", "domain": "conestogac.on.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Fanshawe College", "country": "Canada", "state": "Ontario", "city": "London", "domain": "fanshawec.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Mohawk College", "country": "Canada", "state": "Ontario", "city": "Hamilton", "domain": "mohawkcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Durham College", "country": "Canada", "state": "Ontario", "city": "Oshawa", "domain": "durhamcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Algonquin College", "country": "Canada", "state": "Ontario", "city": "Ottawa", "domain": "algonquincollege.com", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Niagara College", "country": "Canada", "state": "Ontario", "city": "Welland", "domain": "niagaracollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Georgian College", "country": "Canada", "state": "Ontario", "city": "Barrie", "domain": "georgiancollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Lambton College", "country": "Canada", "state": "Ontario", "city": "Sarnia", "domain": "lambtoncollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Cambrian College", "country": "Canada", "state": "Ontario", "city": "Sudbury", "domain": "cambriancollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Canadore College", "country": "Canada", "state": "Ontario", "city": "North Bay", "domain": "canadorecollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Confederation College", "country": "Canada", "state": "Ontario", "city": "Thunder Bay", "domain": "confederationcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Loyalist College", "country": "Canada", "state": "Ontario", "city": "Belleville", "domain": "loyalistcollege.com", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Fleming College", "country": "Canada", "state": "Ontario", "city": "Peterborough", "domain": "flemingcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "St. Lawrence College", "country": "Canada", "state": "Ontario", "city": "Kingston", "domain": "stlawrencecollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Sault College", "country": "Canada", "state": "Ontario", "city": "Sault Ste. Marie", "domain": "saultcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Northern College", "country": "Canada", "state": "Ontario", "city": "Timmins", "domain": "northernc.on.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Boreal College", "country": "Canada", "state": "Ontario", "city": "Sudbury", "domain": "collegeboreal.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "La Cite College", "country": "Canada", "state": "Ontario", "city": "Ottawa", "domain": "collegelacite.ca", "aliases": [], "type": "College", "control": "Public"},

    # British Columbia
    {"name": "British Columbia Institute of Technology", "country": "Canada", "state": "British Columbia", "city": "Burnaby", "domain": "bcit.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Douglas College", "country": "Canada", "state": "British Columbia", "city": "New Westminster", "domain": "douglascollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Langara College", "country": "Canada", "state": "British Columbia", "city": "Vancouver", "domain": "langara.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Capilano University", "country": "Canada", "state": "British Columbia", "city": "North Vancouver", "domain": "capilanou.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Camosun College", "country": "Canada", "state": "British Columbia", "city": "Victoria", "domain": "camosun.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Okanagan College", "country": "Canada", "state": "British Columbia", "city": "Kelowna", "domain": "okanagan.bc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "College of New Caledonia", "country": "Canada", "state": "British Columbia", "city": "Prince George", "domain": "cnc.bc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "North Island College", "country": "Canada", "state": "British Columbia", "city": "Courtenay", "domain": "nic.bc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Selkirk College", "country": "Canada", "state": "British Columbia", "city": "Castlegar", "domain": "selkirk.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "College of the Rockies", "country": "Canada", "state": "British Columbia", "city": "Cranbrook", "domain": "cotr.bc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Northern Lights College", "country": "Canada", "state": "British Columbia", "city": "Dawson Creek", "domain": "nlc.bc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Coast Mountain College", "country": "Canada", "state": "British Columbia", "city": "Terrace", "domain": "coastmountaincollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Justice Institute of British Columbia", "country": "Canada", "state": "British Columbia", "city": "New Westminster", "domain": "jibc.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Nicola Valley Institute of Technology", "country": "Canada", "state": "British Columbia", "city": "Merritt", "domain": "nvit.ca", "aliases": [], "type": "Institute", "control": "Public"},

    # Alberta
    {"name": "NAIT", "country": "Canada", "state": "Alberta", "city": "Edmonton", "domain": "nait.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "SAIT", "country": "Canada", "state": "Alberta", "city": "Calgary", "domain": "sait.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "NorQuest College", "country": "Canada", "state": "Alberta", "city": "Edmonton", "domain": "norquest.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Red Deer Polytechnic", "country": "Canada", "state": "Alberta", "city": "Red Deer", "domain": "rdpolytech.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Lethbridge College", "country": "Canada", "state": "Alberta", "city": "Lethbridge", "domain": "lethbridgecollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Medicine Hat College", "country": "Canada", "state": "Alberta", "city": "Medicine Hat", "domain": "mhc.ab.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Lakeland College", "country": "Canada", "state": "Alberta", "city": "Vermilion", "domain": "lakelandcollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Grande Prairie Regional College", "country": "Canada", "state": "Alberta", "city": "Grande Prairie", "domain": "gprc.ab.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Bow Valley College", "country": "Canada", "state": "Alberta", "city": "Calgary", "domain": "bowvalleycollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Concordia University of Edmonton", "country": "Canada", "state": "Alberta", "city": "Edmonton", "domain": "concordia.ab.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "King's University", "country": "Canada", "state": "Alberta", "city": "Edmonton", "domain": "kingsu.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Ambrose University", "country": "Canada", "state": "Alberta", "city": "Calgary", "domain": "ambrose.edu", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Burman University", "country": "Canada", "state": "Alberta", "city": "Lacombe", "domain": "burmanu.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "St. Mary's University Calgary", "country": "Canada", "state": "Alberta", "city": "Calgary", "domain": "stmu.ca", "aliases": [], "type": "University", "control": "Private"},

    # Quebec
    {"name": "UQTR", "country": "Canada", "state": "Quebec", "city": "Trois-Rivieres", "domain": "uqtr.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "UQAC", "country": "Canada", "state": "Quebec", "city": "Chicoutimi", "domain": "uqac.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "UQO", "country": "Canada", "state": "Quebec", "city": "Gatineau", "domain": "uqo.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "UQAR", "country": "Canada", "state": "Quebec", "city": "Rimouski", "domain": "uqar.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "UQAT", "country": "Canada", "state": "Quebec", "city": "Rouyn-Noranda", "domain": "uqat.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "ETS Montreal", "country": "Canada", "state": "Quebec", "city": "Montreal", "domain": "etsmtl.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "ENAP", "country": "Canada", "state": "Quebec", "city": "Quebec City", "domain": "enap.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "TELUQ", "country": "Canada", "state": "Quebec", "city": "Quebec City", "domain": "teluq.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Dawson College", "country": "Canada", "state": "Quebec", "city": "Montreal", "domain": "dawsoncollege.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Vanier College", "country": "Canada", "state": "Quebec", "city": "Montreal", "domain": "vaniercollege.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "John Abbott College", "country": "Canada", "state": "Quebec", "city": "Sainte-Anne-de-Bellevue", "domain": "johnabbott.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Marianopolis College", "country": "Canada", "state": "Quebec", "city": "Montreal", "domain": "marianopolis.edu", "aliases": [], "type": "College", "control": "Private"},
    {"name": "Champlain College", "country": "Canada", "state": "Quebec", "city": "Sherbrooke", "domain": "champlaincollege.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Heritage College", "country": "Canada", "state": "Quebec", "city": "Gatineau", "domain": "cegep-heritage.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Cegep de Sainte-Foy", "country": "Canada", "state": "Quebec", "city": "Quebec City", "domain": "cegep-ste-foy.qc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Cegep du Vieux Montreal", "country": "Canada", "state": "Quebec", "city": "Montreal", "domain": "cvm.qc.ca", "aliases": [], "type": "College", "control": "Public"},

    # Manitoba
    {"name": "Red River College Polytechnic", "country": "Canada", "state": "Manitoba", "city": "Winnipeg", "domain": "rrc.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Assiniboine Community College", "country": "Canada", "state": "Manitoba", "city": "Brandon", "domain": "assiniboine.net", "aliases": [], "type": "Community College", "control": "Public"},
    {"name": "University College of the North", "country": "Canada", "state": "Manitoba", "city": "The Pas", "domain": "ucn.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Canadian Mennonite University", "country": "Canada", "state": "Manitoba", "city": "Winnipeg", "domain": "cmu.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Universite de Saint-Boniface", "country": "Canada", "state": "Manitoba", "city": "Winnipeg", "domain": "ustboniface.ca", "aliases": [], "type": "University", "control": "Public"},

    # Saskatchewan
    {"name": "Saskatchewan Polytechnic", "country": "Canada", "state": "Saskatchewan", "city": "Saskatoon", "domain": "saskpolytech.ca", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Campion College", "country": "Canada", "state": "Saskatchewan", "city": "Regina", "domain": "campioncollege.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Luther College", "country": "Canada", "state": "Saskatchewan", "city": "Regina", "domain": "luthercollege.edu", "aliases": [], "type": "College", "control": "Private"},
    {"name": "St. Peter's College", "country": "Canada", "state": "Saskatchewan", "city": "Muenster", "domain": "stpeterscollege.ca", "aliases": [], "type": "College", "control": "Private"},
    {"name": "Gabriel Dumont Institute", "country": "Canada", "state": "Saskatchewan", "city": "Saskatoon", "domain": "gdins.org", "aliases": [], "type": "Institute", "control": "Public"},

    # New Brunswick
    {"name": "New Brunswick Community College", "country": "Canada", "state": "New Brunswick", "city": "Fredericton", "domain": "nbcc.ca", "aliases": [], "type": "Community College", "control": "Public"},
    {"name": "Crandall University", "country": "Canada", "state": "New Brunswick", "city": "Moncton", "domain": "crandallu.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "St. Stephen's University", "country": "Canada", "state": "New Brunswick", "city": "St. Stephen", "domain": "ssu.ca", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Universite de Moncton Edmundston", "country": "Canada", "state": "New Brunswick", "city": "Edmundston", "domain": "umce.ca", "aliases": [], "type": "University", "control": "Public"},

    # Nova Scotia
    {"name": "Nova Scotia Community College", "country": "Canada", "state": "Nova Scotia", "city": "Halifax", "domain": "nscc.ca", "aliases": [], "type": "Community College", "control": "Public"},
    {"name": "NSCAD University", "country": "Canada", "state": "Nova Scotia", "city": "Halifax", "domain": "nscad.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universite Sainte-Anne", "country": "Canada", "state": "Nova Scotia", "city": "Church Point", "domain": "usainteanne.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Atlantic School of Theology", "country": "Canada", "state": "Nova Scotia", "city": "Halifax", "domain": "astheology.ns.ca", "aliases": [], "type": "University", "control": "Private"},

    # Newfoundland and Labrador
    {"name": "College of the North Atlantic", "country": "Canada", "state": "Newfoundland and Labrador", "city": "Stephenville", "domain": "cna.nl.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Marine Institute", "country": "Canada", "state": "Newfoundland and Labrador", "city": "St. John's", "domain": "mi.mun.ca", "aliases": [], "type": "Institute", "control": "Public"},

    # Prince Edward Island
    {"name": "Holland College", "country": "Canada", "state": "Prince Edward Island", "city": "Charlottetown", "domain": "hollandcollege.com", "aliases": [], "type": "College", "control": "Public"},

    # Territories
    {"name": "Yukon University", "country": "Canada", "state": "Yukon", "city": "Whitehorse", "domain": "yukonu.ca", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Aurora College", "country": "Canada", "state": "Northwest Territories", "city": "Yellowknife", "domain": "auroracollege.nt.ca", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Nunavut Arctic College", "country": "Canada", "state": "Nunavut", "city": "Iqaluit", "domain": "arcticcollege.ca", "aliases": [], "type": "College", "control": "Public"},
]


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def main():
    canada_path = DATA_DIR / "canada.json"

    # Load existing
    with open(canada_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_names = {normalize_name(r["name"]) for r in existing}
    existing_domains = {r["domain"].lower() for r in existing}

    added = 0
    for record in ADDITIONAL_CANADA:
        norm = normalize_name(record["name"])
        dom = record["domain"].lower()
        if norm not in existing_names and dom not in existing_domains:
            existing.append(record)
            existing_names.add(norm)
            existing_domains.add(dom)
            added += 1

    existing.sort(key=lambda r: (r["state"], r["name"]))

    with open(canada_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new Canadian institutions")
    print(f"Total: {len(existing)} records")

    # Print by province
    provinces = {}
    for r in existing:
        p = r["state"]
        provinces[p] = provinces.get(p, 0) + 1
    print("\nBy province:")
    for p, c in sorted(provinces.items()):
        print(f"  {p}: {c}")


if __name__ == "__main__":
    main()
