# Contributing to University & College Domains

First off, thank you for considering contributing to the **Global University & College Domains Dataset**! The scale and accuracy of this project rely on community input.

## How to Contribute Data

### 1. Data Structure Restrictions
- Ensure all entries are placed inside the correct country directory (e.g. `data/mexico/universities.json`).
- Verify the physical geolocation (State/City) whenever possible.
- The `domain` property **must** point to the canonical root web domain of the institution (e.g., `mit.edu`). Do not link directly to sub-departments unless placing them inside the `aliases` array.

### 2. Testing Your Changes Locally
Before submitting a Pull Request, you **must** validate the integrity of your addition to ensure there are no duplicate domains across borders or JSON syntax errors.

```bash
# 1. Install standard dependencies
pip install -r scripts/requirements.txt

# 2. Run the constraint validator
python scripts/validate_domains.py
```

*Note: Our GitHub Actions CI pipeline will auto-reject PRs that fail this validation check.*

### 3. Pull Requests
- Fill out the provided Pull Request template completely.
- Provide a link to the official institution website to verify your addition.
- Keep PRs scoped locally. If you are adding universities in France and universities in Japan, please separate them into two PRs if they are large batches.

## Modifying Scripts
If you are modifying the Python crawling infrastructure inside `/scripts/`:
- Ensure you do not hardcode absolute path strings.
- Add robust error handling (e.g., `try/except` for remote HTTP errors).
- Document the methodology of the script in the Pull Request.
