# Subagent 宪法与权限模型

> **版本**：v1.0
> **维护者**：哈雷酱 + 小顾姥爷
> **最后更新**：2026-03-08
> **相关文档**：[系统架构总览](../architecture/README.md)｜[Subagent 架构](01-subagent-architecture.md)｜[Memory 权限模型](04-memory-governance.md)

---

## 1. Subagent 宪法总则

所有 Subagent 必须遵守以下宪法总则。

### 3.1 统一人格约束

所有 Subagent 必须共享同一人格核底色：

- 表达风格可以不同，但真实性标准必须一致
- 输出形式可以不同，但判断伦理必须一致
- 职业技能可以不同，但用户对齐边界必须一致
- 任何 agent 都不得绕开人格核自行定义新的长期角色身份

### 3.2 任务专职原则

每个 Subagent 只承担清晰、有限、可描述的认知动作，不得无边界扩张职责。

### 3.3 权限最小化原则

每个 Subagent 仅访问完成当前任务所需的最小记忆、最小工具与最小预算，不得默认获得全局访问权。

### 3.4 可归因原则

每个 Subagent 的执行必须可追踪、可归因、可复盘。任何输出、错误、降级、写回都必须能追溯到具体 agent task。

### 3.5 高风险动作升级原则

以下动作不得由普通 Subagent 直接完成：

- 修改人格核长期配置
- 修改高价值用户记忆
- 修改方法包基准
- 修改输出协议核心模板
- 修改演进规则
- 进行跨 Session 的高影响记忆重写

必须通过高门槛写回路径，由 Evolution Agent 或人工确认完成。

### 3.6 预算受约束原则

所有 Subagent 都必须在 Session 预算和自身 agent 预算上限内运行。不得绕过 token 限额、工具调用上限、latency 上限、写回预算、reflection 预算控制。

### 3.7 Telemetry 义务原则

所有 Subagent 必须履行可观测性义务：输出结构化日志、上报关键指标、参与 trace/span、明确记录预算消耗/工具调用/降级动作/错误等级。

---

## 2. Subagent 通用执行协议

### 统一输入契约

所有 Subagent 在运行时必须接收标准化输入对象 `AgentTaskInput`，包含：

- session_id, trace_id, task_id, agent_name, task_mode
- objective, input_materials, memory_context
- tool_scope, budget_allocation, output_schema
- retry_policy, degradation_policy, metadata

### 统一输出契约

所有 Subagent 必须输出标准化对象 `AgentTaskOutput`，包含：

- task_id, agent_name, result_payload, result_summary
- confidence, assumptions, unresolved_items, budget_spent
- tool_usage, latency_ms, degradation_applied, error_level
- writeback_candidate, telemetry_ref, completed_at

---

## 3. 六个核心 Subagent 的职责与约束

### Memory Agent

**核心职责**：唤醒与当前任务相关的记忆、筛选压缩去噪、形成 memory context 包、判断写回候选、执行普通/重要写回、维护 Memory Registry。

**禁止事项**：不得直接修改人格核、不得跳过审批写入角色级长期记忆、不得直接推进演进规则更新。

**默认错误策略**：检索失败可重试或降级、Memory Kernel 不可用为 Fatal。

---

### Research Agent

**核心职责**：信息搜集与多源比对、材料归并与结构化、证据链整理、洞察提炼、生成供 Decision/Writing 使用的研究素材。

**禁止事项**：不得将研究摘要冒充最终结论、不得直接修改决策记忆、不得绕过 Budget Controller 进行无约束多轮检索。

**默认错误策略**：工具短时失败重试、预算逼近阈值减少轮次、核心数据源不可达降级并报告不确定性。

---

### Decision Agent

**核心职责**：方案比较、风险识别、利弊分析、形成最佳判断、构造备选情景、标注结论成立条件与失效边界。

**禁止事项**：不得无证据直接拍板高风险结论、不得绕过 Copilot 向用户输出最终裁决、不得将猜测替代不确定性标记。

**默认错误策略**：输入证据不足返回低置信度、高质量模型不可用降级并标记、预算不足优先保留比较框架。

---

### Writing Agent

**核心职责**：结构化成稿、风格映射、输出协议适配、压缩与扩写、报告/说明书/简报的表达整理。

**禁止事项**：不得擅自发明事实、不得掩盖不确定性、不得改变 Decision Agent 的核心判断逻辑、不得擅自触发重要写回。

**默认错误策略**：格式输出失败可重试、输出协议不兼容降级为通用结构化文本、预算紧张优先保留结构。

---

### Reflection Agent

**核心职责**：评估任务有效性、识别成功/失败模式、提炼可复用经验、输出 reflection summary、形成演进线索候选。

**禁止事项**：不得直接修改长期配置、不得绕过 Evolution Agent 推动系统升级、不得将一次性波动误判为长期规律。

**默认错误策略**：预算不足直接跳过并记录 reflection_deferred、数据不足输出弱反思并降低置信度。

---

### Evolution Agent

