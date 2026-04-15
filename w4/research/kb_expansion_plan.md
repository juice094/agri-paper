# 知识库规模扩大方案（预备文档）

**当前状态：** 30 条种子记录（10 种作物 × 3 种病害）  
**目标状态：** 500+ 条结构化记录，覆盖 50+ 种作物和 200+ 种病害/害虫  
**策略：** 优先利用公开数据集和可爬取的政府/学术资源，避免版权风险。

---

## 一、数据源评估

### 1.1 AI-AgriBench（伊利诺伊大学 AIFARMS）

| 属性 | 评估 |
|------|------|
| **规模** | 416 条专家标注 QA 对（主 leaderboard）；Smallholders Leaderboard 有约 3100 条（IFPRI/Digital Green/PxD） |
| **可获取性** | 测试集问题需通过官网表单申请；GitHub 仓库 `AIFARMS/AI-AgriBench` 可能包含预处理脚本和示例数据 |
| **适用性** | ⭐⭐⭐⭐⭐ 极高。问题为真实农民视角，答案来自 extension 文档，格式与本项目知识库需求一致。 |
| **风险** | 完整测试集保密；需遵守其使用协议（商业用途需授权）。 |
| **建议操作** | 访问 [aiagribench.org](https://aiagribench.org) 申请测试集问题 JSON；将答案结构化为本地 `crop-disease-symptom-treatment` 格式。 |

### 1.2 USDA National IPM Database（ipmdata.ipmcenters.org）

| 属性 | 评估 |
|------|------|
| **规模** | 706 份 Crop Profiles + 171 份 PMSPs，覆盖美国各州主要作物 |
| **可获取性** | 网页可浏览，PDF 可下载，无明确下载限制 |
| **适用性** | ⭐⭐⭐⭐☆ 高。内容权威，包含症状、防治措施、农药信息。但格式为自由文本 PDF，需要爬取和结构化提取。 |
| **风险** | 美国政府公共领域作品，版权风险极低。 |
| **建议操作** | 使用 `requests` + `pdfplumber` 批量下载并提取文本；用 LLM（本地小模型或 API）将段落结构化为 JSONL 记录。 |

### 1.3 UC IPM（ University of California）

| 属性 | 评估 |
|------|------|
| **网址** | https://ipm.ucanr.edu |
| **规模** | 数十种作物，每种作物包含多个害虫/病害/杂草的详细管理指南 |
| **可获取性** | 网页结构化较好，部分有独立页面 |
| **适用性** | ⭐⭐⭐⭐☆ 高。内容详尽，适合 California 农业，但对其他地区作物覆盖有限。 |
| **建议操作** | 爬取特定作物的 Pest Management 页面，提取害虫名称、症状描述和防治建议。 |

### 1.4 PlantVillage / APS Image Database

| 属性 | 评估 |
|------|------|
| **规模** | 数千张植物病害图片，部分附带元数据 |
| **可获取性** | PlantVillage 数据集在 Kaggle/GitHub 上公开；APS 图片库部分需订阅 |
| **适用性** | ⭐⭐⭐☆☆ 中等。主要是图像数据，文本描述较少，但可从 `readme` 和论文中提取病害名称和症状。 |
| **建议操作** | 下载 PlantVillage 元数据 CSV，提取作物-病害映射，作为扩展记录的种子。 |

### 1.5 中文数据源：国家农业科学数据共享中心 / 知网硕博论文

| 属性 | 评估 |
|------|------|
| **规模** | 大量中文农业技术文献 |
| **可获取性** | 知网需付费/校园网；国家农业数据中心部分开放 |
| **适用性** | ⭐⭐⭐☆☆ 中等。内容质量高但结构化困难，且存在版权问题。 |
| **建议操作** | 作为远期补充，短期内优先使用英文公开数据源。 |

---

## 二、推荐执行路径（分阶段）

### Phase 1：接入 AI-AgriBench（1–2 天）
- 申请并下载 AI-AgriBench 的问题/答案数据。
- 编写转换脚本，将其格式化为 `crop-disease-symptom-treatment` JSONL。
- **预期增量**：+400 条 QA 对，约 100+ 条可转换为知识库记录（去重后）。

### Phase 2：爬取 USDA IPM Crop Profiles（2–3 天）
- 筛选 20–30 种主要作物（rice, wheat, corn, soybean, cotton, tomato, potato, citrus, apple, peanut, sorghum, barley, lettuce, strawberry 等）。
- 爬取对应州的 Crop Profile PDF。
- 使用 `pdfplumber` 提取文本，再用 LLM（本地 Qwen2.5-7B）做段落级结构化：
  ```json
  {"crop": "Corn", "disease": "European Corn Borer", "symptoms": "...", "treatment": "..."}
  ```
- **预期增量**：+300–500 条记录。

### Phase 3：质量过滤与去重（1 天）
- 按 `crop + disease` 去重。
- 人工抽查 50 条记录的准确性。
- 合并进 `agricultural_diseases_all.jsonl`，重新生成 benchmark。

---

## 三、工具链准备

| 工具 | 用途 | 安装状态 |
|------|------|----------|
| `requests` + `BeautifulSoup` | 网页爬取 | ✅ 已安装 |
| `pdfplumber` | PDF 文本/表格提取 | ✅ 已安装 |
| `ollama` + `qwen2.5:7b` | 本地 LLM 结构化抽取 | ❌ 未安装（阻塞） |
| `pandas` | 数据清洗与去重 | ✅ 已安装 |

---

## 四、当前阻塞项

1. **Ollama 未安装**：无论是 LLM 评估还是 PDF 结构化抽取，都需要本地运行 Qwen2.5-7B。
2. **AI-AgriBench 数据需申请**：需要填写官网表单获取测试集 JSON。
3. **网络环境限制**：GitHub SSL 证书验证失败，可能阻碍自动化下载和 API 调用。

---

## 五、下一步动作

1. **用户侧/其他 Agent**：安装 Ollama 并拉取 `qwen2.5:7b`。
2. **agri-paper 窗口**：在 Ollama 就绪后，优先实现 `run_llm_eval.py` 和 `ipm_crawler.py`。
3. **交叉协调**：由处理 devbase 的 Agent 或用户本人填写 AI-AgriBench 数据申请。
