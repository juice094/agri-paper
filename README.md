# agri-paper

A research prototype exploring a **local-first, configuration-driven agent architecture for agricultural knowledge management**.

> ⚠️ **This repository is under active audit and refactoring.** Please read [`PROJECT_STATUS.md`](PROJECT_STATUS.md) before examining earlier commits or using any materials for academic purposes.

---

## Overview

The project investigates whether a generic Rust agent framework (Clarity) can be adapted to agricultural pest and disease diagnosis through external configuration files (the "Domain-as-Config" paradigm), using the Model Context Protocol (MCP) to communicate with a local knowledge-base backend (devbase).

Key components:
- **LaTeX paper sources** in `w4/arxiv/` and `w4/writer/`
- **Agricultural QA benchmark** in `datasets/` (210 templated questions derived from 30 seed records)
- **Knowledge base** in `w3/engineer/agri_knowledge_base/` (30 crop-disease records)
- **Research plans** in `w4/research/` for LLM evaluation and knowledge-base expansion

---

## Repository Structure

```
agri-paper/
├── datasets/              # Agricultural QA benchmark and generation scripts
├── w1/                    # Early-phase artifacts (literature matrix, outline)
├── w3/                    # Mid-phase artifacts (CNKI research, knowledge base, demo)
├── w4/
│   ├── arxiv/             # arXiv submission LaTeX sources
│   ├── writer/            # Internal writer-draft LaTeX sources
│   ├── research/          # Experiment plans and evaluation scripts
│   └── engineer/          # Validation results and metrics
├── PHASE_REPORT_2026-04-15.md   # Latest audit and status report
└── PROJECT_STATUS.md      # Important notice on project maturity
```

---

## Current Limitations

- The knowledge base is small (30 seed records).
- The 210 QA pairs are **template-generated surface paraphrases**, not independent samples.
- **No live LLM has been evaluated** in the reported experiments.
- The retrieval benchmark uses programmatic profile construction for CI reproducibility, not yet a pure TOML-loaded end-to-end test.

See `PROJECT_STATUS.md` and `PHASE_REPORT_2026-04-15.md` for full details.

---

## Citation

If you use the benchmark generation methodology or dataset structure, please cite the seed records derived from public extension literature and the phase report documenting the audit process.

---

*This is a prototype. Use with appropriate skepticism and check the latest reports before drawing conclusions.*
