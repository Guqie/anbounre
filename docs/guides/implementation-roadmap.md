# 总体实施路线图与模块依赖开发顺序

> **版本**：v1.0
> **维护者**：哈雷酱 + 小顾姥爷
> **最后更新**：2026-03-08
> **相关文档**：[系统架构总览](../architecture/README.md)｜[Subagent 架构](../design/01-subagent-architecture.md)｜[Gateway/Scheduler 设计](../design/02-gateway-scheduler.md)

---

## 文档目的

本文档用于回答以下工程实施问题：

1. 这套系统应按什么顺序开发；
2. 各模块之间的依赖关系是什么；
3. 哪些模块必须先做，哪些可以并行；
4. 每一阶段的目标、输出物、验收标准是什么；
5. 哪些风险可能导致返工，如何提前规避；
6. 如何从设计阶段平滑推进到 MVP、灰度上线和持续演进阶段。

> **把架构方案压缩为一条可执行、可排期、可拆任务、可验收的工程路径。**

---

## 实施总原则

### 原则 1：先立控制面，再立执行面

先建立运行时控制骨架：

- Session 生命周期
- 路由与分发框架
- 预算与降级能力
- 观测能力
- 权限与写回检查点

**原因**：如果先写 agent，再补治理层，后续一定大规模返工。

### 原则 2：先打通最小闭环，再扩展复杂链路

建议先实现一条最小可运行闭环：

```
Entry Gateway → Session Router → Agent Dispatcher → Copilot → Memory Agent → Research/Writing → 输出 → Level A 写回
```

### 原则 3：高风险模块后置，但接口前置

以下模块不应最先完整实现，但必须尽早预留接口：

- Evolution Agent
- Level C 高门槛写回
- 多端实时同步
- 自动回滚闭环
- A/B 试验分析

### 原则 4：所有模块必须默认可观测

不允许"功能先写，观测以后再补"。

### 原则 5：所有长期动作必须默认可审计

凡涉及写回、权限拒绝、降级、Fatal 错误、灰度切流、回滚，都必须留下审计痕迹。

---

## 总体实施阶段划分

将实施分为 6 个阶段：

### 阶段 0：工程底座搭建

**目标**：建立工程运行底座。

**核心输出**：

- 项目目录结构
- 分层配置系统
- 日志系统
- 指标系统
- tracing 骨架
- 密钥管理接入
- 基础 CI / 测试框架

### 阶段 1：运行时控制骨架

**目标**：建立 Gateway / Scheduler 的最小控制面。

**核心输出**：Entry Gateway、Session Manager、Session Router、Agent Dispatcher、Feature Flag 最小能力、Session / Task / RoutingDecision 数据模型。

### 阶段 2：Memory + Tool Runtime 闭环

**目标**：打通最小可运行执行链路。

**核心输出**：Tool Runtime 最小版、AgentRegistry、Memory Agent、Working / Project Memory 轻量实现、recall pipeline（轻量版）、compression-first context pack、Level A writeback。

### 阶段 3：主任务闭环 MVP

**目标**：完成面向用户的最小多代理工作流。

**核心输出**：Copilot 主代理编排骨架、Research Agent、Writing Agent、Budget Controller 最小版、基础降级策略、chat / research / write 三种 task mode。

### 阶段 4：判断与治理增强

**目标**：补齐高价值判断链路与重要写回治理。

**核心输出**：Decision Agent、Level B writeback proposal、冲突检测、审计日志、rollback 基础能力、更完整的 budget / degrade / error policy。

### 阶段 5：反思、演进与灰度上线

**目标**：引入长期优化能力，同时保证上线风险可控。

**核心输出**：Reflection Agent、Evolution Agent、Level C 写回骨架、灰度发布机制、新旧架构切流、成本监控告警、性能基准测试。

### 阶段 6：生产化增强

**目标**：补齐多端接入、缓存分层、自动化回滚和更强 observability。

**核心输出**：多层缓存、Web/API / Mobile / WebSocket 适配、更完整 A/B 测试、自动化回滚策略、端到端压测、运维面板与文档自动生成。

---

## 模块依赖总图

### L0：工程底座层

- config system、secret manager、logging、metrics、tracing、test framework

### L1：运行时控制层

- Entry Gateway、Session Manager、Session Router、Agent Dispatcher、Feature Flag、Budget Controller

### L2：执行支撑层

- AgentRegistry、Tool Runtime、Permission Checker、Policy Engine

### L3：能力代理层

- Copilot、Memory Agent、Research Agent、Decision Agent、Writing Agent、Reflection Agent、Evolution Agent

### L4：长期治理层

- Memory Kernel、Memory Registry、Retrieval Index、Writeback Proposal Engine、Conflict Checker、Audit Log、Rollback Engine

依赖方向：`L0 -> L1 -> L2 -> L3 -> L4`

---

## 开发顺序（12 步）

### Step 1：工程底座

- 目录结构、分层配置、structlog / logging 封装、Prometheus 指标基础、OpenTelemetry tracing 骨架、secret manager 接口、pytest / 测试骨架

**验收标准**：任意模块可统一读取配置、可打结构化日志、trace_id 可贯穿一次测试请求、敏感配置不硬编码。

### Step 2：核心数据模型

- TaskRequest、Session、AgentTask、BudgetProfile、RoutingDecision、MemoryRecord、WritebackProposal

**验收标准**：核心对象 schema 稳定、模块间不再用散乱 dict 传参、序列化/持久化格式明确。

### Step 3：Gateway / Session / Router 最小版

- Entry Gateway、Session Manager、Session Router、Feature Flag 最小分流

