# Methodology

## Data Sources

### United States

| Source | Description |
|--------|-------------|
| **IPEDS / NCES** | Integrated Postsecondary Education Data System from the US Department of Education. The authoritative source for accredited US institutions. |
| **Wikipedia** | Lists of universities and colleges by state. Cross-referenced for completeness. |
| **Official Websites** | Each domain is verified against the institution's official website. |

### Canada

| Source | Description |
|--------|-------------|
| **Universities Canada** | National membership organization representing Canadian universities. |
| **Provincial Directories** | Government education directories for each province/territory. |
| **Official Websites** | Each domain is verified against the institution's official website. |

## Collection Process

1. **Aggregate** institution lists from the sources above
2. **Normalize** names (remove trailing "The", standardize abbreviations)
3. **Extract** the primary domain from the official website URL
4. **Classify** by type (`University`, `College`, `Community College`, `Institute`) and control (`Public`, `Private`)
5. **Deduplicate** by name and domain
6. **Validate** domain format and optionally resolve via DNS

## Validation Rules

| Rule | Description |
|------|-------------|
| No duplicates | Each institution name and domain must be unique within its country file |
| Official domain only | Must be the main institutional domain, not a subdomain (e.g. `stanford.edu`, not `cs.stanford.edu`) |
| Valid format | No `http://`, no `www.`, no trailing slashes |
| Required fields | All fields (`name`, `country`, `state`, `city`, `domain`, `aliases`, `type`, `control`) must be present |
| Enum values | `type` must be one of: `University`, `College`, `Community College`, `Institute`. `control` must be `Public` or `Private`. |

## Domain Selection

When an institution has multiple domains, we select the **primary institutional domain**:

- ✅ `mit.edu` — main institutional domain
- ❌ `web.mit.edu` — subdomain
- ❌ `libraries.mit.edu` — department subdomain

Alternative official domains (e.g. when a university operates under multiple TLDs) are recorded in the `aliases` array.

## Quality Assurance

- Automated validation via `scripts/validate_domains.py`
- Spot-check samples from each dataset
- Community contributions reviewed via pull requests
