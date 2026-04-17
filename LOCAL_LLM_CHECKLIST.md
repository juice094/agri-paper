# 本地 LLM 就绪后操作清单（agri-paper）

**当前状态：** 14B 本地模型已可用并验证功能正确，但速度不足以支撑 80 条 benchmark；7B 模型下载因 Windows SSL 证书吊销检查失败而阻塞。RAG 耦合与 eval 二进制已完成。  
**本清单目标：** 一旦本地模型就绪，按顺序执行以下步骤即可推进项目。  
**支持两条路径：**
- **Path A: Ollama** — 传统方案，服务化 REST API。
- **Path B: kalosm (Rust-native)** — 纯 Rust 方案，基于 Candle，无需额外守护进程。

---

## Step 1：安装并验证本地模型（约 10–30 分钟）

### Path A — Ollama

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

### Path B — kalosm（纯 Rust，已验证编译）

#### CPU 模式（默认，零配置）

```powershell
cd C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc

# 编译验证
cargo check

# 运行（debug 模式在 CPU 上极慢，评估建议加 --release）
cargo run
```

#### GPU 模式（CUDA，推荐）

**环境前提：**
- NVIDIA 驱动已装（`nvidia-smi` 正常）
- **CUDA 12.6 Toolkit** 已装到 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6`
- **Visual Studio Build Tools** 已装（提供 `cl.exe`）
- `kalosm` 的 `cuda` feature 已开启（见 `Cargo.toml`）

**由于 cudarc 0.13.9 编译时需要 cuDNN 头文件，但 cuDNN 未单独安装，项目中已使用一个空的 `cudnn.h` stub 绕过编译期检查。该 workaround 对 Transformer LLM 推理是安全的（不调用 cuDNN API）。**

**运行命令：**

```powershell
cd C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc

# 设置 CUDA 12.6 环境（若系统 PATH 已包含 12.6 和 MSVC，可省略）
$env:CUDA_ROOT = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6"
$env:CUDA_PATH = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6"
$env:CUDNN_LIB = "C:\Users\22414\cudnn_stub"
$env:PATH = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin;" + $env:PATH

# 编译（首次开启 cuda feature 需要 1–3 分钟编译 CUDA kernels）
cargo check

# 运行（首次会自动下载 ~4.5 GB GGUF；GPU 上 7B Q4 单条约几秒到十几秒）
cargo run --release
```

> **注意：** 由于 Windows SSL 证书吊销检查问题，Path B 首次 `cargo run` 自动从 HuggingFace 下载约 4–5 GB 的 GGUF 文件可能会失败。建议手动下载 `.gguf` 文件并放置到 `C:\Users\22414\Desktop\model\`；代码会自动检测本地 7B/14B 模型文件并优先加载。

---

## Step 2：运行真实 LLM 生成评估（约 30–60 分钟）

评估二进制已准备就绪：

```powershell
cd C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc

# 确保 7B 模型已放置到本地模型目录后运行
cargo run --bin eval --release
```

**eval 会自动做：**
- 加载本地检测到的模型（优先 7B，回退 14B）
- 从 210 条 benchmark 中 stratified 采样 80 条（easy 30 + medium 30 + hard 20）
- 对每条查询在 3 种检索条件下分别调用本地 LLM：
  - Baseline-A：无检索上下文
  - Baseline-B：仅作物过滤（该作物全部记录）
  - Proposed：基于关键词重叠的 top-1 RAG 记录
- 输出：
  - `llm_eval_raw_<condition>_<timestamp>.jsonl`（原始生成结果）
  - `llm_eval_summary_<timestamp>.json`（汇总统计）

**Step 2 完成后：** 将汇总结果更新到 `w4/arxiv/experiments.tex` 和 `w4/writer/experiments.tex` 中，替换/补充现有的代理评估表格。

---

## Step 3：评估结果回写论文（约 20 分钟）

编辑以下文件（两处内容一致）：
- `w4/arxiv/experiments.tex`
- `w4/writer/experiments.tex`

**需要修改的位置：**
1. 在 "Proxy Evaluation" 小节前添加一段过渡：
   > "To validate the simulated projections reported above, we conducted a real local-LLM evaluation using Qwen2.5-7B..."
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
| 7B 模型手动下载完成 | 高 | Step 2（LLM 评估）和 Step 4.1（PDF 结构化）同时解锁 |
| AI-AgriBench 数据获批 | 中 | Step 4.2 解锁，知识库规模大幅提升 |
| GitHub SSL 修复 | 低-中 | 方便自动化下载公开数据集和工具 |

---

*最后更新：2026-04-15*
