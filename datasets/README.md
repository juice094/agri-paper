# Agricultural QA Benchmark Dataset

## Overview
This directory contains a **self-contained agricultural question-answering benchmark** used for validating the configuration-driven, local-first agriculture agent architecture described in the paper.

Because external agricultural benchmark datasets (e.g., AgriBench, AI-AgriBench, AgMMU) could not be reliably downloaded due to network constraints in the current environment, we constructed a **synthetic-but-grounded** benchmark from high-quality seed records. The extended 210-record benchmark is used for architecture-level validation: it measures retrieval accuracy, configuration-migration overhead, and end-to-end pipeline latency rather than training a new deep-learning model.

## Files

| File | Description |
|------|-------------|
| `agricultural_diseases.jsonl` (source: `w3/engineer/agri_knowledge_base/`) | 15 original handcrafted crop-disease records covering rice, wheat, corn, citrus, and tomato. |
| `extended_diseases.jsonl` (source: `w4/research/`) | 15 additional records covering soybean, potato, cotton, peanut, and apple. |
| `agri_qa_benchmark.jsonl` | 105 QA records generated from the original 15 seeds. |
| `agri_qa_benchmark_extended.jsonl` | 210 QA records generated from all 30 seeds (original 15 + extended 15). |
| `generate_benchmark.py` | Script that expands the original 15 seed records into the 105-record benchmark using templated question variants. |
| `merge_benchmark.py` (source: `w4/research/`) | Script that merges original and extended seeds into the 210-record extended benchmark. |

## Benchmark Structure

Each line in `agri_qa_benchmark_extended.jsonl` is a JSON object with the following schema:

```json
{
  "id": "agri_qa_000_0",
  "crop": "rice",
  "query": "My rice shows diamond-shaped lesions on leaves. What disease could this be?",
  "expected_disease": "Rice Blast",
  "expected_keywords": ["apply tricyclazole...", "use resistant varieties"],
  "symptoms": "...",
  "treatment": "...",
  "type": "diagnosis_from_first_symptom",
  "difficulty": "easy"
}
```

### Question Types
- `diagnosis_from_first_symptom` – single leading symptom
- `diagnosis_and_management` – full symptom list + management ask
- `symptom_recognition` – asks for symptoms of a known disease
- `treatment_recall` – asks for treatment of a known disease
- `multi_symptom_diagnosis` – two secondary symptoms, diagnosis + control
- `prevention_and_treatment` – prevention/treatment of a disease
- `field_observation` – verbose field-report style (hardest)

### Difficulty Distribution
- **Easy**: ~45 questions (direct symptom → disease or treatment recall)
- **Medium**: ~45 questions (combined symptoms + management)
- **Hard**: ~15 questions (verbose field-observation narrative)

## Validation Tasks

### T1 – Knowledge-Base Retrieval Accuracy
For each `query`, the agent (or retrieval function) searches the local `agricultural_diseases.jsonl` knowledge base. Success is defined as the `expected_disease` appearing in the top-k retrieved records.

Metrics:
- `Hit@1`, `Hit@3`, `Hit@5`
- `KeywordRecall@1` – whether `expected_keywords` are present in the top-1 result
- Stratified accuracy by `difficulty`

### T2 – Configuration-Migration Baseline
Compare the proposed *Domain-as-Config* approach against a simulated hard-coded baseline:
- **Baseline-HC**: hypothetical hard-coded adapter (measured in equivalent LOC and manual migration time)
- **Proposed**: `DomainConfig::agriculture()` loaded from TOML/JSON; zero code changes in core framework

Metric:
- `ConfigMigrationTime` – time to switch active profile
- `LOCMigration` – lines of code added (0 for proposed vs ~200+ for baseline)

### T3 – End-to-End Pipeline Latency
Measure wall-clock time for:
1. Load agriculture profile
2. Initialize `McpToolRegistry` and connect to `devbase` MCP server
3. Construct domain-injected system prompt
4. Execute `devkit_query` via MCP stdio
5. Parse JSON response

Metric:
- `EndToEndLatency` (ms)
- `McpToolRegistryInitLatency` (ms)
- `QueryExecutionLatency` (ms)

## Citation
If you use this benchmark, please cite the seed records derived from public extension literature and the paper’s methodology section.
