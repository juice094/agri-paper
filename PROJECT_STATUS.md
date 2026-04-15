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

### What remains incomplete
- **No real LLM evaluation has been performed.** All retrieval and latency experiments are integration tests that bypass the LLM generation layer.
- **The knowledge base remains small:** 30 seed records expanded to 210 templated QA pairs. This is sufficient for architecture-level prototyping but not for generalization claims.
- **The TOML-driven configuration has not yet been validated end-to-end in the retrieval benchmark.** The benchmark tests still construct the agriculture profile programmatically for CI reproducibility.

### What this means
- **This project is NOT ready for peer-reviewed journal or conference submission** in its current state.
- It may be suitable as an **arXiv preprint or internal technical report** *provided* the limitations are clearly disclosed, but even that should wait until real LLM evaluations are added.
- External reviewers or employers examining this repository should read `PHASE_REPORT_2026-04-15.md` and the present file before drawing conclusions about earlier commits.

### Next steps (blocked on local environment)
1. Install Ollama and run local LLM generation experiments (`w4/research/llm_eval_plan.md`).
2. Scale the knowledge base to 500+ records via public datasets (`w4/research/kb_expansion_plan.md`).
3. Re-compile the arXiv PDF from the corrected sources.

---

*This notice exists because earlier commits in the public Git history contained experimental artifacts and claims that have since been corrected. We are committed to transparently documenting both the prototype's potential and its current limitations.*
