# Gateway / Scheduler 详细设计

> **版本**：v1.0
> **维护者**：哈雷酱 + 小顾姥爷
> **最后更新**：2026-03-08
> **状态**：设计阶段
> **相关文档**：[系统架构总览](../architecture/README.md)｜[Subagent 架构](01-subagent-architecture.md)

---

## 设计定位与目标

### 定位

Gateway / Scheduler 是整个 Subagent 架构的**运行时控制平面**，负责：

- **统一入口**：接收来自多种渠道的任务请求
- **会话管理**：维护任务的完整生命周期
- **智能路由**：根据任务类型选择执行模式
- **代理分发**：选择和编排 Subagent 执行
- **预算治理**：全局 Budget 控制和降级
- **可观测性**：日志、指标、追踪的统一管理

### 设计目标

1. **解耦**：入口逻辑与代理逻辑完全分离
2. **可扩展**：支持新渠道、新任务模式、新 Subagent
3. **可观测**：完整的日志、指标、追踪体系
4. **可控**：Budget 治理、降级策略、错误处理
5. **高性能**：异步执行、缓存优化、批处理

---

## 核心模块总览

Gateway / Scheduler 包含 **8 个核心模块**：

| 模块 | 职责 | 关键能力 |
|------|------|----------|
| **Entry Gateway** | 统一入口网关 | 事件监听、命令解析、请求验证 |
| **Session Manager** | 会话管理器 | 会话创建、状态维护、生命周期管理 |
| **Session Router** | 会话路由器 | 任务分类、模式选择、路由决策 |
| **Agent Dispatcher** | 代理分发器 | Subagent 选择、协作编排、上下文构建 |
| **Channel Adapter** | 渠道适配器 | 多渠道协议适配（Obsidian/CLI/WebSocket/REST） |
| **Plugin/Tool Runtime** | 插件运行时 | 工具注册、调用、结果缓存 |
| **Budget Controller** | 预算控制器 | 全局 Budget 治理、降级决策 |
| **Observability & Release Controller** | 可观测性与发布控制器 | 日志、指标、追踪、Feature Flag、灰度发布 |

---

## Entry Gateway 详细设计

### 核心组件

#### 1. 事件监听器（Event Listener）

监听不同渠道的事件：

- **Obsidian 事件**：文件保存、命令触发、快捷键
- **CLI 命令**：`python main.py <command>`
- **WebSocket 消息**：实时消息推送
- **REST API 请求**：HTTP 请求

#### 2. 命令解析器（Command Parser）

解析用户输入，提取：task_type、task_input、user_id、session_id（可选）

#### 3. 请求验证器（Request Validator）

验证请求合法性：必填字段检查、格式验证、权限验证、速率限制

### 数据流

```
外部请求 → Event Listener → Command Parser → Request Validator → TaskRequest
```

---

## Session Manager 详细设计

### 会话状态机

```
received → normalized → routed → budgeted → dispatched → executing → finalizing → closed
```

### 会话存储

- **内存存储**：活跃会话（Redis）
- **持久化存储**：历史会话（数据库）

---

## Session Router 详细设计

### 基础任务模式（7 种）

| 任务模式 | 触发条件 | 目标 Subagent |
|---------|---------|--------------|
| `chat` | 对话交互 | Copilot |
| `research` | 信息研究 | Memory Agent → Research Agent |
| `decision` | 决策分析 | Memory Agent → Decision Agent |
| `write` | 写作生成 | Memory Agent → Writing Agent |
| `archive` | 知识归档 | Research Agent → Memory Agent |
| `reflect` | 反思复盘 | Reflection Agent |
| `evolve` | 演进升级 | Evolution Agent |

---

## Agent Dispatcher 详细设计

### 分发策略

#### 策略 A：单代理直接执行

```
Task → Single Subagent → Result
```

适用场景：简单任务，无需协作

#### 策略 B：串行执行

