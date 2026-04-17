# ⚠️ Project Status: Under Active Audit and Refactoring

**Last Updated:** 2026-04-17

## Important Notice

This repository contains a **research prototype** for a local-first, configuration-driven agent architecture in agricultural knowledge management. It is currently under **active audit and substantial refactoring**.

## What has been done (as of 2026-04-17)

### Audit corrections (2026-04-15)
- A comprehensive integrity and engineering review was conducted (see `PHASE_REPORT_2026-04-15.md`).
- Critical issues identified during the audit have been corrected:
  - Dataset documentation was rewritten to accurately reflect the small scale and templated nature of the benchmark.
  - Misleading claims in the LaTeX sources regarding "zero-code" TOML-driven validation were corrected.
  - Erroneous citation metadata was corrected.
  - The proxy evaluation table in `experiments.tex` was explicitly labeled as **simulated / no actual LLM invoked**.
  - A dangling Git submodule was removed and the knowledge-base structure was normalized.

### kalosm local inference (2026-04-15 ~ 04-17)
- **`tools/rust_llm_poc/` compiles successfully** against `kalosm 0.4` (Candle backend), including CUDA GPU acceleration on an RTX 4060.
- **Interactive REPL** (`main.rs`) loads 30-record KB and injects top-1 retrieved context before generation (RAG coupling verified).
- **`eval.rs` binary** implements the full 80-record stratified benchmark:
  - Three conditions: Baseline-A (no context), Baseline-B (crop filter), Proposed (top-1 RAG)
  - **CPJ-inspired 5-dimensional rule-based scoring** (Plant/Disease/Symptom/Format/Completeness)
  - Per-condition summary JSON output
  - `cargo check --bin eval` passes

### Cross-project integration deliverables (2026-04-17)
- **`configs/agri_expert.toml`**: Persona TOML golden sample for clarity-core `DomainPersonaConfig` parsing test. Includes template variable interpolation (`{{crop}}`, `{{region}}`, etc.), tool schema definitions, safety blacklist, and domain vocabulary.
- **`docs/agri_tag_vocabulary.md`**: Complete agricultural tag namespace v0.1.0 for devbase `repo_tags` (6 categories, 14 crops, 11 regions, query examples, mapping to `agri_observations`).
- **`schemas/agri_observations.sql`**: Updated DDL v0.2.0 for devbase migration, incorporating all review feedback (`observed_at`, `lat`/`lon`, `severity` CHECK constraint, composite index).
- **Competitor codebases registered** in devbase: CPJ, Agri-CM³, AgMMU (cloned to `dev/third_party`, tagged, and papers table populated).
- **`MATURE_ROADMAP_2026-04-17.md`**: Phase 1–4 cross-project roadmap with competitor benchmark methodology integration.

## What remains incomplete

- **No real LLM evaluation has been performed.** The Rust eval binary is ready but the 80-record benchmark has not been executed end-to-end.
  - *Blocker:* 7B quantized model download. HuggingFace auto-download fails with Windows SSL cert revocation error (`CRYPT_E_NO_REVOCATION_CHECK`). 14B model is available for functional verification but too slow for the full 80-record run.
- **The knowledge base remains small:** 30 seed records expanded to 210 templated QA pairs. Sufficient for architecture-level prototyping but not for generalization claims.
- **The TOML-driven configuration has not yet been validated end-to-end** in the retrieval benchmark.
- **Cross-project interface negotiations pending:**
  - clarity-core: `LlmProvider` trait definition and `DomainPersonaConfig` parsing skeleton
  - devbase: `agri_observations` migration PR (committed by agri-paper for 2026-04-18)

## What this means

- **This project is NOT ready for peer-reviewed journal or conference submission** in its current state.
- It may be suitable as an **arXiv preprint or internal technical report** *provided* the limitations are clearly disclosed, but even that should wait until real LLM evaluations are added.
- External reviewers or employers examining this repository should read `PHASE_REPORT_2026-04-15.md`, `MATURE_ROADMAP_2026-04-17.md`, and the present file before drawing conclusions about earlier commits.

## Next steps

### P0 (blocks all downstream work)
1. **Obtain 7B quantized model** (`Qwen2.5-7B-Instruct Q4_K_M`) — manual download required due to Windows SSL issue.
   - Attempting ModelScope mirror as alternative to HuggingFace.
   - Fallback: run 20-record smoke test with 14B if 7B remains unavailable.
2. **Run `cargo run --bin eval --release`** in `tools/rust_llm_poc/` once model is ready.

### P1 (parallel, no dependency on 7B)
3. **Submit devbase PR** for `agri_observations` migration (DDL + `save/query` stubs + feature flag). **Deadline: 2026-04-18.**
4. **Wait for clarity-core `DomainPersonaConfig` parsing skeleton** — agri-paper will iterate `agri_expert.toml` v0.2.0 within 24h of receiving skeleton.

### P2 (post-benchmark)
5. Integrate Agri-CM³ P-M-K reasoning-level stratification into eval output.
6. Scale knowledge base to 500+ records via USDA IPM + AI-AgriBench (guided by AgMMU distillation method).
7. Re-compile arXiv PDF with real evaluation results.

---

*This notice exists because earlier commits in the public Git history contained experimental artifacts and claims that have since been corrected. We are committed to transparently documenting both the prototype's potential and its current limitations.*
