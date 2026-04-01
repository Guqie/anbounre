# 工程化落地建议

> **版本**：v1.0
> **维护者**：哈雷酱 (￣▽￣)／
> **最后更新**：2026-03-08
> **相关文档**：[系统架构总览](../architecture/README.md)｜[实施路线图](implementation-roadmap.md)

---

## 推荐目录结构

```
无敌战警-engine/
├── main.py                      # CLI 入口
├── config/
│   ├── config.yaml              # 系统配置
│   └── subagent_config.yaml     # Subagent 配置
├── gateway/                     # 调度层
│   ├── __init__.py
│   ├── entry_gateway.py         # 入口网关
│   ├── session_router.py        # 会话路由
│   ├── agent_dispatcher.py     # 代理分发
│   ├── channel_adapter.py       # 渠道适配
│   └── plugin_runtime.py        # 插件运行时
├── copilot/                     # 主代理
│   ├── __init__.py
│   ├── main_agent.py            # 主协调代理
│   ├── context_builder.py       # 上下文构建器
│   └── orchestrator.py          # 编排器
├── subagent/                    # Subagent 层
│   ├── __init__.py
│   ├── base.py                  # 基类
│   ├── memory_agent.py          # 记忆代理
│   ├── research_agent.py         # 研究代理
│   ├── decision_agent.py         # 决策代理
│   ├── writing_agent.py          # 写作代理
│   ├── reflection_agent.py       # 反思代理
│   └── evolution_agent.py        # 演进代理
├── kernel/                      # 三核
│   ├── __init__.py
│   ├── persona_kernel.py         # 人格核
│   ├── memory_kernel.py          # 记忆核
│   └── evolution_kernel.py       # 演进核
├── memory/                      # 记忆管理
│   ├── __init__.py
│   ├── memory_manager.py         # 记忆管理器
│   ├── memory_registry.py        # 记忆注册表
│   └── retrieval_index.py        # 检索索引
├── tools/                       # 工具层
│   ├── __init__.py
│   ├── retrieval.py             # 检索工具
│   ├── summarization.py          # 摘要工具
│   └── archiving.py              # 归档工具
├── utils/                       # 工具函数
│   ├── __init__.py
│   ├── logger.py                # 日志
│   └── metrics.py                # 指标
└── tests/                       # 测试
    ├── unit/                    # 单元测试
    ├── integration/              # 集成测试
    └── e2e/                     # 端到端测试
```

---

## 核心接口定义

### BaseSubagent（Subagent 基类）

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseSubagent(ABC):
    def __init__(
        self,
        agent_id: str,
        persona_kernel: PersonaKernel,
        memory_kernel: MemoryKernel,
        capability: Dict[str, Any]
    ):
        self.agent_id = agent_id
        self.persona_kernel = persona_kernel
        self.memory_kernel = memory_kernel
        self.capability = capability

    @abstractmethod
    async def execute(self, context: AgentContext) -> Any:
        """执行任务"""
        pass

    @abstractmethod
    def get_required_permissions(self) -> List[str]:
        """获取所需权限"""
        pass

    @abstractmethod
    def validate_context(self, context: AgentContext) -> bool:
        """验证上下文"""
        pass
```

### AgentContext（上下文载体）

```python
@dataclass
class AgentContext:
    session_id: str
    user_id: str
    task_type: str

    # 记忆相关
    working_memory: Dict[str, Any]
    long_term_memory: Dict[str, Any]

    # 人格相关
    persona_config: Dict[str, Any]

    # 任务相关
    task_input: Any
    task_output: Any

    # 中间结果
    intermediate_results: Dict[str, Any]

    # 元数据
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

---

## Subagent 生命周期管理

采用 **池化 + 懒加载** 策略：

```python
class SubagentPool:
    def __init__(self):
        self._pool: Dict[str, BaseSubagent] = {}
        self._lock = asyncio.Lock()

    async def get_agent(self, agent_type: str) -> BaseSubagent:
        async with self._lock:
            if agent_type not in self._pool:
                self._pool[agent_type] = self._create_agent(agent_type)
            return self._pool[agent_type]
```

---

## 错误处理与降级策略

实现 **三层降级策略**：

1. **重试**：自动重试 3 次
2. **降级**：使用备用 Subagent 或简化逻辑
3. **兜底**：返回默认结果或人工介入

```python
async def execute_with_fallback(
    self,
    agent: BaseSubagent,
    context: AgentContext,
    max_retries: int = 3
) -> Any:
    # 第一层：重试
    for i in range(max_retries):
        try:
            return await agent.execute(context)
        except Exception as e:
            if i == max_retries - 1:
                break
            await asyncio.sleep(2 ** i)

    # 第二层：降级
    fallback_agent = self._get_fallback_agent(agent)
    if fallback_agent:
        try:
            return await fallback_agent.execute(context)
        except Exception:
            pass

    # 第三层：兜底
    return self._get_default_result(agent, context)
```

---

## 记忆一致性保证

实现 **乐观锁 + 版本控制**：

```python
@dataclass
class MemoryEntry:
    key: str
    value: Any
    version: int  # 版本号
    updated_at: datetime
    updated_by: str  # 哪个 Subagent 更新的
```

---

## 测试策略

### 单元测试

```python
@pytest.mark.asyncio
async def test_memory_agent_read():
    agent = MemoryAgent(...)
    context = AgentContext(...)
    result = await agent.execute(context)
    assert result is not None
    assert "user_profile" in result
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_research_to_writing_pipeline():
    research_agent = ResearchAgent(...)
    writing_agent = WritingAgent(...)
    context = AgentContext(task_input="研究 AI 发展趋势")
    research_result = await research_agent.execute(context)
    context.intermediate_results["research"] = research_result
    writing_result = await writing_agent.execute(context)
    assert writing_result is not None
```

---

## 性能优化建议

### 缓存策略

三层缓存：

- **L1**：内存缓存（最快）
- **L2**：Redis 缓存（中等）
- **L3**：磁盘缓存（最慢）

### 批处理

批量处理相似任务，合并后并行执行：

```python
async def process_batch(
    self,
    tasks: List[AgentContext],
    agent: BaseSubagent
) -> List[Any]:
    batches = self._group_similar_tasks(tasks)
    results = []
    for batch in batches:
        batch_results = await asyncio.gather(*[
            agent.execute(task) for task in batch
        ])
        results.extend(batch_results)
    return results
```

---

## 监控与调试

### 结构化日志

```python
logger.info(
    "memory_agent.execute.start",
    session_id=context.session_id,
    task_type=context.task_type
)
```

### 指标收集

```python
agent_requests = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["agent_type", "status"]
)
agent_duration = Histogram(
    "agent_duration_seconds",
    "Agent execution duration",
    ["agent_type"]
)
```

---

**维护者**：哈雷酱 (￣▽￣)／
**最后更新**：2026-03-08
**版本**：v1.0
