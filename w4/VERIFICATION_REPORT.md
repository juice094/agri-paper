# W4 论文与实际内容比对验证报告（修订版）

**Date:** 2026-04-15  
**Scope:** 对 `agri-paper` 项目进行工程与学术层面的深度审计，修正虚假陈述、规范数据结构、清理形式主义文档。

---

## 执行摘要

本次验证对论文 `main_arxiv.tex`（及分章节源文件）与实际代码仓库、数据集和项目文件进行了逐条核对。**本报告是对此前 2026-04-10 版本的诚实修订**。此前版本将大量未解决的技术债务标记为"已修复"，存在误导性。本次改造针对以下核心问题进行了实质性修正：

1. **悬空 Git 子模块**：`w3/engineer/agri_knowledge_base` 缺少 `.gitmodules` 映射，且 README 虚假声称目录内有 30 条记录（实际仅 15 条）。
2. **数据集文档失实**：210 条 benchmark 是 30 条种子记录的 7 次模板改写，但此前未明确披露其非独立性。
3. **论文中的学术诚信风险**：投稿版本（arxiv）删除了关于测试硬编码的关键说明；代理评估表格以模拟值冒充实验结果；存在引用信息错误/虚构。
4. **交接文件形式主义**：所有 `handover_*.yaml` 的 SHA-256 checksum 均为 `"sha256:pending"` 却标记 `verified: true`。

---

## 一、本次改造已完成的实质性修正

### 1. Git 子模块与知识库结构 ✅

**问题**：`w3/engineer/agri_knowledge_base` 在 Git tree 中标记为 submodule（mode 160000），但 `.gitmodules` 文件不存在；子模块内部 README 声称有 30 条记录，实际仅 15 条。

**改造措施**：
- 移除了悬空子模块引用（`git rm --cached`）。
- 将子模块内容保留为普通目录，直接纳入主仓库跟踪。
- 把 W4 的 `extended_diseases.jsonl` 合并到知识库目录。
- 创建合并后的完整数据集 `agricultural_diseases_all.jsonl`（30 条）。
- 重写 README.md，诚实披露数据来源、规模和局限性。

### 2. 数据集生成脚本与文档 ✅

**问题**：`generate_benchmark.py` 和 `merge_benchmark.py` 存在 `IndexError` 风险（硬编码 `s.split(',')[1]` / `[2]` 假设）；`random.seed(42)` 未使用；210 条 benchmark 的非独立性未披露。

**改造措施**：
- 添加 `safe_symptom_fragments()` 保护逻辑和 `extract_keywords()` 改进函数。
- 移除无意义的 `random` 代码。
- 在脚本头部和数据集 README 中**明确添加免责声明**：210 条记录是 7 个模板对 30 条种子的表面改写，不应用于泛化评估。
- 重新生成了 `agri_qa_benchmark.jsonl` 和 `agri_qa_benchmark_extended.jsonl`。

### 3. 论文源文件去毒化 ✅

**问题**：
- `methodology.tex`（arxiv 版）删除了测试硬编码的关键说明，虚假声称"直接从外部 TOML 加载"。
- `experiments.tex` 中代理评估表格（`tab:generation_proxy`）以模拟值呈现，易误导为真实 LLM 实验结果；未诚实披露 Baseline-CropOnly 已达 100% Hit@3。
- `discussion.tex` 使用"10% to 100% accuracy gap"的表述夸大改进幅度。
- `citations.bib` 中存在错误/虚构出版信息（如 `agrarian2025` 的 LNCS 14500 卷号）。

**改造措施**：
- 恢复 `methodology.tex` 中关于程序化构造与 TOML 加载并存的诚实说明。
- 在代理评估部分添加醒目的 **"Important disclaimer: No actual LLM was evaluated"** 声明，并将表格描述改为"projected proxy scores"。
- 在 `experiments.tex` 和 `discussion.tex` 中明确说明 Baseline-CropOnly 因知识库设计（每作物恰好 3 条记录）已达 100% Hit@3，Proposed 的贡献在于 Hit@1 和 KeywordRecall@1 的提升。
- 增强 `Limitations` 子节，明确说明：数据集规模小、无真实 LLM 调用、模板生成导致的独立性不足。
- 修正 `citations.bib` 中 5 条引用的错误信息（`agrarian2025`, `chatdemeter2025`, `kgllm2024`, `agenticgraphrag2025`, `iotmcp2025`）。
- 同步更新了 `main_arxiv.tex`（扁平化 arXiv 版本）中的对应文本与 `thebibliography` 条目。

### 4. 交接文件清理 ✅

**问题**：`w1/handover_w1.yaml`、`w1/handover_w2.yaml`、`w3/handover_w3.yaml` 中所有 artifacts 的 `checksum` 均为 `"sha256:pending"`，但 `verified` 却全部为 `true`。

**改造措施**：
- 将 `checksum` 设为 `null`，`verified` 设为 `false`。
- 添加顶部注释和每条 notes，明确说明这些文件是**回顾性流程产物**，未进行加密校验，仅通过人工检查复核。

