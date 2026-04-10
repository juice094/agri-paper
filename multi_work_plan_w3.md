# W3 多工作并行执行计划

> 阶段：W3（方法实现 + 知识库构建 + 初稿写作）
> 目标：三项工作并行推进，周六晚进行统一交接与整合

---

## 一、工作流总览

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   知网调研员     │    │   论文撰稿人     │    │   代码工程师     │
│  CNKI Agent(A2) │    │  Writer Agent(C) │    │  Code Agent(B2) │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         ▼                      ▼                      ▼
[cnki_results.md]         [introduction.tex]      [agri_knowledge_base/]
[cnki_bib.txt]            [related_work.tex]      [end_to_end_demo.log]
                                 │                      │
                                 └──────────┬───────────┘
                                            ▼
                                   [methodology.tex]
```

---

## 二、子任务 1：知网查询（中文核心文献补充）

### 负责人
子代理 `CNKI-Agent(A2)`

### 目标
补充 **10–15 篇中文核心文献**（2019–2025），重点覆盖：
1. 《农业工程学报》中关于农业专家系统、农业知识图谱、农业信息化的研究
2. 《农业图书情报学报》中关于农业知识管理、领域本体的研究
3. 知网硕博论文中关于"配置驱动""声明式"农业信息系统的探索

### 关键词策略
- 主题词："农业信息化" + "专家系统" / "知识图谱" / "Agent"
- 主题词："智慧农业" + "知识管理" / "决策支持系统"
- 主题词："精准农业" + "配置" / "DSL" / "模型驱动"
- 期刊限定：《农业工程学报》《农业图书情报学报》《中国农机化学报》《农机化研究》

### 交付物
1. `cnki_results.md`：表格形式，含篇名、作者、年份、来源、摘要核心点、与本研究的关联度评分（1–5）
2. `cnki_bib.txt`：GB/T 7714 格式参考文献列表，可直接插入中文稿
3. `cnki_gap_analysis.md`：从中文文献视角补充的 1–2 个 Gap（与英文文献矩阵形成互补）

### 验收标准
- ≥10 篇中文核心（北大核心或 CSCD）
- 至少 3 篇来自《农业工程学报》
- 每篇有明确的"可引用点"（Introduction 或 Discussion 中的具体位置）

---

## 三、子任务 2：论文撰写（Introduction + Related Work 初稿）

### 负责人
子代理 `Writer-Agent(C)`

### 目标
基于已有的 `outline.md`、`literature_matrix.md`、`innovation_claim.md`，产出：
1. `introduction.tex`（~800 words）
2. `related_work.tex`（~1,200 words）

### 写作规范
- 使用 Elsevier `elsarticle` 模板格式
- 图表引用使用 `\ref{fig:architecture}` 等占位符
- 参考文献使用 `\cite{key}`，key 来自文献矩阵中的编号（如 `\cite{gong2025kgllm}`）
- 查重预控：避免直接复制文献矩阵中的原句，进行同义改写和逻辑重构

### Introduction 结构要求
1. **Paragraph 1**：农业病虫害诊断的重要性（粮食安全、农民收入）
2. **Paragraph 2**：现有系统的两种路径及其痛点（云端大模型 vs 边缘轻量模型）
3. **Paragraph 3**：问题陈述——硬编码领域逻辑导致的迁移成本高、云端依赖风险
4. **Paragraph 4**：研究目标（RO1/RO2/RO3）
5. **Paragraph 5**：主要贡献（3 点）
6. **Paragraph 6**：论文结构概述

### Related Work 结构要求
1. **2.1 农业病虫害诊断专家系统**
   - RiceMan、AgrODSS（本体+规则）
   - AgenticGraphRAG（LLM+KG）
   - Chat Demeter（多 Agent + CNN）
   - **批判性总结**：垂直应用型，缺乏水平架构通用性
2. **2.2 农业大语言模型与知识图谱**
   - AgriGPT、AgroLLM、KGLLM
   - **批判性总结**：云端部署为主，本地优先研究不足
3. **2.3 MCP 协议与配置驱动架构**
   - IoT-MCP、AGRARIAN、Precision Agriculture DSL
   - **批判性总结**：农业垂直领域的 MCP 标准与本地优先 Agent 实践空白
4. **2.4 Rust 原生 Agent 框架**
   - Rig、RusticAI、ADK-Rust
   - **批判性总结**：缺乏同时支持 TUI、Subagent、MCP Client 的本地优先平台

### 交付物
1. `introduction.tex`
2. `related_work.tex`
3. `citations.bib`：初步的 BibTeX 条目（至少 20 条）

---

## 四、子任务 3：项目代码实现（农业数据集 + 端到端 Demo）

### 负责人
子代理 `Code-Agent(B2)`

### 目标
1. 构建最小可运行的农业知识库数据集
2. 通过 devbase 的 `scan` + `index` + `query` 建立索引
3. 跑通"配置 → Agent 系统提示 → MCP 工具查询 → 结果返回"的端到端链路

### 数据集策略（最小可行方案）
由于真实农业教材 PDF 的版权和获取周期问题，采用**合成+公开元数据**的混合策略：

**方案 A（优先）**：
- 从公开农业数据集（如 PlantVillage 的 `readme` / `metadata.csv`）提取病虫害名称、作物类型、症状描述
- 生成结构化的 JSON/TXT 文件，存储在 `agri_knowledge_base/` 中
- 每个文件代表一种"作物-病虫害"组合，包含：
  - `crop`：作物名称
  - `disease`：病虫害名称
  - `symptoms`：症状描述（英文或中文）
  - `treatment`：防治建议（基于农业常识生成或公开资料整理）

**方案 B（保底）**：
- 若公开元数据获取困难，直接手写 10–15 种常见作物病虫害的结构化文本
- 确保覆盖水稻、小麦、玉米、柑橘、番茄等 `agri_profile.toml` 中声明的作物

### devbase 索引流程
```bash
# 1. 将农业知识库注册为 devbase 的"仓库"（使用 scan --register）
devbase scan agri_knowledge_base/ --register

