# agri-paper

![Status](https://img.shields.io/badge/status-research%20prototype-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

A research prototype exploring a **local-first, configuration-driven agent architecture for agricultural knowledge management**.

> ⚠️ **This repository is under active audit and refactoring.** Please read [`PROJECT_STATUS.md`](PROJECT_STATUS.md) before examining earlier commits or using any materials for academic purposes.

---

## Overview

The project investigates whether a generic Rust agent framework (**Clarity**) can be adapted to agricultural pest and disease diagnosis through external configuration files (the "Domain-as-Config" paradigm), using the Model Context Protocol (**MCP**) to communicate with a local knowledge-base backend (**devbase**).

Key components:
- **LaTeX paper sources** in `w4/arxiv/` and `w4/writer/`
- **Agricultural QA benchmark** in `datasets/` (210 templated questions derived from 30 seed records)
- **Knowledge base** in `w3/engineer/agri_knowledge_base/` (30 crop-disease records)
- **Research plans** in `w4/research/` for LLM evaluation and knowledge-base expansion
- **Rust-native LLM PoC** in `tools/rust_llm_poc/` (local inference via [`kalosm`](https://github.com/floneum/floneum) + Candle)

---

## Repository Structure

```
agri-paper/
├── datasets/              # Agricultural QA benchmark and generation scripts
├── tools/                 # Rust-native local-LLM inference PoC
├── w1/                    # Early-phase artifacts (literature matrix, outline)
├── w3/                    # Mid-phase artifacts (CNKI research, knowledge base, demo)
├── w4/
│   ├── arxiv/             # arXiv submission LaTeX sources
│   ├── writer/            # Internal writer-draft LaTeX sources
│   ├── research/          # Experiment plans and evaluation scripts
│   └── engineer/          # Validation results and metrics
├── PHASE_REPORT_2026-04-15.md   # Latest audit and status report
├── LOCAL_LLM_CHECKLIST.md       # Step-by-step guide to run local model evals
└── PROJECT_STATUS.md            # Important notice on project maturity
```

---

## Current Limitations

- The knowledge base is small (30 seed records).
- The 210 QA pairs are **template-generated surface paraphrases**, not independent samples.
- **No live LLM evaluation has been executed yet.** The retrieval and latency experiments are integration tests that bypass the generation layer.
  - *Update:* A Rust-native inference path (`kalosm` → `Qwen2.5-7B-Instruct-GGUF`) has been verified to compile, **including CUDA GPU acceleration on RTX 4060**. An interactive terminal REPL is available. The next step is downloading the quantized model and running the 80-record stratified benchmark.
- The retrieval benchmark uses programmatic profile construction for CI reproducibility, not yet a pure TOML-loaded end-to-end test.

See `PROJECT_STATUS.md` and `PHASE_REPORT_2026-04-15.md` for full details.

---

## Why this project matters

> **agri-paper 的优势不是"模型更聪明"，而是"让聪明的通用模型，通过架构设计（配置 + 检索 + Rust 本地引擎），变成农民可以离线使用的、数据可控的、领域可迁移的专家系统。"**

在农业等数据敏感、网络条件差的场景下，"本地优先"不仅是技术偏好，更是基础设施刚需。本项目探索的 **Domain-as-Config** 范式表明：你不需要重新训练一个农业大模型，只需要把领域知识整理成结构化配置，就能让通用本地 LLM 在离线的环境下提供专业、可解释的农业建议。

---

## Quickstart (for developers)

```bash
# 1. Browse the benchmark
cat datasets/agricultural_diseases_all.jsonl | head -n 3

# 2. Inspect the evaluation plan
cat w4/research/llm_eval_plan.md

# 3. Check the Rust-native LLM PoC
cd tools/rust_llm_poc
cargo check        # kalosm compiles (CPU or CUDA GPU)
cargo run --release  # GPU inference recommended if CUDA 12.6 is installed
```

---

## Citation

If you use the benchmark generation methodology or dataset structure, please cite the seed records derived from public extension literature and the phase report documenting the audit process.

---

*This is a prototype. Use with appropriate skepticism and check the latest reports before drawing conclusions.*