```
Task → Agent1 → Agent2 → Agent3 → Result
```

适用场景：有明确依赖关系的任务

#### 策略 C：并行执行

```
Task → [Agent1, Agent2, Agent3] → Merge → Result
```

适用场景：独立子任务可并行

#### 策略 D：条件分支

```
Task → Condition → Agent1 (条件 A)
                 → Agent2 (条件 B)
```

适用场景：根据条件选择不同路径

#### 策略 E：循环迭代

```
Task → Agent1 → Agent2 → Check → Continue/End
         ↑                  ↓
         └──────────────────┘
```

适用场景：需要多轮迭代优化

---

## Budget Controller 详细设计

### Budget 层级（5 层）

```yaml
budgets:
  # 1. Token Budget
  token:
    total: 12000
    reserve: 1500
    system_max: 8000

  # 2. Model Budget
  model:
    max_calls_per_session: 10
    max_concurrent_calls: 3

  # 3. Tool Budget
  tool:
    max_tool_calls: 20
    max_tool_time: 30s

  # 4. Retrieval Budget
  retrieval:
    max_results: 50
    max_embedding_calls: 10

  # 5. Latency Budget
  latency:
    max_session_time: 120s
    max_agent_time: 30s
```

### 降级决策

当 Budget 不足时，触发降级：

1. **减少并发**：降低并行 Subagent 数量
2. **简化上下文**：减少记忆加载
3. **跳过非关键步骤**：跳过反思、演进
4. **使用缓存**：优先使用缓存结果
5. **降级模型**：使用更小的模型
6. **限制工具调用**：减少工具使用
7. **快速失败**：提前终止任务
8. **拒绝任务**：返回错误

---

## 数据对象设计

### TaskRequest

```python
@dataclass
class TaskRequest:
    user_id: str
    task_type: str
    task_input: Any
    metadata: Dict[str, Any]
    created_at: datetime
```

### Session

```python
@dataclass
class Session:
    session_id: str
    user_id: str
    task_type: str
    status: str  # received/normalized/routed/...
    task_input: Any
    task_output: Any
    created_at: datetime
    updated_at: datetime
```

### AgentTask

```python
@dataclass
class AgentTask:
    task_id: str
    session_id: str
    agent_type: str
    status: str
    input: Any
    output: Any
    created_at: datetime
```

### RoutingDecision

```python
@dataclass
class RoutingDecision:
    mode: str
    subagents: List[str]
    collaboration_mode: str  # sequential/parallel/conditional/iterative
    budget_profile: BudgetProfile
```

---

## 错误处理

### 3 级错误

#### 1. Retryable（可重试）

- 网络超时、临时性错误、速率限制

**处理**：自动重试 3 次，指数退避

#### 2. Degradable（可降级）

- Budget 不足、资源不足、部分失败

**处理**：触发降级策略

#### 3. Fatal（致命）

- 权限错误、数据错误、系统错误

**处理**：立即终止，返回错误

---

## 工具运行时抽象

### BaseTool 接口

```python
class BaseTool(ABC):
    @abstractmethod
    async def execute(self, params: Dict) -> Any:
        pass

    @abstractmethod
    def validate_params(self, params: Dict) -> bool:
        pass
```

---

## MVP 实施建议

| Phase | 时长 | 核心任务 |
|-------|------|----------|
| Phase 1：基础框架 | 2 周 | Entry Gateway、Session Manager、Session Router（基础路由） |
| Phase 2：核心功能 | 3 周 | Agent Dispatcher、Channel Adapter（CLI）、Plugin/Tool Runtime |
| Phase 3：治理能力 | 2 周 | Budget Controller、降级策略、错误处理 |
| Phase 4：可观测性 | 1 周 | Logging、Metrics、Tracing |

---

**维护者**：哈雷酱 + 小顾姥爷
**最后更新**：2026-03-08
**版本**：v1.0