**验收标准**：任务可进入系统、能生成 session_id、能识别 chat / research / write 等基础模式。

### Step 4：AgentRegistry + Dispatcher + Permission Checker

- Agent 协议基类、AgentRegistry、AgentDispatcher、permission matrix 基础实现

**验收标准**：Dispatcher 能根据 task mode 选择 agent 组合、未注册 agent 不可调用、越权访问能被拒绝。

### Step 5：Budget Controller 最小版

- 分层 budget profile、预算装载、agent budget allocation、基础 budget accounting、简版降级策略

**验收标准**：每个 Session 能装载预算模板、每个 AgentTask 能分到预算、预算超限时能触发至少一种降级动作。

### Step 6：Tool Runtime 最小版

- tool registry、authorize_call、execute、usage accounting、timeout / retry wrapper

**验收标准**：agent 不直接调用外部工具、所有工具调用可被预算计量、工具错误可统一包装。

### Step 7：Memory 最小闭环

- MemoryRecord 模型、Working / Project Memory 最小版、recall pipeline（轻量）、compression-first context pack、Level A writeback

**验收标准**：Memory Agent 能产出 memory context、可完成最小召回与压缩、会话摘要可被写回 working memory。

### Step 8：Copilot + Memory Agent + Writing Agent

- Copilot 最小编排逻辑、Memory Agent、Writing Agent、chat / write 路径

**验收标准**：用户可得到稳定输出、输出链路可观测、基础写回可运行。

### Step 9：Research Agent + research task mode

- Research Agent、research 路由、检索工具接入、研究摘要输出

**验收标准**：research 任务可跑通、研究素材进入 Writing Agent、budget / latency / degradation 可观测。

### Step 10：Decision Agent + Level B writeback

- Decision Agent、decision task mode、Writeback Proposal、Conflict Checker、审计日志

**验收标准**：架构/判断任务可跑通、决策记忆可 proposal 化、冲突写回可被拦截。

### Step 11：Reflection / Evolution 后置接入

- Reflection Agent、Evolution Agent、Level C 写回基础骨架、rollback 基础能力

**验收标准**：reflection 可被预算策略跳过或执行、evolution 不会默认频繁触发、高门槛写回不会绕过审批。

### Step 12：灰度 / 基准 / 上线准备

- 灰度发布策略、新旧架构切流、成本监控与告警、性能 benchmark、压测与失败演练

**验收标准**：可对 5% 流量切入新架构、可快速回滚到旧链路、可监控 budget burn / latency / error rate。

---

## 并行开发建议

### 可并行组 A：工程底座

config、logging、metrics、tracing、secret manager、test skeleton

### 可并行组 B：核心模型与协议

Session / AgentTask schema、Agent protocol、MemoryRecord / Proposal schema、budget profile schema

### 可并行组 C：执行与治理

在 Step 4 以后：Tool Runtime、Memory 最小闭环、Budget Controller、permission checker

### 不建议并行过早启动

Evolution Agent、Level C writeback、多端 WebSocket 会话、全量 A/B 系统、自动化回滚闭环

---

## 里程碑设计

| 里程碑 | 达成条件 |
|--------|---------|
| **M1：控制骨架建立** | Gateway / Session / Router / Dispatcher 跑通、observability 基础具备、核心数据模型稳定 |
| **M2：最小记忆闭环建立** | Memory Agent 能召回并压缩、Level A writeback 可用、chat / write 可跑通 |
| **M3：MVP 完整闭环建立** | research 模式可用、Budget Controller 可工作、Tool Runtime 接入可观测 |
| **M4：高价值判断链路建立** | Decision Agent 可用、Level B proposal 可用、冲突检测与审计可用 |
| **M5：灰度上线准备完成** | Reflection / Evolution 基础接入、灰度分流可控、成本监控和回滚可执行 |

---

## 风险点与规避策略

| 风险 | 规避 |
|------|------|
| 过早实现复杂 agent，忽略控制骨架 | 先完成 Session / Dispatcher / Budget / Runtime，agent 只在控制骨架下实现 |
| Memory 一开始做太重 | 先做 Working / Project Memory 最小版，Level C、复杂 novelty scoring 后置 |
| 预算控制只做统计，不做约束 | Budget Controller 必须参与 dispatch、runtime、writeback |
| Observability 后补 | 把日志、指标、trace 当作 DoD 的一部分 |
| 写回治理太晚实现 | MVP 阶段至少要有 Level A 规则和 Level B proposal 骨架 |

---

## Definition of Done（完成定义）

每个模块必须同时满足以下条件才算完成：

1. 功能实现完成
2. 结构化日志已接入
3. 至少一个关键指标已上报
4. trace/span 已挂载
5. 基础单元测试通过
6. 配置不硬编码
7. 错误分级明确
8. 权限与预算检查已接入（如适用）
9. 文档注释与 schema 说明齐备

---

## 最终推荐开发顺序（极简版）

> **先做工程底座与控制骨架，再做记忆与工具闭环，再做 Copilot + 核心 agent，再做判断与写回治理，最后做反思、演进与灰度上线。**

1. 工程底座
2. 核心数据模型
3. Gateway / Session / Router
4. AgentRegistry / Dispatcher / Permission
5. Budget Controller
6. Tool Runtime
7. Memory 最小闭环
8. Copilot + Memory + Writing
9. Research
10. Decision + Level B proposal
11. Reflection / Evolution
12. 灰度 / 基准 / 上线

---

**维护者**：哈雷酱 + 小顾姥爷
**最后更新**：2026-03-08
**版本**：v1.0
**状态**：正式发布
