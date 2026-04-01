# Subagent 架构与调度层设计

> **版本**：v1.0
> **维护者**：哈雷酱 + 小顾姥爷
> **最后更新**：2026-03-08
> **状态**：架构设计阶段
> **相关文档**：[系统架构总览](../architecture/README.md)｜[Gateway/Scheduler 详细设计](02-gateway-scheduler.md)｜[Subagent 宪法](03-subagent-constitution.md)

---

## 架构定位

### 系统新定位

**一个以三核为本体、以 Copilot 为主代理、以 Subagent 为执行网络、以 OpenClaw 式调度层为入口中枢的 Obsidian 认知系统**

### 不是什么

- 一个 Obsidian 插件集合
- 一个大模型聊天壳
- 一个纯 RAG 知识库
- 一个单体 Agent

### 是什么

- 可成长的角色型认知系统
- 多代理协作的智能工作流引擎
- 基于三核的自演进系统
- 统一调度的多入口平台

---

## 核心设计原则

### 原则 1：三核是本体

三核不做具体任务，只定义系统存在方式：

- **人格核（Persona Kernel）**：角色核心底色
- **记忆核（Memory Kernel）**：角色经验基础
- **演进核（Evolution Kernel）**：角色成长机制

### 原则 2：Copilot 是主代理

主代理职责：

- 读取三核
- 理解当前任务
- 选择 Subagent
- 编排上下文
- 协调工具和写回
- 保持整体一致性

**Copilot = 总协调代理 / 主意识代理**

### 原则 3：Subagent 共享人格底色

所有 Subagent 必须：

- 共享同一人格底色（不能各自发展独立人格）
- 使用不同职业身份、技能包和方法包
- 遵守统一的输出协议

### 原则 4：调度层独立

参考 OpenClaw 的 gateway / channel / plugin 思想：

- 入口逻辑不塞进代理里
- 统一的 Session Router
- 可扩展的 Channel Adapter
- 独立的 Plugin/Tool Runtime

### 原则 5：记忆读写分权

不是所有 Subagent 都能平等访问全部记忆：

- **普通写回**：工作记忆、临时结论、研究条目
- **重要写回**：决策记忆、用户记忆
- **高门槛写回**：角色记忆、能力升级、演进规则

### 原则 6：演进更新分级

三层写回权限：

- Writing Agent 不能直接改角色记忆
- Research Agent 不能直接改能力升级
- Evolution Agent 才有权限推动角色/能力升级

---

## Subagent 体系设计

### 核心 Subagent（6 个）

#### 1. Memory Agent

**职责**：

- 唤醒工作记忆、用户记忆、决策记忆
- 判断哪些内容该进入长期记忆
- 负责写回和记忆压缩
- 管理 Memory Registry

**能力包**：

- 记忆检索、记忆压缩、记忆索引、记忆写回

**权限**：

- 读：全部记忆
- 写：工作记忆、用户记忆（需确认）

---

#### 2. Research Agent

**职责**：

- 信息搜集、多材料比较
- 研究结构化、洞察提炼
- 构造研究结论

**能力包**：检索、摘要、对比、归纳

**权限**：读（知识库、检索索引）、写（研究条目、三行摘要）

---

#### 3. Decision Agent

**职责**：

- 方案比较、风险识别、利弊分析
- 形成最佳判断、构造备选情景
- 标注结论成立条件与失效边界

**能力包**：专业信息分析师、架构顾问、风险评估

**权限**：读（全部记忆、研究条目）、写（决策记忆、决策日志）

---

#### 4. Writing Agent

**职责**：

- 生成结构化输出、风格适配
- 压缩与扩写、报告/说明书成文

**能力包**：输出协议、风格适配、结构化表达

**权限**：读（研究条目、决策记忆）、写（输出文档，不能改核心记忆）

---

#### 5. Reflection Agent

**职责**：

- 复盘任务有效性
- 提炼经验、识别失败模式
- 生成演进线索

**能力包**：反思框架、经验提炼、失败模式识别

**权限**：读（全部记忆、演进日志）、写（反思记录、演进线索）

---

#### 6. Evolution Agent

**职责**：

- 汇总反思结果
- 判断技能包/方法包/记忆结构升级
- 形成演进建议或自动更新计划

