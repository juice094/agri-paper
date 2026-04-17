# ⚠️ Project Status: Under Active Audit and Refactoring

**Last Updated:** 2026-04-15

## Important Notice

This repository contains a **research prototype** for a local-first, configuration-driven agent architecture in agricultural knowledge management. It is currently under **active audit and substantial refactoring**.

### What has been done
- A comprehensive integrity and engineering review was conducted on **2026-04-15** (see `PHASE_REPORT_2026-04-15.md`).
- Critical issues identified during the audit have been corrected in subsequent commits:
  - Dataset documentation was rewritten to accurately reflect the small scale and templated nature of the benchmark.
  - Misleading claims in the LaTeX sources regarding "zero-code" TOML-driven validation were corrected to honestly disclose the coexistence of programmatic construction and declarative loading paths.
  - Erroneous citation metadata (including a suspected fabricated DOI/volume for `agrarian2025`) was corrected.
  - The proxy evaluation table in `experiments.tex` was explicitly labeled as **simulated / no actual LLM invoked**.
  - A dangling Git submodule was removed and the knowledge-base structure was normalized.
- **Rust-native local inference path verified:** `tools/rust_llm_poc/` compiles successfully against `kalosm 0.4` (Candle backend), including CUDA GPU acceleration on an RTX 4060. An interactive terminal REPL is available, and a standalone `eval` binary has been created for the 80-record stratified benchmark.
- **RAG coupling verified:** The REPL now loads a 30-record knowledge base (`agricultural_diseases_all.jsonl`) and injects the top-1 retrieved record into the prompt before generation, using a naive keyword-overlap retriever.
- **Eval binary ready:** `tools/rust_llm_poc/src/eval.rs` implements the full stratified benchmark (Baseline-A: no context, Baseline-B: crop filter, Proposed: top-1 RAG). It compiles but has not yet been run end-to-end.

### What remains incomplete
- **No real LLM evaluation has been performed.** All retrieval and latency experiments are integration tests that bypass the LLM generation layer.
  - *The Rust eval binary (`tools/rust_llm_poc/src/eval.rs`) is ready and `cargo check` passes. The only remaining blocker is obtaining a 7B quantized model that can run the 80-record stratified benchmark at feasible speed on an RTX 4060 8GB. A local 14B model is available and has been used to verify functional correctness, but it is too slow for the full benchmark.*
- **The knowledge base remains small:** 30 seed records expanded to 210 templated QA pairs. This is sufficient for architecture-level prototyping but not for generalization claims.
- **The TOML-driven configuration has not yet been validated end-to-end in the retrieval benchmark.** The benchmark tests still construct the agriculture profile programmatically for CI reproducibility.

### What this means
- **This project is NOT ready for peer-reviewed journal or conference submission** in its current state.
- It may be suitable as an **arXiv preprint or internal technical report** *provided* the limitations are clearly disclosed, but even that should wait until real LLM evaluations are added.
- External reviewers or employers examining this repository should read `PHASE_REPORT_2026-04-15.md` and the present file before drawing conclusions about earlier commits.

### Next steps (blocked on local environment)
1. **Obtain a 7B quantized model** (Qwen2.5-7B-Instruct Q4_K_M) — manual download is needed because automated HuggingFace downloads fail with a Windows SSL certificate revocation error. Then execute the 80-record stratified evaluation via `cargo run --bin eval` in `tools/rust_llm_poc/`.
2. **Integrate upgraded evaluation methodology** borrowed from competitor codebases: CPJ's 5-dimensional scoring and Agri-CM³'s P-M-K reasoning-level stratification. See the detailed plan in [`w4/research/MATURE_ROADMAP_2026-04-17.md`](w4/research/MATURE_ROADMAP_2026-04-17.md).
3. Scale the knowledge base to 500+ records via public datasets (`w4/research/kb_expansion_plan.md`), guided by AgMMU's real-dialogue distillation approach.
4. Re-compile the arXiv PDF from the corrected sources.

---

*This notice exists because earlier commits in the public Git history contained experimental artifacts and claims that have since been corrected. We are committed to transparently documenting both the prototype's potential and its current limitations.*
