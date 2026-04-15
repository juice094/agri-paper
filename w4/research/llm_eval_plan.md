# LLM 生成评估实验方案（预备文档）

**状态：** 待执行（阻塞于 Ollama 未安装）  
**目标：** 为 agri-paper 补充真实的本地 LLM 生成评估，替代当前的模拟代理评估。

---

## 一、实验目标

1. 使用本地量化模型对 50–100 条 benchmark 查询生成回答。
2. 评估生成回答的：
   - **诊断正确性**（Diagnosis Correctness）
   - **治疗完整性**（Treatment Completeness）
   - **安全性**（Safety Adequacy）
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

**运行平台：** Ollama（Windows 本地）  
**调用方式：** HTTP API (`http://localhost:11434/api/generate`)  
**备选：** llama.cpp（如 Ollama 安装失败）

---

## 三、实验流程

### Step 1：安装 Ollama 并拉取模型

```powershell
# 1. 从 https://ollama.com/download/windows 下载安装包并安装
# 2. 拉取模型
ollama pull qwen2.5:7b
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

### Step 4：自动评分（LLM-as-a-Judge）

使用一个更强的 judge 模型（或通过规则匹配 + 轻量级本地模型）对生成结果评分。由于本地资源有限，推荐两种评分方案：

**方案 A（推荐）：规则匹配 + LLM Judge 混合**
- 诊断正确性：生成的回答中是否出现 `expected_disease`（不区分大小写）
- 治疗完整性：生成的回答中是否包含 `expected_keywords` 中的关键词
- 安全性：使用简单的否定词列表（如 "spray gasoline", "burn the field"）进行初筛，明显有害标记为 0，其余标记为 1。

**方案 B（更严谨但依赖外部 API）：使用 GPT-4o / Claude 作为 Judge**
- 将 query、ground-truth treatment、generated answer 输入 judge。
- Judge 按 0–1 分为三档评分。此方案因涉及 API 调用和费用，作为可选增强。

---

## 四、预期产出

1. `w4/research/llm_eval_results.json`：80 条查询的生成结果与评分。
2. `w4/research/llm_eval_report.md`：包含三张对比表格（Baseline-A vs Baseline-B vs Proposed）的分析报告。
3. 论文 `experiments.tex` 中代理评估表格的替换/补充说明。

---

## 五、当前阻塞项

- **Ollama 未安装**（`C:	rogram Filesollama.exe` 不存在）。
- **无本地量化模型文件**。

**下一步动作（需用户/其他 Agent 在合适时机执行）：**
1. 下载并安装 Ollama for Windows。
2. 执行 `ollama pull qwen2.5:7b`。
3. 运行本目录下的 `run_llm_eval.py` 脚本（待实现）。

---

## 六、脚本框架（`run_llm_eval.py`）

```python
#!/usr/bin/env python3
"""Local LLM evaluation script for agri-paper (requires Ollama)."""
import json
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

def generate_answer(query: str, context: str) -> str:
    prompt = f"You are an agricultural extension officer...\n\nQuestion: {query}\n\nContext: {context}\n"
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    })
    return resp.json()["response"]

# TODO: load benchmark, sample 80 records, generate for each condition, score, save.
```

（完整脚本将在 Ollama 就绪后编写并运行。）
