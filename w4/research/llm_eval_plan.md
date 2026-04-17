# LLM 生成评估实验方案（v2 — 方法论升级）

**状态：** 技术路径已就绪（kalosm REPL + eval 二进制编译通过），阻塞于 7B 模型下载  
**目标：** 为 agri-paper 补充真实的本地 LLM 生成评估，替代当前的模拟代理评估。  
**方法论升级：** 基于 CPJ (`cpj_ref`) 的 5 维度评分与 Agri-CM³ (`agricm3_ref`) 的 P-M-K 分层推理框架，评估协议已从单一规则评分升级为分层 + Judge + 信度验证体系。详见 [`MATURE_ROADMAP_2026-04-17.md`](MATURE_ROADMAP_2026-04-17.md)。

---

## 一、实验目标

1. 使用本地量化模型对 80 条 stratified benchmark 查询生成回答。
2. 评估生成回答的 **5 维度评分**（ borrowed from CPJ ）：
   - **Plant Accuracy**：正确识别作物
   - **Disease Accuracy**：正确识别病害
   - **Symptom Accuracy**：精确描述症状
   - **Format Adherence**：回答同时包含诊断与治疗建议
   - **Completeness**：全面且专业（≥30 词，含具体措施）
3. 引入 **P-M-K 分层标签**（ borrowed from Agri-CM³ ），定位模型失效根因：
   - **P (Perception)**：作物/病害识别能力
   - **M (Mixed P-C)**：症状→病害推理能力
   - **K (Knowledge)**：治疗方案知识应用能力
3. 对比三种检索上下文条件：
   - **Baseline-A**：无检索上下文（纯参数化 LLM）
   - **Baseline-B**：仅作物过滤后的上下文（CropOnly RAG）
   - **Proposed**： symptom-level 排序后的精确 top-1 上下文（Domain-as-Config RAG）

---

## 二、推荐模型与运行环境

| 模型 | 参数 | 量化 | 预计显存/内存 | 适用性 |
|------|------|------|---------------|--------|
| Qwen2.5-7B-Instruct | 7B | Q4_K_M | ~5 GB | 中文农业术语理解较好，推荐首选 |
| Llama-3.1-8B-Instruct | 8B | Q4_K_M | ~5 GB | 英文表现强，农业领域稍弱 |
| Qwen2.5-14B-Instruct | 14B | Q4_K_M | ~9 GB | 如有足够显存，推理质量更高 |

**运行平台：** kalosm（纯 Rust，Candle 后端，CUDA GPU 已验证）  
**调用方式：** `cargo run --bin eval --release`  
**备选：** Ollama / llama.cpp（若 kalosm 遇到模型兼容问题）

---

## 三、实验流程

### Step 1：获取本地 7B 量化模型

因 Windows SSL 证书吊销检查导致 HuggingFace 自动下载失败，建议**手动下载**：

```powershell
# 通过浏览器或镜像站下载 Qwen2.5-7B-Instruct-Q4_K_M.gguf
# 放置到：C:\Users\22414\Desktop\model\Qwen2.5-7B-Instruct-Q4_K_M.gguf
# 代码会自动检测并优先加载 7B（回退 14B）
```

### Step 2：构造 Prompt

对于每个查询，构造如下格式的 prompt：

```
You are an agricultural extension officer. A farmer asks:

"{query}"

Use the following retrieved knowledge to answer:

{retrieved_context}

Provide a concise diagnosis and actionable management recommendations.
If the context does not contain enough information, say so.
```

其中 `retrieved_context` 根据实验条件变化：
- Baseline-A：空字符串（"No retrieved context available."）
- Baseline-B：该作物的 3 条记录拼接
- Proposed：top-1 记录

### Step 3：批量生成

运行 `w4/research/run_llm_eval.py`（待编写），输入为 `datasets/agri_qa_benchmark_extended.jsonl` 的子集（建议 stratified 采样：easy 30 + medium 30 + hard 20 = 80 条）。

### Step 4：自动评分（LLM-as-a-Judge + 规则匹配双模式）

**Fast Mode（规则匹配，零 API 成本）：**
- Plant Accuracy：`expected_crop` 是否出现在回答中
- Disease Accuracy：`expected_disease` 是否出现在回答中
- Symptom Accuracy：`expected_symptoms` 关键词命中比例
- Format Adherence：回答是否同时包含症状描述和管理建议
- Completeness：回答字数 ≥30 词，且含具体措施（药剂/时间/方法）

**Deep Mode（本地 LLM-as-a-Judge，数据主权）：**
- 使用本地 7B/14B 模型作为 Judge，prompt 参考 `cpj_ref/step3_answer_selection/diagnosis_judge.py`。
- 输出 JSON 格式的 5 维度评分（0–1 每项，总分 0–5）。
- 验证：抽取 20%（16 条）由用户人工评分，计算与 Judge 的一致率（目标 ≥75%）。

**安全性筛查：**
- 维护一个有害建议黑名单（如 "spray gasoline", "burn the field"），命中即标记为 0 分并记录。

---

## 四、预期产出

1. `w4/research/llm_eval_results.json`：80 条查询的生成结果与评分。
2. `w4/research/llm_eval_report.md`：包含三张对比表格（Baseline-A vs Baseline-B vs Proposed）的分析报告。
3. 论文 `experiments.tex` 中代理评估表格的替换/补充说明。

---

## 五、当前阻塞项

- **Ollama 未安装**（`C:	rogram Files
ollama.exe` 不存在）。
- **无本地量化模型文件**。

**下一步动作（需用户/其他 Agent 在合适时机执行）：**
1. 下载并安装 Ollama for Windows。
2. 执行 `ollama pull qwen2.5:7b`。
3. 运行本目录下的 `run_llm_eval.py` 脚本（待实现）。

---

## 六、评估实现

评估主体已迁移至 Rust 二进制 `tools/rust_llm_poc/src/eval.rs`，支持：
- 自动检测本地 7B/14B 模型
- 加载 30-record KB 并进行 stratified 采样（easy 30 + medium 30 + hard 20）
- 三种检索条件对比：Baseline-A / Baseline-B / ProposedTop1
- JSONL + JSON 输出

**待增强项（参考 `MATURE_ROADMAP_2026-04-17.md`）：**
- [ ] 在 `eval.rs` 中集成 P/M/K 分层标签
- [ ] 引入 CPJ 5 维度评分（规则匹配版）
- [ ] 可选：增加 `judge.rs` 实现本地 LLM-as-a-Judge
