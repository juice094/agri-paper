# Ollama 就绪后操作清单（agri-paper）

**当前状态：** Ollama 未安装，阻塞 agri-paper 的 LLM 评估和知识库扩展。
**本清单目标：** 一旦 Ollama 安装完成，按顺序执行以下步骤即可推进项目。

---

## Step 1：安装并验证 Ollama（约 10 分钟）

```powershell
# 1. 下载安装
# 访问 https://ollama.com/download/windows 下载安装包并运行

# 2. 拉取模型
ollama pull qwen2.5:7b

# 3. 验证服务
ollama list
# 应显示 qwen2.5:7b

# 4. 测试生成
ollama run qwen2.5:7b "Say hello"
```

---

## Step 2：运行真实 LLM 生成评估（约 30–60 分钟）

评估脚本已准备就绪：

```powershell
cd C:\Users\22414\Desktop\agri-paper
python w4\research\run_llm_eval.py
```

**脚本会自动做：**
- 检查 Ollama 可用性和模型存在性
- 从 210 条 benchmark 中 stratified 采样 80 条（easy 30 + medium 30 + hard 20）
- 对每条查询在 3 种检索条件下分别调用本地 LLM：
  - Baseline-A：无检索上下文
  - Baseline-B：仅作物过滤（该作物全部 3 条记录）
  - Proposed：symptom-level 排序后的 top-1 记录
- 自动评分（诊断正确性 / 治疗完整性 / 安全性黑名单筛查）
- 输出：
  - `w4/research/llm_eval_results_YYYYMMDD_HHMMSS.json`（汇总统计）
  - `w4/research/llm_eval_raw_YYYYMMDD_HHMMSS.jsonl`（原始生成结果）

**Step 2 完成后：** 将汇总结果更新到 `w4/arxiv/experiments.tex` 和 `w4/writer/experiments.tex` 中，替换/补充现有的代理评估表格。

---

## Step 3：评估结果回写论文（约 20 分钟）

编辑以下文件（两处内容一致）：
- `w4/arxiv/experiments.tex`
- `w4/writer/experiments.tex`

**需要修改的位置：**
1. 在 "Proxy Evaluation" 小节前添加一段过渡：
   > "To validate the simulated projections reported above, we conducted a real local-LLM evaluation using Ollama with Qwen2.5-7B..."
2. 新增一个表格 `tab:llm_eval_results`，展示 Baseline-A / Baseline-B / Proposed 的实测均值。
3. 在 Limitations 中移除或弱化 "no live LLM was invoked" 的表述，改为说明本地模型的局限性（量化、7B 规模、无多模态）。

---

## Step 4：启动知识库扩展（并行进行，约 2–3 天）

### 4.1 爬取 USDA IPM Crop Profiles

```powershell
cd C:\Users\22414\Desktop\agri-paper
# 待编写脚本（可参考 kb_expansion_plan.md）
python w4\research\ipm_crawler.py
```

该脚本需：
- 从 https://ipmdata.ipmcenters.org/ 下载目标作物的 Crop Profile PDF
- 使用 `pdfplumber` 提取文本
- 使用本地 Qwen2.5-7B 将段落结构化为 JSONL：
  ```json
  {"crop": "Corn", "disease": "European Corn Borer", "symptoms": "...", "treatment": "..."}
  ```

### 4.2 申请 AI-AgriBench 数据（可与 4.1 并行）

- 访问 https://aiagribench.org
- 填写测试集申请表
- 所需信息草稿已准备于 `w4/research/ai_agribench_request.md`
- 收到数据后运行转换脚本并入 `agricultural_diseases_all.jsonl`

### 4.3 质量过滤与重新生成 benchmark

- 去重（按 `crop + disease`）
- 人工抽查 50 条
- 运行 `datasets/generate_benchmark.py` 和 `w4/research/merge_benchmark.py` 重新生成 210+ 条 QA

---

## Step 5：重新编译 arXiv 投稿包（约 10 分钟，需有 LaTeX 的机器）

Windows 环境缺少 LaTeX 编译器。请在具备 MiKTeX/TeX Live 的机器上执行：

```bash
cd w4/arxiv
pdflatex main_arxiv.tex
bibtex main_arxiv
pdflatex main_arxiv.tex
pdflatex main_arxiv.tex
```

验证：
- PDF 页数合理（约 14–16 页）
- 引用格式正确（ numbered [1], [2]...）
- 图片/表格未溢出

然后重新打包：
```bash
zip arxiv_upload.zip main_arxiv.tex *.tex *.bib
# 或按 arXiv 官方要求打包 source tarball
```

详细编译指南见 `w4/research/arxiv_compile_instructions.md`。

---

## 阻塞解除优先级

| 阻塞项 | 影响 | 解除后最大收益 |
|--------|------|----------------|
| Ollama 安装 | 高 | Step 2（LLM 评估）和 Step 4.1（PDF 结构化）同时解锁 |
| AI-AgriBench 数据获批 | 中 | Step 4.2 解锁，知识库规模大幅提升 |
| GitHub SSL 修复 | 低-中 | 方便自动化下载公开数据集和工具 |

---

*最后更新：2026-04-15*
