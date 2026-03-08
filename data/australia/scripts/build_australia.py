#!/usr/bin/env python3
"""Build the Australian university and college dataset."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent

AU_UNIVERSITIES = [
    # Group of Eight (Go8)
    {"name": "Australian National University", "country": "Australia", "state": "ACT", "city": "Canberra", "domain": "anu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Melbourne", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "unimelb.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Sydney", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "sydney.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Queensland", "country": "Australia", "state": "Queensland", "city": "Brisbane", "domain": "uq.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of New South Wales", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "unsw.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Monash University", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "monash.edu", "aliases": ["monash.edu.au"], "type": "University", "control": "Public"},
    {"name": "University of Western Australia", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "uwa.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Adelaide", "country": "Australia", "state": "South Australia", "city": "Adelaide", "domain": "adelaide.edu.au", "aliases": [], "type": "University", "control": "Public"},
    # Australian Technology Network (ATN)
    {"name": "Curtin University", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "curtin.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Deakin University", "country": "Australia", "state": "Victoria", "city": "Geelong", "domain": "deakin.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "RMIT University", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "rmit.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of South Australia", "country": "Australia", "state": "South Australia", "city": "Adelaide", "domain": "unisa.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Technology Sydney", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "uts.edu.au", "aliases": [], "type": "University", "control": "Public"},
    # Innovative Research Universities (IRU)
    {"name": "Charles Darwin University", "country": "Australia", "state": "Northern Territory", "city": "Darwin", "domain": "cdu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Flinders University", "country": "Australia", "state": "South Australia", "city": "Adelaide", "domain": "flinders.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Griffith University", "country": "Australia", "state": "Queensland", "city": "Brisbane", "domain": "griffith.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "James Cook University", "country": "Australia", "state": "Queensland", "city": "Townsville", "domain": "jcu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "La Trobe University", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "latrobe.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Murdoch University", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "murdoch.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Western Sydney University", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "westernsydney.edu.au", "aliases": [], "type": "University", "control": "Public"},
    # Regional Universities Network (RUN)
    {"name": "CQUniversity", "country": "Australia", "state": "Queensland", "city": "Rockhampton", "domain": "cqu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Federation University Australia", "country": "Australia", "state": "Victoria", "city": "Ballarat", "domain": "federation.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Southern Cross University", "country": "Australia", "state": "New South Wales", "city": "Lismore", "domain": "scu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of New England", "country": "Australia", "state": "New South Wales", "city": "Armidale", "domain": "une.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Southern Queensland", "country": "Australia", "state": "Queensland", "city": "Toowoomba", "domain": "usq.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of the Sunshine Coast", "country": "Australia", "state": "Queensland", "city": "Sippy Downs", "domain": "usc.edu.au", "aliases": [], "type": "University", "control": "Public"},
    # Other public universities
    {"name": "Australian Catholic University", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "acu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Charles Sturt University", "country": "Australia", "state": "New South Wales", "city": "Bathurst", "domain": "csu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Edith Cowan University", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "ecu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Macquarie University", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "mq.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Queensland University of Technology", "country": "Australia", "state": "Queensland", "city": "Brisbane", "domain": "qut.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Swinburne University of Technology", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "swinburne.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Canberra", "country": "Australia", "state": "ACT", "city": "Canberra", "domain": "canberra.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Newcastle", "country": "Australia", "state": "New South Wales", "city": "Newcastle", "domain": "newcastle.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Tasmania", "country": "Australia", "state": "Tasmania", "city": "Hobart", "domain": "utas.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Wollongong", "country": "Australia", "state": "New South Wales", "city": "Wollongong", "domain": "uow.edu.au", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Victoria University", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "vu.edu.au", "aliases": [], "type": "University", "control": "Public"},
    # Private universities
    {"name": "Bond University", "country": "Australia", "state": "Queensland", "city": "Gold Coast", "domain": "bond.edu.au", "aliases": [], "type": "University", "control": "Private"},
    {"name": "University of Notre Dame Australia", "country": "Australia", "state": "Western Australia", "city": "Fremantle", "domain": "notredame.edu.au", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Torrens University Australia", "country": "Australia", "state": "South Australia", "city": "Adelaide", "domain": "torrens.edu.au", "aliases": [], "type": "University", "control": "Private"},
    {"name": "University of Divinity", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "divinity.edu.au", "aliases": [], "type": "University", "control": "Private"},
]

AU_COLLEGES = [
    {"name": "TAFE NSW", "country": "Australia", "state": "New South Wales", "city": "Sydney", "domain": "tafensw.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "TAFE Queensland", "country": "Australia", "state": "Queensland", "city": "Brisbane", "domain": "tafeqld.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "TAFE SA", "country": "Australia", "state": "South Australia", "city": "Adelaide", "domain": "tafesa.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "South Metropolitan TAFE", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "southmetrotafe.wa.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "North Metropolitan TAFE", "country": "Australia", "state": "Western Australia", "city": "Perth", "domain": "northmetrotafe.wa.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Melbourne Polytechnic", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "melbournepolytechnic.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Holmesglen Institute", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "holmesglen.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Box Hill Institute", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "boxhill.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Chisholm Institute", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "chisholm.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Kangan Institute", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "kangan.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "William Angliss Institute", "country": "Australia", "state": "Victoria", "city": "Melbourne", "domain": "angliss.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Canberra Institute of Technology", "country": "Australia", "state": "ACT", "city": "Canberra", "domain": "cit.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "TasTAFE", "country": "Australia", "state": "Tasmania", "city": "Hobart", "domain": "tastafe.tas.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Charles Darwin University TAFE", "country": "Australia", "state": "Northern Territory", "city": "Darwin", "domain": "cdu.edu.au", "aliases": [], "type": "Institute", "control": "Public"},
]

def main():
    au_dir = DATA_DIR / "australia"
    au_dir.mkdir(parents=True, exist_ok=True)
    (au_dir / "scripts").mkdir(exist_ok=True)

    unis = sorted(AU_UNIVERSITIES, key=lambda r: (r["state"], r["name"]))
    cols = sorted(AU_COLLEGES, key=lambda r: (r["state"], r["name"]))

    with open(au_dir / "universities.json", "w", encoding="utf-8") as f:
        json.dump(unis, f, indent=2, ensure_ascii=False)
    with open(au_dir / "colleges.json", "w", encoding="utf-8") as f:
        json.dump(cols, f, indent=2, ensure_ascii=False)

    print(f"Australia Universities: {len(unis)}")
    print(f"Australia Colleges/TAFE: {len(cols)}")
    print(f"Australia Total: {len(unis) + len(cols)}")

if __name__ == "__main__":
    main()
