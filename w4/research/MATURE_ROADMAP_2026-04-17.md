# 成熟化路线图：agri-paper × clarity × devbase 交叉项目演进

**日期：** 2026-04-17  
**版本：** v1.0（基于竞品源码扫描后的方法论升级）  
**核心原则：** 协议优先、下游驱动、单向依赖、先验证后抽象  

---

## 一、竞品源码参照的发现与可借鉴点

本阶段通过直接克隆与分析 3 个关键开源竞品/基准仓库，识别出当前 agri-paper 在**评估方法论**与**数据构造**上的核心差距，并提取可直接落地的改进方案。

### 1.1 已注册的竞品仓库（devbase 本地知识库）

| 仓库 ID | 来源 | 本地路径 | 标签 | 核心借鉴价值 |
|---------|------|----------|------|--------------|
| `cpj_ref` | [CPJ-Agricultural/CPJ-Agricultural-Diagnosis](https://github.com/CPJ-Agricultural/CPJ-Agricultural-Diagnosis) | `C:\Users\22414\Desktop\cpj_ref` | `benchmark, agriculture, llm-as-judge, cpj` | **评估流水线**：5 维度评分（Plant/Disease/Symptom/Format/Completeness）+ LLM-as-a-Judge + 人工验证协议（Cohen's κ=0.88） |
| `agricm3_ref` | [HIT-Kwoo/Agri-CM3](https://github.com/HIT-Kwoo/Agri-CM3) | `C:\Users\22414\Desktop\agricm3_ref` | `benchmark, agriculture, multimodal, agricm3` | **分层评估框架**：Perception (P) → Mixed Perception-Cognition (M) → Knowledge Application (K) 三级推理拆解 |
| `agmmu_ref` | [AgMMU/AgMMU](https://github.com/AgMMU/AgMMU) | `C:\Users\22414\Desktop\agmmu_ref` | `benchmark, agriculture, multimodal, agmmu` | **数据蒸馏方法**：11.6 万 USDA 专家真实对话 → 746 MCQ/OEQ + 5.7 万知识事实的流水线 |

> 同时注册了 `cpj2025`、`agricm3_2025`、`agmmu2025`、`agridoctor2025` 四篇论文到 devbase `papers` 表，便于后续知识检索与引用。

### 1.2 关键差距与 borrowable 方案

| 差距项 | 当前状态 | 竞品方案 | 本项目落地策略 |
|--------|---------|----------|----------------|
| **评估维度单一** | 仅 3 维度规则评分（诊断/治疗/安全） | Agri-CM³ 的 **P-M-K 三级分层** | 引入轻量级分层测试：30 条测 P（作物识别）、30 条测 M（症状→病害推理）、20 条测 K（治疗方案知识） |
| **缺乏 LLM-as-a-Judge** | 计划用规则匹配 + 可选 API Judge | CPJ 的 **5 维度评分 + tie-breaking + 人工校验协议** | 在 `eval.rs` 或 `run_llm_eval.py` 中复用 CPJ 的 judge prompt（本地化到纯文本场景，去除图像相关描述） |
| **数据构造伪多样性** | 30 seed → 210 模板 QA | AgMMU 的 **真实对话蒸馏** | 明确标注 210 QA 为"架构验证集"；中期以 USDA IPM + AI-AgriBench 真实问答为来源重构 |
| **无人工信度验证** | 未规划 | CPJ 的 **N=396, κ=0.88** | 80-record benchmark 中抽取 20%（16 条）由用户（农业背景）做人工双盲评分，计算简单一致性 |

---

## 二、Phase 1–4 修订版路线图

### Phase 1：最小数据闭环（当前，预计 2026-04-20 完成）

**目标：** 在 agri-paper 中完成"本地模型 → RAG 检索 → 生成 → 评分"的端到端验证，产出可复现的 benchmark 二进制。

**成功标准（修订后）：**
- [x] `tools/rust_llm_poc/` 编译通过（含 CUDA）
- [x] REPL 可加载 30-record KB 并进行 RAG 注入生成
- [x] `eval.rs` 实现 stratified 80-record 三条件对比
- [ ] **7B 模型就绪并跑通 10 条 smoke test**（放宽：14B 验证功能后，7B 为 benchmark 速度优化）
- [ ] **引入 CPJ 评分维度**：将原 3 维度扩展为 5 维度（+ Symptom Accuracy + Format Adherence），并在 `eval.rs` 中实现规则匹配版自动评分

**关键动作：**
1. **7B 模型获取替代方案**：因 HuggingFace 自动下载受 Windows SSL 吊销检查阻塞，改用：
   - 浏览器/迅雷/镜像站手动下载 `Qwen2.5-7B-Instruct-Q4_K_M.gguf`
   - 或从已有的 14B 文件来源（如 modelscope）同步下载 7B 版本
2. **eval.rs 评分增强**：参考 `cpj_ref/step3_answer_selection/diagnosis_judge.py` 的 5 维度 JSON schema，在 Rust 端用 `serde_json` + 正则匹配实现快速规则评分。

---

### Phase 2：方法论升级与评估层抽象（2026-04-20 至 05-05）

**目标：** 参照 CPJ 与 Agri-CM³，将评估从"单一生成测试"升级为"分层 + Judge + 信度验证"的成熟方法论。

**成功标准：**
- [ ] `eval.rs` 输出包含 **P/M/K 分层标签** 与 **5 维度评分**
- [ ] 实现一个独立的 `judge.rs`（或 Python `judge.py`），支持两种模式：
  - **Fast mode**：本地规则匹配（零 API 成本）
  - **Deep mode**：调用本地 7B/14B 模型作为 LLM-as-a-Judge（数据主权，无云 API）
- [ ] 完成 80-record 完整跑通，生成 `llm_eval_summary_*.json`
- [ ] 人工抽检 16 条，记录一致性率（目标 ≥80%）

**竞品源码直接借鉴：**
- **CPJ `diagnosis_judge.py`**：将其 system prompt 中"图像描述"替换为"检索上下文"，保留 5 维度评分逻辑。
- **Agri-CM³ `evaluation/`**：学习其按 reasoning level 拆分 MCQ 的 JSON 格式，将我们的 open-ended QA 也标记 `level: 1|2|3`。

---

### Phase 3：Clarity 集成与生态卡位（2026-05-05 至 05-25）

**目标：** 将验证过的 kalosm 推理路径抽象为 Clarity 的 Provider，并通过 MCP 暴露给 devbase/agri-paper。

**成功标准：**
- [ ] Clarity 新增 `KalosmProvider`（本地 GGUF 加载）
- [ ] devbase MCP Server 暴露 `agri_query` 工具：输入作物+症状 → 返回 top-k 检索结果
- [ ] agri-paper 的 `eval` 二进制可被 Clarity 通过 MCP 调用（即评估本身成为一个可复用的 Tool）
- [ ] 发布 `Agri-MCP-Server` 概念验证到 GitHub（最小可用：7 个工具中的 3 个）

**架构约束（重申）：**
- agri-paper 继续作为**下游验证场**，所有抽象必须先在 agri-paper 跑通后再上提到 clarity/devbase。
- 禁止在 clarity 中预设农业业务逻辑（如作物列表、病害名称），所有领域知识留在 agri-paper 的配置/TOML 中。

---

### Phase 4：数据扩展与论文迭代（2026-05-25 至 06-30）

**目标：** 参照 AgMMU 的真实对话蒸馏方法，将知识库从 30 seed 扩展至 500+ 真实记录，并重新编译 arXiv 投稿包。

**成功标准：**
- [ ] 知识库规模 ≥500 条（来源：USDA IPM Crop Profiles + AI-AgriBench 子集）
- [ ] 新 benchmark ≥300 条 QA，且**非模板生成**（≥60% 来自真实问答或专家文档改写）
- [ ] arXiv 版本 `experiments.tex` 中的代理评估表格被真实评估表格替换
- [ ] 在 Limitations 中诚实披露：本地 7B 量化模型的性能上限、无多模态、无边缘视觉输入

**数据扩展路径（参考 AgMMU）：**
1. **USDA IPM PDF 结构化**：爬取 20+ 作物 Profile，用本地 7B 模型提取 `crop|disease|symptoms|treatment` JSONL。
2. **AI-AgriBench 对齐**：申请测试集后，将其问题映射到我们的 KB 检索结果，做跨基准 RAG 评估。
3. **质量过滤**：按 `crop+disease` 去重，人工抽查 50 条，错误率 >5% 的数据源标记为"需二次校验"。

---

## 三、评估协议升级详情

### 3.1 分层测试设计（ borrowed from Agri-CM³ ）

| 层级 | 测试内容 | 样本数（80 条中） | 示例问题 |
|------|---------|------------------|---------|
| **P** (Perception) | 给定作物名称 + 症状描述，识别病害 | 20 | "What disease affects tomatoes with dark, sunken lesions at the blossom end?" |
| **M** (Mixed P-C) | 给定症状，推理出作物和病害 | 30 | "A farmer reports leaf curling, yellowing, and stunted growth. What is the likely disease and crop?" |
| **K** (Knowledge) | 给定病害，输出治疗方案与预防知识 | 30 | "How should Wheat Leaf Rust be managed?" |

> 注：由于当前 benchmark 是 open-ended 而非 Agri-CM³ 的 MCQ，我们将问题按上述三层分类，并在 `eval.rs` 中记录 `reasoning_level` 字段。

### 3.2 CPJ 5 维度评分本地化

将 CPJ 的图像诊断评分改造为**文本 RAG 场景评分**：

| 维度 | 定义 | 规则匹配快速评分 |
|------|------|------------------|
| Plant Accuracy | 正确识别作物 | `expected_crop` 是否在回答中出现（含别名/拉丁名） |
| Disease Accuracy | 正确识别病害 | `expected_disease` 是否在回答中出现 |
| Symptom Accuracy | 精确描述症状 | `expected_symptoms` 的关键词命中数 / 总关键词数 |
| Format Adherence | 包含诊断+治疗两部分 | 回答中是否同时出现症状描述和管理建议 |
| Completeness | 全面且专业 | 回答字数 ≥30 词，且包含至少一个具体措施（如药剂名称、施用时间） |

**总分 0–5**，与 CPJ 保持一致，便于后续学术对标。

### 3.3 LLM-as-a-Judge 的本地实现

由于数据主权诉求，**不依赖 GPT-4o API**，而是使用本地模型作为 Judge：

```rust
// judge.rs 伪代码
async fn llm_judge(answer: &str, ground_truth: &AgriRecord) -> JudgeScore {
    let prompt = format!(
        "You are an agricultural expert evaluator.\n\n\
        Ground truth: crop={}, disease={}, symptoms={}, treatment={}\n\n\
        Generated answer: {}\n\n\
        Rate the answer on 5 dimensions (0 or 1 each):\n\
        1. Plant Accuracy\n2. Disease Accuracy\n3. Symptom Accuracy\n4. Format Adherence\n5. Completeness\n\n\
        Output JSON only: {{\"plant\":0|1, \"disease\":0|1, ...}}",
        ground_truth.crop, ground_truth.disease, ...
    );
    // 复用 kalosm ChatSession，temperature=0.1
}
```

**验证**：取 16 条样本，用户人工评分 vs. 本地 Judge 评分，计算一致率。若 <75%，调整 prompt 或回退到规则匹配。

---

## 四、风险对冲与生存期决策

### 4.1 继续冻结的事项

| 冻结项 | 原因 |
|--------|------|
| **Seed records 规模** | 维持 30 条直到 Phase 2 评估跑通，避免在方法论未稳前扩大数据债务 |
| **LaTeX 双轨制重构** | writer/ 与 arxiv/ 的合并推迟到 Phase 4，当前以文档更新为主 |
| **Clarity 大规模代码重构** | 在 `KalosmProvider` 验证前，不改动 Clarity 的核心 Agent 编排逻辑 |

### 4.2 必须解除的阻塞项

| 优先级 | 阻塞项 | 解除 Deadline | 解除方案 |
|--------|--------|---------------|----------|
| P0 | 7B 模型手动下载 | 2026-04-20 | 浏览器/镜像站下载 GGUF，放入 `Desktop/model/` |
| P0 | eval.rs 端到端跑通 | 2026-04-25 | 先跑 10 条 smoke test，再跑 80 条完整 benchmark |
| P1 | CPJ 评分维度集成 | 2026-05-05 | 参考 `cpj_ref/diagnosis_judge.py` 的 prompt 和 JSON schema |
| P1 | AI-AgriBench 数据申请 | 2026-05-10 | 提交 `ai_agribench_request.md` 中已准备好的申请 |
| P2 | USDA IPM 爬虫 | 2026-05-20 | 编写 `ipm_crawler.py`，优先爬取 10 个高频作物 Profile |

### 4.3 若阻塞项无法按期解除的 B 计划

- **7B 模型始终无法下载**：用 14B 模型跑 **20 条精简 benchmark**（而非 80 条），作为概念验证写入论文 Limitations。
- **AI-AgriBench 申请被拒**：转向公开可用的 **AgMMU HuggingFace 数据集** 子集（知识事实部分），用其 QA 做外部验证。
- **人工评分无法完成**：仅报告自动评分结果，并在 Limitations 中明确说明"未经过农业专家人工验证"。

---

## 五、可交付物清单

| 阶段 | 文件/产物 | 说明 |
|------|----------|------|
| Phase 1 | `tools/rust_llm_poc/src/eval.rs` | 已存在，需增强 5 维度评分与 P/M/K 标签 |
| Phase 1 | `llm_eval_raw_*_*.jsonl` + `llm_eval_summary_*.json` | eval 输出（目标：80 条 × 3 条件） |
| Phase 2 | `tools/rust_llm_poc/src/judge.rs` | 新增的本地 LLM-as-a-Judge 模块 |
| Phase 2 | `w4/research/eval_methodology_v2.md` | 记录分层评估与 5 维度评分的协议文档 |
| Phase 3 | `clarity/src/provider/kalosm.rs` | Clarity 的 kalosm Provider（抽象自 agri-paper 验证代码） |
| Phase 3 | `devbase/src/mcp_agri.rs` | 农业查询的 MCP Tool 暴露（可选独立 crate） |
| Phase 4 | `datasets/agricultural_diseases_v2.jsonl` | ≥500 条记录的新知识库 |
| Phase 4 | `w4/arxiv/main_arxiv.pdf` | 基于真实评估结果重新编译的投稿包 |

---

## 六、引用与溯源

本路线图直接借鉴了以下已注册到 devbase 的竞品源码：
- **CPJ** (`cpj_ref`)：`step3_answer_selection/diagnosis_judge.py` 的评分维度和 LLM-as-a-Judge 协议。
- **Agri-CM³** (`agricm3_ref`)：`README.md` 中的 P-M-K 三级分层评估框架。
- **AgMMU** (`agmmu_ref`)：`README.md` 与 `scoring_eval_pipeline/` 中的 USDA 真实对话蒸馏与双轨（MCQ+OEQ）评估格式。

*文档生成后，下一步动作：*
1. 立即执行 7B 模型手动下载（P0 阻塞）。
2. 在 `eval.rs` 中先集成规则匹配版的 5 维度评分。
3. 将本路线图同步到 `PROJECT_STATUS.md` 与 `PHASE_REPORT_2026-04-15.md`。
