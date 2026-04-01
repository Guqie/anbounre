# 工程文档总入口

> **项目**：无敌战警系统
> **版本**：v2.0
> **维护者**：哈雷酱 (￣▽￣)／
> **最后更新**：2026-04-02

---

## 文档定位

本文档是所有工程设计文档的索引入口。工程文档按用途分为四层：

| 层级 | 目录 | 说明 |
|------|------|------|
| **架构层** | `architecture/` | 系统全景、架构图谱 |
| **设计层** | `design/` | 详细设计文档 |
| **指南层** | `guides/` | 实施路线图、工程化建议 |
| **参考层** | `reference/` | 规范契约 |

---

## 快速导航

### 从这里开始

1. **新人入门**：[系统架构总览](architecture/README.md) → [架构可视化图谱](architecture/diagrams.md)
2. **开发者**：[Subagent 架构](design/01-subagent-architecture.md) → [上下文注入契约](reference/上下文注入契约.md)
3. **实施规划**：[实施路线图](guides/implementation-roadmap.md) → [工程化建议](guides/engineering-guide.md)

---

## 文档列表

### 架构层 (architecture/)

| 文档 | 说明 |
|------|------|
| [系统架构总览](architecture/README.md) | 系统定位、三核架构、三层架构、知识库结构 |
| [架构可视化图谱](architecture/diagrams.md) | Mermaid 图表集（系统架构、Subagent 网络、数据流、时序图） |

### 设计层 (design/)

| 文档 | 说明 |
|------|------|
| [01 - Subagent 架构与调度层设计](design/01-subagent-architecture.md) | 三核底座、6 个核心 Subagent、调度层架构 |
| [02 - Gateway/Scheduler 详细设计](design/02-gateway-scheduler.md) | 8 个核心模块、会话生命周期、Budget 控制 |
| [03 - Subagent 宪法与权限模型](design/03-subagent-constitution.md) | 宪法总则、Agent 职责约束、权限矩阵、预算模型 |
| [04 - Memory 权限模型与写回治理](design/04-memory-governance.md) | 六层记忆、召回策略、写回等级、污染防控 |

### 指南层 (guides/)

| 文档 | 说明 |
|------|------|
| [总体实施路线图](guides/implementation-roadmap.md) | 6 阶段实施、12 步开发顺序、里程碑、风险点 |
| [工程化落地建议](guides/engineering-guide.md) | 目录结构、接口定义、测试策略、性能优化 |

### 参考层 (reference/)

| 文档 | 说明 |
|------|------|
| [上下文注入契约规范](reference/上下文注入契约.md) | Directive vs Reference、ContextBlock 标准、预算装箱、压缩策略 |

---

## 文档阅读顺序建议

```
新人入门：
  1. architecture/README.md（系统全景）
  2. architecture/diagrams.md（可视化图谱）

开发者：
  3. design/01-subagent-architecture.md（Subagent 架构）
  4. design/03-subagent-constitution.md（宪法总则）
  5. design/04-memory-governance.md（记忆治理）
  6. reference/上下文注入契约.md（上下文规范）

实施者：
  7. guides/implementation-roadmap.md（实施路线图）
  8. guides/engineering-guide.md（工程化建议）
  9. design/02-gateway-scheduler.md（调度层详细设计）
```

---

## 与知识库的关联

工程文档定义了系统的技术架构，其落地实现依赖以下知识库模块：

| 知识库模块 | 对应工程内容 |
|-----------|-------------|
| `08-大脑核心/` | Memory Kernel（记忆核）的知识库落地 |
| `09-灵魂系统/` | Persona Kernel（人格核）的知识库落地 |
| `05-AI技术文档/` | AI 技术积累，支持 Subagent 实现 |
| `00-每日工作区/` | 日常使用入口，对应 CLI / Gateway 层 |

代码实现位于：`D:/桌面/无敌战警-engine/`

---

## 文档维护规范

1. **版本管理**：文档头部使用 YAML frontmatter 标注 `版本`、`维护者`、`最后更新`
2. **链接规范**：跨文档引用使用相对路径，内部知识库引用使用 `[[双链]]`
3. **图表规范**：架构图使用 Mermaid，格式见 `architecture/diagrams.md`
4. **命名规范**：设计文档使用序号前缀（`01-` `02-`），确保排序正确

---

**维护者**：哈雷酱 (￣▽￣)／
**最后更新**：2026-04-02
