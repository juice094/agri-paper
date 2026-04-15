# AI-AgriBench 数据申请表草稿

**状态：** 待提交（需用户手动访问 https://aiagribench.org 填写表单）

---

## 一、项目基本信息

| 字段 | 建议填写内容 |
|------|-------------|
| **Project / Institution Name** | `agri-paper` (Local-First Agricultural Agent Architecture Research) |
| **Primary Contact Email** | 用户自己的邮箱 |
| **Country / Region** | China |
| **Intended Use** | Academic research and prototype validation. We are evaluating a local-first, configuration-driven agent architecture for agricultural knowledge retrieval. The AI-AgriBench dataset will be used as an external validation source to benchmark retrieval-augmented generation (RAG) quality against our local knowledge base. |
| **Will results be published?** | Yes, intended for arXiv preprint and potentially a peer-reviewed venue after further validation. |
| **Commercial use?** | No. This is a non-commercial research prototype. |

---

## 二、数据使用声明（可直接复制到表单的 free-text 框）

```
We request access to the AI-AgriBench test-set questions for the purpose of benchmarking a local-first agricultural advisory system.

Our system couples a Rust-based agent framework (Clarity) with a local SQLite knowledge-base backend (devbase) via the Model Context Protocol (MCP). We aim to compare our retrieval-augmented generation pipeline against the AI-AgriBench ground-truth answers to measure:
1. Diagnosis correctness on fine-grained agricultural symptoms.
2. Treatment completeness relative to expert-curated recommendations.
3. Safety adequacy of generated advice under fully offline conditions.

The evaluation is strictly non-commercial and for academic research. Any published results will cite the AI-AgriBench consortium and acknowledge the dataset source.
```

---

## 三、技术背景（如表单要求补充）

**System description:**
- Framework: Rust-native agent kernel with MCP stdio transport
- Knowledge base: Local SQLite + JSONL crop-disease records
- LLM backend: Local quantized model (Qwen2.5-7B via Ollama)
- Transport: Offline, no cloud API dependency

**Why AI-AgriBench:**
- It provides farmer-oriented questions grounded in real extension documents.
- It allows us to test generalization beyond our small synthetic seed knowledge base.
- It serves as an independent, third-party benchmark for our RAG retrieval quality.

---

## 四、提交后的下一步

1. **等待邮件回复**：通常 1–3 个工作日。
2. **收到 JSON 后**：运行转换脚本将其并入本地知识库格式。
3. **本地评估**：使用 `run_llm_eval.py` 对 AI-AgriBench 子集进行生成评估。
4. **结果反馈**：如项目方要求，可自愿提交 leaderboard 结果。

---

## 五、注意事项

- AI-AgriBench 的 **测试集 ground-truth 是保密的**，请勿将其答案上传到任何公开仓库。
- 收到的问题 JSON 仅包含 `qna_id`、`question`、`crop_group`、`topic_categories` 等字段，**不包含答案**。
- 评估需由用户自己的模型生成回答后，按官方格式提交给 AI-AgriBench 团队评分。

---

*Draft prepared by agri-paper agent — 2026-04-15*