---

## 二、已知但尚未解决的技术债务

以下问题在本次改造中**被如实披露但未被工程修复**，需要在后续工作中解决：

| # | 问题 | 影响 | 当前状态 |
|---|------|------|----------|
| 1 | **TOML 配置文件未被集成测试直接加载** | 中 | 论文已诚实披露：测试中同时存在程序化构造路径和 TOML 加载路径，但检索 benchmark 仍使用程序化构造。`agri_profile.toml` 本质上是演示性 artifact。 |
| 2 | **无真实 LLM 生成评估** | 高 | 论文已在 Limitations 和代理评估部分明确承认。所有实验均为绕过 LLM 的 Rust 集成测试。 |
| 3 | **检索评分机制过于简单** | 中 | 使用的是 token 重叠打分，没有 BM25、向量嵌入或农业本体匹配。论文已说明这在小规模知识库上足够，但不足以支撑大规模部署。 |
| 4 | **LaTeX 编译产物与压缩包被移除** | 低 | 根据 `.gitignore`，`w4/arxiv/` 中的 `.aux`, `.log`, `.out`, `.pdf`, `.zip`, `.tar.gz` 已被删除。如需投稿，需在具备 LaTeX 环境的机器上重新编译。 |

---

## 三、论文价值重评估

### 3.1 仍可宣称的亮点（经修正后）

1. **MCP stdio 农业适配的工程验证**
   - 将 MCP 协议（含 Content-Length/NDJSON 双解析、动态工具发现）与本地 SQLite 知识库打通，并在完全离线环境下测得约 18 ms 端到端延迟。这在农业 AI 的本地优先部署中具有工程参考价值。

2. **配置驱动的水平迁移概念**
   - `DomainConfig` + `Profile` + `McpToolRegistry` 的组合展示了通过外部配置（而非源码修改）适配新作物的架构潜力。虽然当前验证路径包含程序化构造，但框架本身支持 TOML/JSON 加载。

### 3.2 必须弱化的声称（已修改）

1. **"首个 MCP-based 农业 Agent 架构"** → 改为更谦逊的表述或删除绝对化用词。当前版本已减少"first"的使用，但仍需在最终投稿前进一步核查是否有先行工作。
2. **"100% 检索准确率证明架构优越性"** → 已修正为：100% Hit@3 在 Baseline-CropOnly 上同样可达，Proposed 的真正贡献是 Hit@1 和 KeywordRecall@1。
3. **代理评估数值** → 已明确标注为理论投影（theoretical projection），非实测。

### 3.3 投稿建议

- **arXiv 预印本**：当前修正后的版本**可以上传 arXiv**，作为快速公开原型和获取社区反馈的手段，但摘要和方法论中仍需保持谦逊。
- **Peer-reviewed 期刊**：由于缺少真实 LLM 评估、TOML 端到端测试未完全闭合、数据集规模极小，**不建议直接投稿 SCI/SSCI 期刊**。如需投稿，必须先补充真实生成实验和更大规模的知识库验证。

---

## 四、可交付物状态（改造后）

| 文件/目录 | 状态 | 说明 |
|-----------|------|------|
| `w3/engineer/agri_knowledge_base/` | ✅ 已规范化 | 移除悬空子模块，合并 extended_diseases.jsonl，README 诚实化 |
| `datasets/*.jsonl` | ✅ 已重新生成 | 脚本修复并运行，文档含独立性免责声明 |
| `w4/arxiv/*.tex` | ✅ 已修正 | 关键学术不端风险点已去除 |
| `w4/arxiv/*.pdf` | ❌ 已删除 | 按 `.gitignore` 移除，需重新编译 |
| `w4/arxiv/*.zip` / `*.tar.gz` | ❌ 已删除 | 按 `.gitignore` 移除，需从最新源文件重建 |
| `handover_*.yaml` | ✅ 已清理 | 移除虚假 checksum + verified 组合 |
| `citations.bib` | ✅ 已修正 | 5 条错误引用信息已更新 |

---

## 五、下一步建议（按优先级排序）

1. **补充真实 LLM 生成评估**
   - 使用 Ollama 或 llama.cpp 本地运行量化模型，对至少一部分 benchmark 查询生成回答，人工或自动化评估准确性和幻觉率。

2. **实现 TOML 配置文件端到端加载测试**
   - 修改 Rust 集成测试，使其直接从 `agri_profile.toml` 加载配置并运行完整检索 benchmark，消除"程序化构造"与"零代码声明"之间的差距。

3. **扩大知识库规模或接入公开数据集**
   - 将 AI-AgriBench 或 AgMMU 的公开子集转换为本地可检索格式，验证系统在更大、更不平衡数据上的检索表现。

4. **重新编译 arXiv PDF 与源文件包**
   - 在具备 MiKTeX/TeX Live 的环境中重新编译 `main_arxiv.tex`，并重新打包 `arxiv_upload.zip` 和 `arxiv_source.tar.gz`。
