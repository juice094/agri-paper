# 文献矩阵：农业知识管理 Agent 系统（2021–2026）

> 检索范围：Web of Science、Scopus、arXiv、Google Scholar、中国知网预印本、农业工程学报、Frontiers 系列期刊、GitHub 技术仓库。
> 检索日期：2026-04-10

---

## 一、核心文献清单（30 篇）

### 方向 A：农业病虫害诊断 Agent / 专家系统（8 篇）

| # | 标题 | 作者 | 年份 | 来源 | 核心贡献 |
|---|------|------|------|------|----------|
| A1 | An Ontology-Based Expert System for Rice Disease Identification and Control Recommendation | Jearanaiwongkul et al. | 2021 | *Applied Sciences* | **RiceMan**：基于水稻病害本体（RiceDO）与 SWRL 规则推理， symptoms→disease 映射，可解释诊断。 |
| A2 | An Ontology-Based Agriculture Decision-Support System with an Evidence-Based Explanation Model | Alharbi et al. | 2024/25 | *Smart Agricultural Technology* | **AgrODSS**：植物病虫害本体 PDP-O + EBEM 解释模型，SPARQL 查询，专家评估准确率 **80.66%**。 |
| A3 | 基于大语言模型与知识图谱的水稻病虫害专家系统 | 上海海洋大学 | 2025 | *农业工程学报* | **AgenticGraphRAG**：ReAct + 双检索（向量+Cypher），LLM+KG 协同推理，准确率 **86%（人工）/ 89.33%（LLM）**。 |
| A4 | Chat Demeter: A Multi-Agent System for Plant Disease Diagnosis Integrating CNN-Transformer Models | Frontiers Team | 2025 | *Frontiers in Plant Science* | 四 Agent 协作（规划→推理→评估→可视化），CNN-Transformer，准确率 **99.50%**。 |
| A5 | Intelligent Agents System for Vegetable Plant Disease Detection Using MDTW-LSTM Model | Chelloug et al. | 2023 | Conf/Journal | 3D 转换 + DRL 多智能体框架，病害识别与严重程度量化。 |
| A6 | Knowledge-Based System for Crop Pests and Diseases Recognition | Rodríguez-García et al. | 2021 | *Electronics* | OWL 本体 + 专家规则整合，为后续 KG-LLM 奠定知识工程基础。 |
| A7 | 神农植保多模态大模型 1.0 | 产业报道 | 2024 | 中文核心/产业 | 覆盖 53 作物、347 病虫害，云端大模型 + 小程序，难以配置适配地方特有作物。 |
| A8 | 雄小农 AI 农业大模型 | 产业报道 | 2024 | 中文核心/产业 | DeepSeek 基座 + 农技 KG + 多模态引擎，Agent 行为与知识库结构固定。 |

### 方向 B：农业知识图谱与大语言模型（8 篇）

| # | 标题 | 作者 | 年份 | 来源 | 核心贡献 |
|---|------|------|------|------|----------|
| B1 | The Application Progress and Research Trends of KG and LLM in Agriculture | Gong & Li | 2025 | *Computers and Electronics in Agriculture* | 系统综述 KG-LLM **互补特性（KG-LLM-Mcom）**，指出 KG 构建成本高与 LLM 幻觉可协同解决。 |
| B2 | Implementation of LLMs and Agricultural KGs for Efficient Plant Disease Detection | Zhao et al. | 2024 | *Agriculture* | 验证 KG 在提升 LLM 事实准确性与领域相关性方面的有效性。 |
| B3 | Agricultural LLM Based on Precise Knowledge Retrieval and Knowledge Collaborative Generation (KGLLM) | Research Team | 2024 | *Smart Agriculture* | 信息熵过滤 + KG 显式约束解码，BertScore 平均提升 **9.84%**，显著降低幻觉。 |
| B4 | AgriGPT: A Large Language Model Ecosystem for Agriculture | Yang et al. | 2025 | arXiv:2508.08632 | **首个开源农业 LLM 生态**：Agri-342K 数据集、Tri-RAG、AgriBench-13K 评测基准。 |
| B4b | CPJ: Explainable Agricultural Pest Diagnosis via Caption-Prompt-Judge | Zhang et al. | 2025 | arXiv:2512.24947 | **训练无关的 LLM-as-a-Judge 评估流水线**：5 维度评分、Cohen's κ=0.88 人工验证协议。已注册到 devbase (`cpj_ref`)。 |
| B4c | Agri-CM³: A Chinese Massive Multi-modal, Multi-level Benchmark | Wang et al. | 2025 | ACL 2025 | **P-M-K 三级分层评估**：3,939 图像 + 15,901 MCQ，感知-认知-知识拆解。已注册到 devbase (`agricm3_ref`)。 |
| B4d | AgMMU: A Comprehensive Agricultural Multimodal Understanding Benchmark | Gauba et al. | 2025 | arXiv:2504.10568 | **真实对话蒸馏**：11.6 万 USDA 专家对话 → 746 MCQ/OEQ + 5.7 万知识事实。已注册到 devbase (`agmmu_ref`)。 |
| B5 | AgroLLM: Connecting Farmers and Agricultural Practices Through LLMs | Samuel et al. | 2025/26 | *AgriEngineering* | **RAG + DKPL**：从教材自动提取语义词汇、因果规则与约束库，准确率 **95.2%**。 |
| B6 | AgriBERT: Knowledge-Infused Agricultural Language Models | Rezayi et al. | 2022 | *IJCAI* | 农业领域语言模型先驱，通过领域语料预训练提升农业文本理解。 |
| B7 | The Role of Large Language Models in Modern Agriculture: A Review | (Various) | 2024 | *Agronomy* | 综述 LLM 在农业决策支持、知识问答、作物管理中的应用现状与挑战。 |
| B8 | Knowledge Graph Construction for Agriculture: Methods and Applications | (Various) | 2023 | *Information Processing in Agriculture* | 农业 KG 构建方法论，包括实体抽取、关系推理与图谱补全技术。 |

