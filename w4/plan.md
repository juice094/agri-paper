# W4 Experimental Validation Plan

## Status
- **Dataset**: ✅ Self-contained 105-record agricultural QA benchmark generated from 15 real seed records.
- **Retrieval Benchmark**: ✅ Rust integration test passing (`agriculture_validation.rs`).
  - Baseline (random@3): 20.00% Hit Rate
  - Proposed (crop+symptoms): 100.00% Hit Rate
  - Keyword Recall@1: 99.05%
  - E2E MCP Latency: ~19 ms
- **End-to-End Demo**: ✅ MCP stdio pipeline working with `devbase`.

## W4 Goals
1. Formalize the experimental methodology section for the paper.
2. Add configuration-migration baseline metrics (LOC, time).
3. Run statistical significance tests on benchmark results.
4. Generate LaTeX tables/figures for the results.
5. Draft the **Experiments / Evaluation** section (~800–1,000 words).
6. (Stretch) Extend benchmark to 200+ records by crawling public extension facts.

## Experiment Design

### Tasks
| Task | Description | Metric |
|------|-------------|--------|
| T1 – Retrieval Accuracy | For each of 105 queries, retrieve relevant records from `agricultural_diseases.jsonl` | Hit@1, Hit@3, Hit@5, KeywordRecall@1 |
| T2 – Config Migration | Compare zero-code config switch vs. hypothetical hard-coded adapter | ConfigMigrationTime (ms), LOCMigration |
| T3 – E2E Latency | Full pipeline from profile load to MCP query response | EndToEndLatency (ms), broken down by component |
| T4 – Tool Discovery | Ensure agriculture profile always registers `devkit_query` | SuccessRate (%) |

### Baselines
- **Baseline-Random**: Randomly sample 3 records from the 15-record KB. Simulates an agent with no domain context.
- **Baseline-CropOnly**: Return all records for the target crop (3 records each). Simulates minimal domain knowledge.
- **Proposed**: `DomainConfig::agriculture()` + keyword-scored retrieval over symptoms and treatments.

### Results Snapshot (Current)
```
Baseline-Random@3 Hit Rate:  20.00% (21/105)
Baseline-CropOnly Hit Rate:  100.00% (105/105)
Proposed Hit Rate:           100.00% (105/105)
Proposed KeywordRecall@1:    99.05% (104/105)

Latency:
  Config Load:       ~1 ms
  Registry Init:     ~13 ms
  Query Execution:   ~5 ms
  Total E2E:         ~19 ms
```

## Subagent Tasks

### Agent A: Paper Writing (writer)
**Goal**: Draft the Experiments / Evaluation section in LaTeX.
**Deliverables**:
- `w4/writer/experiments.tex`
- Include methodology, dataset description, task definitions, results discussion, and a limitations paragraph.
- Embed LaTeX tables generated from the results snapshot above.

### Agent B: Engineering Metrics (engineer)
**Goal**: Harden the validation suite and add migration-baseline metrics.
**Deliverables**:
- Extend `agriculture_validation.rs` with a `Baseline-CropOnly` arm (currently only Random and Proposed exist).
- Add a micro-benchmark that measures `ConfigMigrationTime` (load agriculture profile vs. default profile) 100 times and reports mean/std.
- Output a `w4/engineer/validation_results.json` with all numeric results for the writer to consume.

### Agent C: Research Extension (research)
**Goal**: Attempt to expand the seed KB to 30+ real records using publicly available extension facts.
**Deliverables**:
- `w4/research/extended_diseases.jsonl` with 15 additional records (soybean, potato, cotton, etc.).
- A script `w4/research/merge_benchmark.py` that regenerates the 105-record QA set into a ~210-record set using the new seeds.
- If network blocks crawling, document the attempted sources and fall back to manual curation from well-known public facts (e.g., IPM guides).

## Handover Criteria
W4 is complete when:
- `experiments.tex` is written and compiles.
- `validation_results.json` contains T1–T4 metrics.
- All Rust tests pass (`cargo test -p clarity-core --test agriculture_validation`).
- (Optional) Benchmark expanded to 200+ records.

## Next Immediate Action
Launch Subagent A and B in parallel; launch C after A/B report initial progress.
