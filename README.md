# University and College Domains

A global open dataset of official university and college domains. Designed for identity verification, academic email validation, research, and application integrations.

## Overview

This repository provides a **structured, searchable, and continuously expanding database** of academic institution domains worldwide. Each record includes the institution's name, location, primary domain, type, and control (public/private).

### Coverage

| Country | Records | Approx. Target | Coverage % | Status |
|---|---|---|---|---|
| China | 6219 | 3117 | 199% | ✅ OK |
| Usa | 5892 | 5762 | 102% | ✅ OK |
| Brazil | 3534 | 1264 | 279% | ✅ OK |
| India | 3063 | 5300 | 57% | ⚠️ Good |
| Philippines | 2956 | 2400 | 123% | ✅ OK |
| Russia | 2642 | 1010 | 261% | ✅ OK |
| Mexico | 1912 | 1139 | 167% | ✅ OK |
| France | 1808 | 625 | 289% | ✅ OK |
| Indonesia | 1600 | 3277 | 48% | ❌ Gap |
| Nigeria | 1179 | 200 | 589% | ✅ OK |
| Poland | 996 | 392 | 254% | ✅ OK |
| South Korea | 908 | 401 | 226% | ✅ OK |
| Canada | 884 | 383 | 230% | ✅ OK |
| Iran | 882 | 400 | 220% | ✅ OK |
| Japan | 803 | 803 | 100% | ✅ OK |
| Spain | 752 | 350 | 214% | ✅ OK |
| Vietnam | 680 | ? | ? | ❓ Unknown |
| Argentina | 614 | 174 | 352% | ✅ OK |
| Pakistan | 607 | 500 | 121% | ✅ OK |
| Colombia | 495 | 350 | 141% | ✅ OK |
| Morocco | 378 | ? | ? | ❓ Unknown |
| Germany | 343 | 422 | 81% | ✅ OK |
| Uk | 241 | 260 | 92% | ✅ OK |
| Turkey | 188 | 207 | 90% | ✅ OK |
| Malaysia | 145 | ? | ? | ❓ Unknown |
| Italy | 137 | 310 | 44% | ❌ Gap |
| Bangladesh | 86 | 150 | 57% | ⚠️ Good |
| Taiwan | 85 | 152 | 55% | ⚠️ Good |
| Thailand | 85 | 170 | 50% | ⚠️ Good |
| Switzerland | 81 | ? | ? | ❓ Unknown |

**Total Records:** 42,824
**Total Countries:** 195
**Countries with ≥80% coverage:** 20 (among top 30)

## Data Format

Data is stored as **JSON** in country subdirectories, split into `universities.json` and `colleges.json`:

```json
{
  "name": "Stanford University",
  "country": "USA",
  "state": "California",
  "city": "Stanford",
  "domain": "stanford.edu",
  "aliases": [],
  "type": "University",
  "control": "Private"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Official institution name |
| `country` | string | Country code or name |
| `state` | string | State, province, or region |
| `city` | string | City where the main campus is located |
| `domain` | string | Primary official domain |
| `aliases` | string[] | Alternative official domains |
| `type` | string | `University`, `College`, `Community College`, or `Institute` |
| `control` | string | `Public` or `Private` |

## Usage

### Python

```python
import json
from pathlib import Path

# Load all US institutions
universities = json.loads(Path("data/usa/universities.json").read_text())
colleges = json.loads(Path("data/usa/colleges.json").read_text())
all_usa = universities + colleges

# Validate an email domain
email = "student@stanford.edu"
domain = email.split("@")[1]

match = next((i for i in all_usa if i["domain"] == domain or domain in i["aliases"]), None)

if match:
    print(f"Verified: {match['name']} ({match['type']}, {match['control']})")
else:
    print("Domain not found in database")
```

### JavaScript

```javascript
const fs = require('fs');

const universities = JSON.parse(fs.readFileSync('./data/usa/universities.json'));
const colleges = JSON.parse(fs.readFileSync('./data/usa/colleges.json'));
const allUSA = [...universities, ...colleges];

const domain = 'stanford.edu';
const match = allUSA.find(i => i.domain === domain || i.aliases.includes(domain));

if (match) {
  console.log(`Verified: ${match.name}`);
}
```

## Scripts

### Validate Data

```bash
pip install -r scripts/requirements.txt
python scripts/validate_domains.py
```

### Import from IPEDS (US Dept of Education)

```bash
python data/usa/scripts/full_reimport.py
```

Downloads the IPEDS HD2023 federal database and rebuilds the USA dataset.

## File Structure

```
university-college-domains/
├── data/
│   ├── usa/            # 6,033 records (99% coverage)
│   ├── canada/         # 158 records (100% coverage)
│   ├── uk/             # 155 records (~95% coverage)
│   ├── australia/      # 55 records (~95% coverage)
│   ├── germany/        # 69 records (~25% coverage)
│   └── <country>/
│       ├── universities.json
│       ├── colleges.json
│       └── scripts/    # Country-specific data importers
├── scripts/
│   ├── validate_domains.py   # Data validation (all countries)
│   ├── collect_domains.py    # General collection framework
│   └── requirements.txt
├── docs/
│   └── methodology.md
├── LICENSE
└── README.md
```

## Validation Rules

1. Domain must be the **official institutional domain** (not a department subdomain)
2. No duplicate institution names within a file
3. No duplicate domains across different countries
4. Prefer the main institutional domain:
   - ✅ `stanford.edu`
   - ❌ `cs.stanford.edu`, `mail.stanford.edu`

## Data Sources

- **USA**: [IPEDS HD2023](https://nces.ed.gov/ipeds/) — US Department of Education's Integrated Postsecondary Education Data System
- **Global Extraction**: Extracted comprehensive datasets using:
    - **Wikipedia API**: Recursive sub-category scanning across 60+ regional/provincial lists. Cross-referenced English Wikipedia with 12+ native-language Wikipedias (zh, ko, fr, ru, pt, es, id).
    - **WES API (World Education Services)**: Directly imported institution names through WES Credential Evaluation directories, matched with Wikipedia pages for primary domain verification.
- **Canada**: Universities Canada directory, provincial education directories, official websites

## Roadmap

- [x] Phase 1 — United States (~98% coverage)
- [x] Phase 2 — Canada (~100% coverage)
- [x] Phase 3 — High-Density Gap Analysis & Targeted Expansion (21,000+ total global coverage achieved)
- [ ] Phase 4 — Data normalizations (city, state validation for EU regions)
- [ ] Phase 5 — API endpoint for domain verification
- [ ] Email domain validation service

## Contributing

1. Fork the repository
2. Edit or add the relevant JSON file in `/data/<country>/`
3. Run `python scripts/validate_domains.py` to verify
4. Submit a pull request

## License

This dataset is released under the [MIT License](LICENSE).