### 方向 C：MCP / 边缘计算 / 配置驱动架构（8 篇）

| # | 标题 | 作者 | 年份 | 来源 | 核心贡献 |
|---|------|------|------|------|----------|
| C1 | IoT-MCP: Bridging LLMs and IoT Systems Through MCP | IoT-MCP Team | 2025/26 | 预印本 | **三层 MCP 架构**（Local Host → Datapool & Connection Server → IoT Devices），标准化 JSON 命令控制边缘设备。 |
| C2 | IoT-Edge-MCP-Server: MCP Server for Industrial IoT, SCADA and PLC | Poly-MCP | 2025 | GitHub/白皮书 | 生产级 MCP Server，MQTT/Modbus 统一为 AI 可编排 API，支持时序存储与预测性维护。 |
| C3 | A Self-Organizing CPS for Sustainable Agriculture (AGRARIAN) | AGRARIAN Team | 2025 | *Springer* | **K3s + GitOps 声明式配置**，边缘节点动态服务编排与 AI 应用部署。 |
| C4 | A DSL Framework for Farm Management Information Systems in Precision Agriculture | Groeneveld et al. | 2021 | *Precision Agriculture* | **FMIS DSL**：Functionality/Sector/Configuration DSL 三层拆分，降低农民与工程师沟通成本。 |
| C5 | D4.4: Initial Agri-Food Data-Sharing Reference Architecture | Ploutos H2020 | 2021 | EU H2020 技术报告 | 语义 Web + 声明式元数据注册，PCSM 核心语义模型与 PIE 互操作框架。 |
| C6 | 边缘计算在智慧农业中的应用现状与展望 | 国内团队 | 2022/25 | *农业工程学报* | 云-雾-边三层架构，边缘 AI "模型前端化、轻量化"，呼吁统一通讯协议与数据命名规范。 |
| C7 | Model Context Protocol: Specification | Anthropic | 2024 | 官方规范 | MCP 协议标准文档，定义 tools/list、tools/call、Content-Length stdio 传输等规范。 |
| C8 | Local-First Software: You Own Your Data, in Spite of the Cloud | Kleppmann et al. | 2021 | *Ink & Switch* | 本地优先软件设计原则，强调离线可用、数据主权、端侧智能的架构哲学。 |

### 方向 D：Rust Agent 框架 / 开发者工具（6 篇/项目）

