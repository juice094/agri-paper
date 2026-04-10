# Phase Report: TOML Gap Closure & arXiv Packaging

**Date:** 2026-04-10  
**Scope:** Close the Domain-as-Config test gap, clean up paper sources, and establish Git tracking for both `clarity` and `agri-paper` repositories.

---

## 1. Completed Work

### 1.1 TOML-Driven Integration Tests (`clarity`)
- **`agriculture_validation.rs`**
  - Now loads `agri_profile.toml` from `w1/engineer/agri_profile.toml` via `Config::loader().without_env().load_str()`.
  - Removed hard-coded `DomainConfig` / `Profile` construction.
  - Fixed `suspicious_double_ref_op` compiler warning.
  - Removed unused imports (`DomainConfig`, `Profile`).

- **`agriculture_end_to_end.rs`**
  - Refactored `build_agriculture_config()` to load the same external TOML file instead of programmatically building the config.
  - Patches the `devbase` MCP server path dynamically after TOML load.
  - Removed unused imports.

- **`config/mod.rs`**
  - Added `#[serde(default)]` to `DomainConfig.constraints` to ensure robust deserialization when the field is absent or empty in TOML.

### 1.2 Test Verification
All tests pass cleanly (0 warnings from test files):

```
cargo test -p clarity-core --test agriculture_end_to_end --test agriculture_validation -- --nocapture
```

| Test | Result | Key Metrics |
|------|--------|-------------|
| `test_agriculture_end_to_end_demo` | ✅ pass | E2E demo with TOML-loaded config |
| `test_agriculture_retrieval_benchmark` | ✅ pass | Hit@3 = 100.00%, KeywordRecall@1 = 99.52% (209/210) |
| `test_agriculture_end_to_end_mcp_latency` | ✅ pass | Config Load ~1–9 ms, Registry Init ~11–230 ms, Query ~5–18 ms, Total ~17–257 ms |
| `test_config_migration_overhead` | ✅ pass | Profile switch < 0.1 ms |

### 1.3 Paper Source Cleanup (`agri-paper/w4/arxiv`)
- **`methodology.tex`**: Removed the outdated caveat that tests "programmatically construct" the profile. The text now correctly states that both integration tests load directly from external TOML.
- **`main.tex`**, **`main_arxiv.tex`**, **`arxiv_submission.tex`**: Replaced placeholder author block (`Author Names / Affiliation`) with anonymous submission block (`Anonymous Authors / Anonymous Institution`).
- Removed the corrupted 0-byte `main.pdf` from `w4/arxiv/`.
- Recreated `arxiv_upload.zip` and `arxiv_source.tar.gz` with updated sources.

### 1.4 Git Tracking Established
- Initialized a new Git repository in `C:\Users\22414\clarity` and committed all source files (`.gitignore` excludes `target/` and `Cargo.lock`).
- Initialized a new Git repository in `C:\Users\22414\Desktop\agri-paper` and committed the full paper project (including datasets, handovers, and arXiv sources).

---

## 2. Known Limitations

| # | Issue | Impact | Mitigation |
|---|-------|--------|------------|
| 1 | **No LaTeX compiler on this Windows environment.** | `main_arxiv.pdf` (~408 KB, 16 pages) is the last successfully compiled PDF, but it does *not* yet reflect the two minor edits (author block + removed CI caveat). | Re-compile `main_arxiv.tex` on any machine with MiKTeX/TeX Live before final submission. The source archives are fully up-to-date. |
| 2 | **Root repo (`C:\Users\22414`) has unrelated syncthing changes.** | These were intentionally *not* committed because they are outside the scope of this agricultural-paper phase. | Handle syncthing work in a separate branch or session. |

---

## 3. Repository State

### `clarity`
- **Branch:** `main`
- **HEAD:** `a362ddc` — "feat(agri): TOML-driven config for integration tests"
- **Status:** clean working tree

### `agri-paper`
- **Branch:** `main`
- **HEAD:** `d165bb5` — "docs(paper): update arxiv sources for TOML-driven validation"
- **Status:** clean working tree
- **Note:** `w3/engineer/agri_knowledge_base` is tracked as an embedded Git repository (submodule hint emitted during initial add). If you intend to publish this repo, consider converting it to a proper submodule or flattening it.

---

## 4. Next Steps (Recommended Priority)

1. **Regenerate arXiv PDF**
   - On a machine with `pdflatex` + `bibtex`, run:
     ```bash
     cd w4/arxiv
     pdflatex main_arxiv.tex
     bibtex main_arxiv
     pdflatex main_arxiv.tex
     pdflatex main_arxiv.tex
     ```
   - Verify the output is 16 pages and that the author block reads "Anonymous Authors".

2. **Replace Anonymous Authors**
   - When you are ready to submit (or post to a pre-print server), replace the anonymous block in `main_arxiv.tex`, `main.tex`, and `arxiv_submission.tex` with real author names and affiliations.

3. **Expand Stress Testing (Optional but Recommended)**
   - Run the agriculture benchmark under simulated load:
     - Concurrent queries via `tokio::spawn` to measure throughput.
     - Large knowledge base (e.g., 1,000+ records) to see if Hit@3 / latency degrades.
   - This would strengthen the "Scalability" paragraph in `discussion.tex`.

4. **Add a Figure for the TOML Pipeline**
   - The paper currently describes the TOML-driven pipeline in text. A small TikZ or PlantUML diagram showing `agri_profile.toml → Config::loader() → DomainConfig → McpToolRegistry → devkit_query` would improve readability.

5. **Tag a Release**
   - Tag `clarity` and `agri-paper` with a consistent version (e.g., `v0.2.0-agri`) so the arXiv submission can reference a stable commit hash.

---

*Report generated automatically at the end of the TOML-gap-closure phase.*
