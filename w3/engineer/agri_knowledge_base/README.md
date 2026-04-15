# Agricultural Knowledge Base

This directory contains a structured dataset of crop diseases and pests for the configuration-driven agricultural agent architecture research.

## Data Source

The dataset was manually curated from publicly available agricultural extension resources, including:
- FAO (Food and Agriculture Organization) crop protection guidelines
- Regional agricultural extension service publications
- Plant pathology reference materials for major staple crops

Records were synthesized and validated against standard symptom descriptions and integrated pest management (IPM) recommendations.

## Files

| File | Description | Records |
|------|-------------|---------|
| `agricultural_diseases.jsonl` | Original seed dataset | 15 |
| `extended_diseases.jsonl` | Extended seed dataset (W4) | 15 |
| `agricultural_diseases_all.jsonl` | Merged dataset containing all 30 records | 30 |

## Coverage

| Crop    | Records | Source File |
|---------|---------|-------------|
| Rice    | 3       | `agricultural_diseases.jsonl` |
| Wheat   | 3       | `agricultural_diseases.jsonl` |
| Corn    | 3       | `agricultural_diseases.jsonl` |
| Citrus  | 3       | `agricultural_diseases.jsonl` |
| Tomato  | 3       | `agricultural_diseases.jsonl` |
| Soybean | 3       | `extended_diseases.jsonl` |
| Potato  | 3       | `extended_diseases.jsonl` |
| Cotton  | 3       | `extended_diseases.jsonl` |
| Peanut  | 3       | `extended_diseases.jsonl` |
| Apple   | 3       | `extended_diseases.jsonl` |
| **Total** | **30** | Combined across both files |

## Data Limitations

- **Small scale**: This is a minimal viable knowledge base intended for architecture-level prototyping only. Each disease is represented by a single symptom description and a single treatment paragraph.
- **No visual data**: The dataset does not include images or field photographs.
- **Regional generalization**: Descriptions are generic and do not capture geographic or seasonal variations.

## Record Format

Each line is a JSON object with the following fields:
- `crop`: Target crop (e.g., rice, wheat, corn)
- `disease`: Disease or pest name
- `symptoms`: Observable symptoms in plain English
- `treatment`: Prevention and treatment recommendations

## Indexing

This directory is registered as a `devbase` repository and indexed for keyword search via the `devbase__devkit_query` MCP tool.