**核心职责**：汇总 reflection 结果、识别需升级的技能/方法/记忆结构、生成长期配置修改提案、判断演进候选、推动高等级写回流程。

**禁止事项**：不得在无审计证据条件下推动升级、不得将单次异常直接变成长期规则、不得绕过审批直接修改人格核。

**默认错误策略**：证据不足输出 upgrade_candidate=false、策略校验失败拒绝推进、审批链缺失为 Fatal。

---

## 4. 记忆访问权限模型

### 读权限矩阵

| Agent | 工作记忆 | 项目记忆 | 用户记忆 | 决策记忆 | 角色/演进记忆 |
|-------|---------|---------|---------|---------|--------------|
| Copilot | 全读 | 全读 | 全读 | 全读 | 摘要读 |
| Memory Agent | 全读 | 全读 | 全读 | 全读 | 受限读 |
| Research Agent | 全读 | 主题相关读 | 受限摘要读 | 相关读 | 不读 |
| Decision Agent | 全读 | 相关读 | 受限摘要读 | 全读 | 摘要读 |
| Writing Agent | 当前任务相关读 | 相关读 | 风格相关读 | 结论相关读 | 不读 |
| Reflection Agent | 全读 | 相关读 | 受限摘要读 | 相关读 | 摘要读 |
| Evolution Agent | 摘要读 | 相关读 | 受限摘要读 | 相关读 | 全读 |

### 读权限原则

- 无关记忆不得加载
- 高敏感用户记忆默认仅摘要读
- Writing Agent 不得接触不必要的原始长期记忆

---

## 5. 写回权限与审批模型

### Level A：普通写回

允许写入：会话摘要、工作记忆压缩包、一般研究条目、检索索引更新

可执行者：Copilot、Memory Agent、Research Agent（仅研究条目）

### Level B：重要写回

允许写入：项目记忆、用户偏好更新建议、决策记忆、关键研究结论存档

可执行者：Memory Agent、Copilot（受策略约束）、Decision Agent（仅决策条目，经主代理确认）

必须生成 proposal、通过成本与冲突检查、留审计记录。

### Level C：高门槛写回

允许写入：人格核长期配置、方法包升级、输出协议核心更新、演进规则调整、角色级长期记忆更新

可执行者：Evolution Agent

执行前提：高置信度条件、升级规则检查、必要时人工确认、必须可版本回滚。

---

## 6. Agent 预算模型

### 预算分配原则

- Session Budget 是上位约束
- Agent Budget 是局部额度
- 多 agent 协作时，Copilot 不得一次性耗尽预算
- 并行 agent 默认分配上限更低
- Reflection / Evolution 预算默认后置

### 各 Agent 预算倾向

| Agent | Token | Tool Calls | Latency | 写回预算 | 备注 |
|-------|-------|-----------|---------|---------|------|
| Memory Agent | 中 | 中 | 中 | 中高 | 记忆治理优先 |
| Research Agent | 中高 | 高 | 中高 | 低 | 检索密集 |
| Decision Agent | 中高 | 中 | 中 | 中 | 判断质量优先 |
| Writing Agent | 中 | 低 | 低 | 低 | 输出时效优先 |
| Reflection Agent | 低中 | 低 | 中 | 低 | 可跳过 |
| Evolution Agent | 中 | 低中 | 中 | 高 | 高频禁用 |

---

## 7. 错误处理与降级边界

### 错误分类

| 分类 | 典型场景 | 处理策略 |
|------|---------|---------|
| **Retryable** | 网络超时、临时限流、短时资源不可用 | 自动重试 3 次，指数退避 |
| **Degradable** | Budget 逼近、检索不足、部分工具不可用 | 触发降级决策、返回部分结果并标注 |
| **Fatal** | 权限校验失败、核心依赖不可用、违反宪法约束 | 立即终止、返回明确错误 |

### 错误传播

- 子任务错误不应直接导致整个 Session 失败
- Copilot 负责错误隔离与恢复决策
- 关键路径错误必须上报
- 非关键路径错误可降级处理

---

## 8. Telemetry 义务

### 必须记录的事件

- agent.execute.start / success / error
- agent.budget.warning
- agent.degradation.applied
- agent.writeback.proposed

### 必须上报的指标

- agent_requests_total（计数器）
- agent_duration_seconds（直方图）
- agent_budget_spent（计数器）
- agent_tool_calls_total（计数器）
- agent_degradation_count（计数器）

---

## 9. 测试与审计要求

### 单元测试要求

每个 Subagent 必须有：正常执行测试、错误处理测试、降级策略测试、权限检查测试、Budget 约束测试。

### 集成测试要求

必须测试：多 agent 协作、上下文传递、错误传播、降级链路、写回流程。

### 审计要求

必须支持：完整执行链追溯、预算消耗审计、权限使用审计、降级决策审计、写回审批审计。

---

**维护者**：哈雷酱 + 小顾姥爷
**最后更新**：2026-03-08
**版本**：v1.0
**状态**：正式发布
