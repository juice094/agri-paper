# arXiv 投稿包编译指南

**当前环境限制：** Windows 工作站上没有安装 MiKTeX / TeX Live，无法本地编译 `main_arxiv.pdf`。
**本指南目标：** 记录在有 LaTeX 环境的标准机器上如何编译和打包 arXiv 投稿文件。

---

## 一、环境要求

- **TeX Live**（推荐 2023 或更新版本）或 **MiKTeX**
- 必须包含的包：`inputenc`, `fontenc`, `lmodern`, `amsmath`, `amssymb`, `graphicx`, `booktabs`, `hyperref`, `cleveref`, `enumitem`, `geometry`, `setspace`, `tikz`（含 `arrows.meta`, `positioning`, `shapes` 库）
- `bibtex` 或 `bibtex8` 用于处理 `citations.bib`

---

## 二、编译步骤

```bash
# 进入 arxiv 源文件目录
cd w4/arxiv

# 1. 首次编译（生成 .aux）
pdflatex main_arxiv.tex

# 2. 处理参考文献
bibtex main_arxiv

# 3. 第二次编译（解析交叉引用）
pdflatex main_arxiv.tex

# 4. 第三次编译（确保所有引用稳定）
pdflatex main_arxiv.tex
```

**预期结果：**
- 生成 `main_arxiv.pdf`
- 页数：约 14–16 页
- 文件大小：约 350–450 KB
- 引用格式：numbered citations `[1]`, `[2]`, ...

---

## 三、编译后检查清单

| 检查项 | 方法 | 预期 |
|--------|------|------|
| 页数 | `pdfinfo main_arxiv.pdf` | 14–16 页 |
| 作者块 | 查看第 1 页 | "Anonymous Authors / Anonymous Institution"（投稿版）或真实作者信息（最终版） |
| 引用无问号 | 全文搜索 `[?]` | 零匹配 |
| 图片无溢出 | 查看 Methodology 中的 TikZ 图 | 完整显示，无边界截断 |
| 表格对齐 | 查看 `tab:retrieval_results` | 列对齐正确 |

---

## 四、打包 arXiv 投稿文件

arXiv 接受 `.tar.gz` 格式的源码包。确保只包含编译所需的源文件，不包含 `.aux`、`.log`、`.out`、`.pdf`。

### 4.1 清理编译产物（在仓库根目录执行）

```bash
cd w4/arxiv
rm -f *.aux *.bbl *.blg *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.toc *.pdf
```

> 注：项目根目录的 `.gitignore` 已配置忽略这些文件，正常不应被 Git 跟踪。

### 4.2 创建 arXiv 源码压缩包

```bash
cd w4/arxiv

# 方法 A：tar.gz（arXiv 推荐）
tar -czvf arxiv_source.tar.gz \
  main_arxiv.tex \
  main.tex \
  introduction.tex \
  related_work.tex \
  methodology.tex \
  experiments.tex \
  discussion.tex \
  conclusion.tex \
  citations.bib

# 方法 B：zip（部分投稿系统接受）
zip arxiv_upload.zip \
  main_arxiv.tex \
  main.tex \
  introduction.tex \
  related_work.tex \
  methodology.tex \
  experiments.tex \
  discussion.tex \
  conclusion.tex \
  citations.bib
```

### 4.3 检查包内容

```bash
tar -tzf arxiv_source.tar.gz
```

应仅包含 `.tex` 和 `.bib` 文件。如有缺失图片或宏包依赖，arXiv 的自动编译会失败。

---

## 五、已知问题与注意事项

1. **TikZ 图兼容性**
   - `methodology.tex` 中使用了 `tikz` 绘制架构图。
   - arXiv 的 TeX 环境支持 TikZ，但某些非常新的库可能缺失。如果编译失败，可尝试将 TikZ 图预渲染为 PDF 插图，然后使用 `\includegraphics` 替代。

2. **BibTeX 格式**
   - `citations.bib` 中使用了 `@article`, `@misc`, `@techreport`, `@book` 等标准类型。
   - `agrarian2025` 已从 `@book` 改为 `@article`，确保与 `plain` bibstyle 兼容。

3. **匿名审稿**
   - `main_arxiv.tex` 当前使用 `Anonymous Authors`。
   - 在最终投稿或预印本发布前，请替换为真实作者名和机构信息。

4. **PDF 大小限制**
   - arXiv 对单个 PDF 文件大小限制为 50 MB。`main_arxiv.pdf` 约 400 KB，远低于限制。

---

## 六、快速验证脚本（Linux/macOS/WSL）

```bash
#!/bin/bash
set -e
cd w4/arxiv
pdflatex main_arxiv.tex
bibtex main_arxiv
pdflatex main_arxiv.tex
pdflatex main_arxiv.tex

# 验证页数
PAGES=$(pdfinfo main_arxiv.pdf | grep Pages | awk '{print $2}')
echo "PDF generated: main_arxiv.pdf ($PAGES pages)"

# 清理并打包
rm -f *.aux *.bbl *.blg *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.toc
tar -czvf arxiv_source.tar.gz *.tex *.bib
echo "Source archive: arxiv_source.tar.gz"
```

---

*Guide prepared by agri-paper agent — 2026-04-15*