| # | 标题/项目 | 作者/维护方 | 年份 | 来源 | 核心贡献 |
|---|-----------|-------------|------|------|----------|
| D1 | **Clarity** (本地优先 Rust Agent 框架) | 本项目 | 2026 | GitHub | TUI + Subagent + Memory + MCP Client，本地优先的端到端 Agent 平台。 |
| D2 | **devbase** (开发者知识管理系统) | 本项目 | 2026 | GitHub | 本地仓库群扫描/健康/同步/查询，7 个 MCP 工具暴露给 Agent。 |
| D3 | **Rig** (Rust LLM 应用框架) | Playgrounds | 2025 | GitHub/crates.io | 强调规模化、WASM、向量存储集成，无原生 TUI/Subagent。 |
| D4 | **RusticAI** (PydanticAI-inspired Rust Agent) | mazdak | 2025 | GitHub | Agent 编排 + Realtime Voice + Deferred Tools，MCP Toolsets 集成。 |
| D5 | **ADK-Rust** (Model-Agnostic Agent Dev Kit) | zavora-ai | 2025 | GitHub | Voice Agent + 部署无关，模块化 but 无 TUI/Subagent 继承。 |
| D6 | Awesome MCP Servers | 社区 | 2025 | GitHub | MCP Server 生态 curated list，含 Filesystem/Git/Memory/Fetch 等参考实现。 |

---

## 二、方法对比矩阵（8 个代表性系统）

| 系统/框架 | 年份 | 架构通用性 | 本地优先/离线 | 配置驱动程度 | 数据集/指标 | 核心缺陷/Gap |
|-----------|------|------------|---------------|--------------|-------------|--------------|
| **RiceMan / AgrODSS** | 2021/24 | ⭐⭐☆☆☆ 低 | ⭐⭐⭐⭐☆ 高 | ⭐⭐⭐☆☆ 中 | 水稻领域本体 / 80.66% | 跨作物迁移需重写 OWL/SWRL 本体 |
| **AgenticGraphRAG** | 2025 | ⭐⭐⭐☆☆ 中 | ⭐⭐☆☆☆ 低 | ⭐⭐☆☆☆ 低 | 水稻症状数据集 / 86-89% | Prompt、检索模块围绕水稻硬编码 |
| **Chat Demeter** | 2025 | ⭐⭐☆☆☆ 低 | ⭐⭐⭐☆☆ 中 | ⭐⭐☆☆☆ 低 | 植物叶片图像 / 99.5% | CNN-Transformer 与 Agent 流程高度定制 |
| **AgriGPT + Tri-RAG** | 2025 | ⭐⭐⭐⭐☆ 较高 | ⭐⭐☆☆☆ 低 | ⭐⭐⭐☆☆ 中 | AgriBench-13K / 开源 | 核心模型与 RAG 流水线仍需大量领域工程 |
| **CPJ** | 2025 | ⭐⭐⭐☆☆ 中 | ⭐⭐⭐⭐☆ 高* | ⭐⭐⭐⭐☆ 较高 | CDDMBench / 开源 | *训练无关，评估协议可直接本地化复用 |
| **Agri-CM³** | 2025 | ⭐⭐⭐⭐☆ 较高 | ⭐⭐⭐☆☆ 中 | ⭐⭐⭐☆☆ 中 | 15,901 MCQ / 开源 | 中文为主，P-M-K 分层框架具有通用借鉴价值 |
| **AgMMU** | 2025 | ⭐⭐⭐⭐☆ 较高 | ⭐⭐☆☆☆ 低 | ⭐⭐⭐☆☆ 中 | 746 QA + 57K facts / 开源 | 数据蒸馏方法对 USDA IPM 扩展有直接参考意义 |
| **AgroLLM (RAG+DKPL)** | 2025 | ⭐⭐⭐☆☆ 中 | ⭐⭐⭐☆☆ 中 | ⭐⭐⭐⭐☆ 较高 | 农业教材 / 95.2% | DKPL 约束提取器与教材结构强耦合 |
| **IoT-MCP / IoT-Edge-MCP** | 2025 | ⭐⭐⭐⭐⭐ 高 | ⭐⭐⭐⭐☆ 高 | ⭐⭐⭐⭐⭐ 高 | 工业/边缘场景 | 农业垂直领域的工具注册规范仍空白 |
| **AGRARIAN (K3s+GitOps)** | 2025 | ⭐⭐⭐⭐☆ 较高 | ⭐⭐⭐⭐⭐ 很高 | ⭐⭐⭐⭐⭐ 高 | 农业 CPS | 农艺模型仍需单独开发容器镜像 |
| **Clarity + devbase** | 2026 | ⭐⭐⭐⭐⭐ 高* | ⭐⭐⭐⭐⭐ 高* | ⭐⭐⭐⭐⭐ 高* | 本研究验证中 | *本文研究对象，待验证 |