# 2. 建立索引（knowledge_engine::run_index）
devbase index agri_knowledge_base/

# 3. 查询验证
devbase query "crop:rice"
```

> 注：devbase 当前主要面向 Git 仓库设计。如果农业知识库目录不是 git repo，需先 `git init` 一个空仓库，或用 devbase 的 `scan` 的 `--register` 强制注册非 git 目录（视 devbase 实现而定）。

### 端到端 Demo 设计
不依赖 TUI 的完整 LLM 集成，而是写一个**独立的 Rust 测试/示例程序**：

```rust
// crates/clarity-core/examples/agriculture_demo.rs
// 或 tests/agriculture_end_to_end.rs

// 1. 加载 agriculture profile 配置
// 2. 初始化 McpToolRegistry（连接 devbase）
// 3. 构造系统提示词（注入 domain 信息）
// 4. 模拟 LLM 的 tool_calls 决策：选择 devbase__devkit_query
// 5. 执行查询：expression = "crop:rice symptom:yellow_leaf"
// 6. 将查询结果包装为 assistant 回复的一部分
// 7. 输出完整对话日志
```

这个 demo 不调用真实 LLM API（避免成本和网络依赖），而是**模拟 LLM 的 tool call 决策流程**，验证"配置 → Agent → MCP → 知识库 → 结果"的完整链路。

### 交付物
1. `agri_knowledge_base/`：数据集文件（JSON/TXT/Markdown）+ `README.md`（数据来源说明）
2. `crates/clarity-core/tests/agriculture_end_to_end.rs` 或 `examples/agriculture_demo.rs`：端到端 demo 代码
3. `demo.log`：运行 demo 产生的完整输出日志（证明链路跑通）
4. `devbase_index_report.md`：devbase 索引结果报告（条目数、查询样例、响应时间）

### 验收标准
- 数据集覆盖 ≥10 种作物-病虫害组合
- devbase `query` 能检索到至少 1 条有效结果
- demo 日志完整展示：配置加载 → tool 选择 → MCP 调用 → 结果返回
- `cargo test --test agriculture_end_to_end -- --nocapture` 通过（如果是测试形式）

---

## 五、时间线与同步机制

### Day 1–2（周三–周四）
- **A2**：完成知网关键词检索，产出 `cnki_results.md` 初稿
- **C**：完成 `introduction.tex` 初稿
- **B2**：完成数据集收集/生成，开始 devbase 索引

### Day 3–4（周五–周六）
- **A2**：产出 `cnki_bib.txt` 和 `cnki_gap_analysis.md`
- **C**：完成 `related_work.tex` 初稿 + `citations.bib`
- **B2**：完成端到端 demo 代码和 `demo.log`

### Day 5（周日）
- 三人进行异步文档交接
- 主代理（你）整合三项产出，生成 `handover_w3.yaml`
- 确定 W4 实验设计细节

---

## 六、子代理交接协议

每个子代理完成任务后，必须在交付目录中生成一个 `handover_subagent.yaml`：

```yaml
from: "CNKI-Agent(A2)"
to: "Writer-Agent(C) + Main Agent"
date: "2026-04-13"
artifacts:
  - path: "cnki_results.md"
    verified: true
blockers: []
notes: "文献[3]为网络首发，尚未分配页码，引用时标注 DOI"
```

---

## 七、风险控制

| 风险 | 概率 | 影响 | 备案 |
|------|------|------|------|
| 知网访问受限（无校园 VPN） | 40% | 中 | 改用万方/维普/百度学术替代，或手动整理已公开的农业工程学报文章摘要 |
| devbase 对非 git 目录索引失败 | 30% | 中 | 在知识库目录下 `git init` 空仓库后再扫描 |
| 数据集质量过低导致查询无结果 | 20% | 中 | 直接手写 15 条高质量结构化记录，确保 demo 可用 |
| 论文初稿查重率偏高 | 15% | 低 | C 在写作时主动进行同义改写，避免长句照搬 |