**能力包**：演进规则、能力升级、记忆结构优化

**权限**：读（全部记忆、演进日志）、写（演进核、能力层、记忆结构，最高权限）

---

## 调度层设计

### 调度层架构（Agent Gateway）

包含 5 个模块：

#### 1. Entry Gateway（入口网关）

统一入口：

- Obsidian 事件（文件保存、命令触发）
- CLI 命令（python main.py xxx）
- 快捷命令（Obsidian Command Palette）
- 移动端（未来）
- 外部消息入口（未来：微信、邮件）

#### 2. Session Router（会话路由）

负责把任务分到不同执行模式：

- `chat` - 对话模式
- `research` - 研究模式
- `archive` - 归档模式
- `write` - 写作模式
- `reflect` - 反思模式
- `evolve` - 演进模式

#### 3. Agent Dispatcher（代理分发）

真正决定调用哪个 Subagent，或由谁协同：

- 单代理任务：直接分发
- 多代理协作：编排执行顺序
- 主代理协调：Copilot 统筹

#### 4. Channel Adapter（渠道适配）

接不同入口协议：

- Obsidian Plugin API
- Python CLI
- WebSocket（未来）
- REST API（未来）

#### 5. Plugin/Tool Runtime（插件运行时）

所有工具和插件不直接挂在主代理上，而是挂在运行时里供调度层调用：

- 检索工具、摘要工具、归档工具
- 写作工具、反思工具

---

## 实施路线图

### Phase 1：基础设施（Week 1-3）

- [ ] 设计 Agent Gateway 接口
- [ ] 实现 Entry Gateway
- [ ] 实现 Session Router
- [ ] 实现 Agent Dispatcher
- [ ] 定义 Subagent 接口

### Phase 2：核心 Subagent（Week 4-9）

- [ ] 实现 Memory Agent
- [ ] 实现 Research Agent
- [ ] 实现 Writing Agent
- [ ] 实现 Decision Agent
- [ ] 实现 Reflection Agent
- [ ] 实现 Evolution Agent

### Phase 3：Copilot 升级（Week 10-12）

- [ ] 重构 Copilot 为主协调代理
- [ ] 实现 Subagent 选择策略
- [ ] 实现多代理协作编排

### Phase 4：三核集成（Week 13-16）

- [ ] 人格核集成
- [ ] 记忆核集成
- [ ] 演进核集成
- [ ] 权限控制实现

### Phase 5：调度层完善（Week 17-19）

- [ ] Channel Adapter 实现
- [ ] Plugin/Tool Runtime 实现
- [ ] 会话管理
- [ ] 监控与日志

### Phase 6：测试与优化（Week 20-22）

- [ ] 端到端测试
- [ ] 性能优化
- [ ] 文档完善
- [ ] 用户验收

---

## 技术选型建议

### 编程语言

- **Python 3.10+**（当前已使用）
- 异步支持：`asyncio`
- 类型提示：`typing`

### 框架与库

| 类别 | 技术 |
|------|------|
| 调度层 | FastAPI、asyncio、APScheduler |
| Subagent | LangChain（可选）、Pydantic、structlog |
| 记忆与检索 | LanceDB、Sentence Transformers |
| 配置管理 | Pydantic Settings、python-dotenv |

### 数据格式

- **YAML**（配置文件）
- **JSON**（数据交换）
- **Markdown**（知识库）

---

## 风险点与应对

| 风险 | 应对策略 |
|------|----------|
| 复杂度爆炸 | 严格控制 Subagent 数量、统一接口规范、完善文档 |
| 性能问题 | 异步执行（asyncio）、缓存机制、懒加载 |
| 记忆一致性 | 记忆锁机制、事务性写入、版本控制、冲突检测 |
| 人格分裂 | 强制共享人格底色、统一输出协议、定期一致性检查 |
| 权限失控 | 严格权限控制、写入前验证、审计日志、回滚机制 |

---

## 附录

### 参考架构

- **Copilot**：主代理范式
- **Smart Connections**：记忆与检索底座
- **OpenClaw**：入口与调度范式

### 创新点

用三核把这一切统合成一个可成长的角色型认知系统

---

**维护者**：哈雷酱 + 小顾姥爷
**最后更新**：2026-03-08
**版本**：v1.0