**维度说明**：
- **架构通用性**：能否通过最小改动迁移到其他农业子领域。
- **本地优先/离线**：是否支持边缘设备独立运行、无需持续云连接。
- **配置驱动程度**：农业业务逻辑是通过外部配置文件动态加载，还是硬编码在代码/模型权重中。

---

## 三、识别的 3 个关键 Gap

### Gap 1：硬编码农业逻辑 vs 通用框架配置适配之间的鸿沟
**现状**：无论是传统本体专家系统（RiceMan、AgrODSS）还是最新 LLM+KG 框架（AgenticGraphRAG、Chat Demeter），其农业知识抽取 Prompt、Agent 工具调用链、诊断规则与作物参数均**针对单一作物或特定场景手工设计**。  
**问题**：当需要将这些系统从"水稻病虫害"迁移到"小麦病害"或"果树虫害"时，开发者往往需要重写本体、重训模型、重构 Agent 任务拆解逻辑——**缺乏一种"通过声明式配置即可适配新作物/新病害"的通用农业 Agent 框架**。  
**我们的改进**：基于 **MCP 协议**与 **TOML 配置系统**，将作物知识库、诊断工具、执行器接口抽象为可热插拔的配置模块，实现"同一 Agent 内核 + 不同农艺配置包"的跨领域快速部署。

### Gap 2：MCP 协议在农业垂直领域的适配标准与实践空白
**现状**：MCP 在工业物联网、智能家居等领域已有较成熟 Server 实现（IoT-Edge-MCP、EMQX MCP），但农业场景中传感器协议（LoRaWAN、Zigbee、NB-IoT）、农艺知识图谱接口、无人机/农机执行器控制的异构性远高于工业场景。  
**问题**：目前**尚无农业专用的 MCP 工具注册规范、农艺上下文交换格式（Context Schema）以及边缘安全访问标准**，导致农业 LLM Agent 与物理设备的对接仍停留在"定制化 API 集成"阶段。  
**我们的改进**：提出面向农业知识管理的 **Agri-MCP 工具 Schema 草案**（基于 devbase 的 7 个工具扩展），定义病虫害诊断结果、防治建议、知识库查询的标准化 JSON Schema。

### Gap 3：配置驱动的边缘 Agent 系统缺失
**现状**：现有农业 Agent 系统（AgenticGraphRAG、Chat Demeter、神农植保）主要运行在云端，依赖大模型 API 在线推理；边缘侧虽有不少轻量化 CNN 模型，但多为**单一功能的"模型推理盒子"**，缺乏具备任务规划、知识检索、多工具调用能力的完整 Agent。  
**问题**：农村网络基础设施不稳定，农民对数据隐私和实时性要求高，但**目前缺乏一种"通过 YAML/TOML 声明式配置即可动态加载本地农艺知识、调整诊断 Agent 行为、并在离线/在线混合模式下运行"的本地优先 Agent 架构**。  
**我们的改进**：验证 Clarity（本地优先 TUI Agent）+ devbase（本地知识库 MCP Server）的组合，支持通过 `.clarity.toml` 配置文件动态切换：① 本地知识库路径；② 可用的工具集合；③ Agent 人格与系统提示词。

---

## 四、可借鉴点汇总

| 来源 | 可借鉴点 | 在本研究中的应用 |
|------|----------|------------------|
| AgenticGraphRAG (A3) | ReAct + 双检索（向量+图谱） | 农业诊断 Agent 的推理模式设计参考 |
| AgroLLM (B5) | 领域约束 RAG（DKPL） | 配置文件中 `domain.constraints` 字段的设计灵感 |
| **CPJ (B4b)** | LLM-as-a-Judge 5 维度评分 | `eval.rs` 评分维度从 3 维扩展为 5 维的直接依据 |
| **Agri-CM³ (B4c)** | P-M-K 三级分层评估 | 将单一 benchmark 升级为分层推理测试的设计依据 |
| **AgMMU (B4d)** | USDA 真实对话蒸馏 | `kb_expansion_plan.md` 中 USDA IPM 扩展的数据构造参考 |
| IoT-MCP (C1) | 三层 MCP 架构 | 本文 Clarity→devbase→syncthing/git 三层架构的理论支撑 |
| AGRARIAN (C3) | K3s + GitOps 声明式配置 | "配置即代码"在农业分布式环境中的可复现性论证 |
| Groeneveld DSL (C4) | FMIS DSL 三层拆分 | Profile 配置中 `persona`/`tools`/`domain` 的分层设计参考 |
