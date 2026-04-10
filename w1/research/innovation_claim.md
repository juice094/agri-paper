# 创新点陈述（Innovation Claim）

> 本文件用于论文核心贡献的反向验证。每个 Claim 必须可证伪（falsifiable）。

---

## 主 Claim

**提出的 Clarity+devbase 配置驱动农业 Agent 架构能够在零代码修改的前提下，通过 TOML 配置文件实现从通用开发助手到农业知识管理专家的领域迁移。**

---

## 支撑点与可证伪标准

### 支撑点 1：MCP 协议作为跨领域抽象层的有效性
**Claim**：Clarity 的 `StdioMcpClient` 可以正确地与 devbase 的 MCP Server 进行完整的 JSON-RPC 2.0 通信（initialize → tools/list → tools/call）。

**证伪条件**：
- 集成测试中 `initialize` 请求失败，或返回的 `protocolVersion` 不是 `"2024-11-05"`
- `tools/list` 无法返回 7 个 devbase 工具（devkit_scan/health/sync/query/index/note/digest）
- `tools/call` 调用 `devkit_health` 或 `devkit_query` 返回 `success: false`

**验证状态**：✅ **已通过**（见 `clarity-core/tests/mcp_devbase_integration.rs`，4/4 测试通过，2026-04-10）

---

### 支撑点 2：农业领域可通过声明式配置注入，无需修改 Rust 源码
**Claim**：用户仅需修改 `.clarity.toml` 中的 `persona.system_prompt`、`tools.enabled` 和新增的 `domain` 字段，即可让同一 Clarity Agent 内核具备农业知识管理能力。

**证伪条件**：
- 新增一种作物类型（如"柑橘"）需要修改 `.rs` 源文件
- 农业诊断流程需要硬编码在 Clarity 的 ReAct 循环中
- 配置文件变更后需要重新编译才能生效

**验证状态**：⏳ **待 W2 验证**（需扩展 `Config` 结构体支持 `domain` 字段，并编写零代码迁移演示）

---

### 支撑点 3：本地优先架构在农业场景中的可用性
**Claim**：基于 Clarity+devbase 的系统可以在无公网连接的环境下，通过本地 LLM（Ollama）或本地知识库完成农业病虫害诊断与防治建议查询。

**证伪条件**：
- 系统在无网络环境下无法启动或报错
- 本地知识库查询延迟 > 5 秒（单节点、本地 SQLite）
- 农业诊断准确率显著低于云端基线（>10% 差距）

**验证状态**：⏳ **待 W3-W4 验证**（需构建农业测试数据集并跑通端到端诊断任务）

---

## 反向验证（Red Team）

| 反驳点 | 回应策略 | 实验/写作安排 |
--------|----------|---------------|
| "这只是一个 MCP Client 联调 demo，没有农业领域特异性。" | 强调方法论贡献：将**通用软件工程架构**通过**配置**适配到农业场景，本身就是对"硬编码农业系统"范式的突破。 | Methodology 章节详细对比传统农业专家系统的实现方式。 |
| "没有真实农民使用，没有田间验证。" | 明确论文边界：本研究是**软件架构验证**（Architecture Validation），而非**田野应用研究**（Field Study）。田间部署是未来工作。 | Introduction 中明确声明验证范围为"桌面端知识管理闭环"。 |
| "农业诊断准确率不如专门的农业大模型（如神农植保）。" | 承认性能差距，但指出我们的目标是**可配置性**和**本地优先**，而非 SOTA 准确率。论文中应诚实报告准确率数据。 | Experiments 章节包含与神农植保等系统的准确率对比，并讨论 Trade-off。 |
| "syncthing-rust 的 Push 未实现，分布式同步不完整。" | 将 syncthing-rust 从本研究验证范围中**明确排除**，三层架构仅验证 Clarity+devbase 两层。 | Related Work 中说明 syncthing 作为"架构预留层"，本研究不做端到端验证。 |

---

## 与现有研究的区分度总结

| 维度 | 现有研究（如 AgenticGraphRAG、Chat Demeter） | 本研究 |
|------|-----------------------------------------------|--------|
| **核心对象** | 农业 AI 模型/算法 | 通用 Agent 框架的农业适应性 |
| **实现方式** | 硬编码农业逻辑 | 声明式配置驱动 |
| **部署形态** | 云端 API / 小程序 | 本地优先 TUI + 本地知识库 |
| **迁移成本** | 高（换作物需改代码/重训模型） | 低（换作物仅需改 TOML） |
| **协议标准** | 定制化 API | 标准化 MCP |
| **验证指标** | 准确率、AUC | 配置迁移时间、工具调用成功率、响应延迟 |
