---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
created: 2026-03-03
updated: 2026-03-03
---

# GuDaStudio Commands 使用指南

> 基于 RPI 和有效上下文理论，让 Claude Code 一次只专注于一件事

**来源**: [GitHub - GuDaStudio/commands](https://github.com/GuDaStudio/commands)

---

## 一、项目简介

### 核心定位

**GuDaStudio Commands** — RPI 编码理论的完整实现

- 基于 RPI (Research-Plan-Implementation) 编码理论
- 融合 OpenSpec 规范和多模型协作
- 让 Claude Code 更适用于复杂场景、长时间编码任务
- 以人为本的操作理念，多阶段手动分割上下文
- 极致利用 Claude Code 的有效上下文（约 80K）

### 项目数据

- **Stars**: 817 ⭐
- **Forks**: 47
- **许可证**: MIT
- **最后更新**: 2026-01-28 (v0.2.0)
- **开发者**: GuDaStudio

### 设计理念

**核心问题**: Claude Code 的 200K 上下文窗口虽大，但有效上下文约 80K

**解决方案**:
- 将复杂任务拆解为多个阶段（Research → Plan → Implementation）
- 每个阶段专注一件事，控制上下文在 80K 以内
- 通过 OpenSpec 文档在阶段间传递信息
- 多模型协作提升各阶段质量

**RPI 理论**:
- **Research**: 需求研究，形成约束集
- **Plan**: 计划制定，消除不确定性
- **Implementation**: 代码实现，零决策执行

---

## 二、核心命令

### gudaspec 命令集

| 命令 | 功能 | 阶段 |
|------|------|------|
| `/gudaspec:init` | 初始化 OpenSpec 环境，验证 MCP 工具可用性 | 准备阶段 |
| `/gudaspec:research` | 并行探索代码库，将需求转化为约束集 | Research 阶段 |
| `/gudaspec:plan` | 多模型分析，生成零决策执行计划与 PBT 属性 | Plan 阶段 |
| `/gudaspec:implementation` | 多模型协作实现，原型重构为生产级代码 | Implementation 阶段 |

### 命令详解

#### 1. /gudaspec:init

**功能**: 项目初始化

**执行内容**:
- 自动安装 OpenSpec 框架
- 检测 Codex-MCP 是否可用
- 检测 Gemini-MCP 是否可用
- 创建项目配置文件

**使用时机**: 项目开始前，仅需执行一次

**输出**: 初始化报告，MCP 工具可用性检测结果

#### 2. /gudaspec:research

**功能**: 需求研究与约束集生成

**执行内容**:
- 并行探索代码库（使用 Auggie MCP）
- 理解用户需求
- 识别需求中的歧义，主动征求用户意见
- 将需求转化为技术约束集
- 生成初步 OpenSpec 文档

**使用时机**: 收到新需求时

**输入**: 用户需求描述

**输出**: OpenSpec 初步提案文档

**上下文控制**: 约 60K 左右

#### 3. /gudaspec:plan

**功能**: 计划制定与不确定性消除

**执行内容**:
- 读取 Research 阶段生成的 OpenSpec 文档
- 启动多模型协作（Codex + Gemini）
- 对实现方案进行分析细化
- 消除技术上的模糊性
- 提取 Property-Based Testing 属性
- 生成零决策执行计划（可顺序执行的 pipeline）

**使用时机**: Research 阶段完成后

**输入**: OpenSpec 初步提案

**输出**: 完整 OpenSpec 文档（含执行计划和 PBT 属性）

**上下文控制**: 新开会话，约 70K 左右

#### 4. /gudaspec:implementation

**功能**: 代码实现与多模型协作

**执行内容**:
- 读取 Plan 阶段生成的 OpenSpec 文档
- 自动识别最小可验证任务
- 逐步实现各阶段任务
- 启用多模型代码原型获取（前端/UI → Gemini，后端/逻辑 → Codex）
- 每完成一阶段任务后启用多模型 review
- 重构原型为生产级代码

**使用时机**: Plan 阶段完成后

**输入**: 完整 OpenSpec 文档

**输出**: 生产级代码

**上下文控制**:
- 每完成一阶段任务后暂停
- 若上下文 < 80K，继续下一阶段
- 若上下文 > 80K，建议 `/clear` 新开会话

---

## 三、核心概念

### 1. OpenSpec 规范

**定义**: 规范化的需求-实现工作流框架

**作用**:
- 结构化的约束集管理
- 确保从需求到代码的可追溯性和一致性
- 在阶段间传递信息的标准格式

**文档结构**:
- 需求描述
- 约束集（技术限制条件）
- 实现方案
- 执行计划
- PBT 属性（可验证属性）

### 2. 约束集（Constraint Set）

**定义**: 将需求转化为具体的技术限制条件

**作用**:
- 消除实现阶段的决策点
- 每个约束都缩小解空间
- 使实现阶段成为纯机械执行，无需即时判断

**示例**:
```
需求: "生成一个美观的天气页面"
约束集:
- UI 设计参考苹果公司顶级前端设计
- 支持北京、上海、深圳三个城市
- 四种基础天气（大风、降雨、晴天、下雪）
- 实时天气信息必须为真实数据
- 包含温度、湿度等信息
```

### 3. Property-Based Testing (PBT)

**定义**: 基于属性的测试方法

**作用**:
- 在 Plan 阶段提取可验证属性
- 供 Implementation 阶段验证使用
- 确保实现符合需求

**示例**:
```
属性 1: 温度数据必须与中央气象台一致
属性 2: 城市切换后天气数据必须更新
属性 3: 不同天气类型必须有不同的视觉展示
```

### 4. 有效上下文理论

**核心观点**: Claude Code 的有效上下文约 80K

**理论依据**:
- 200K 上下文窗口 ≠ 200K 有效上下文
- 上下文过长会导致注意力分散
- 80K 是最专注的上下文长度

**实践策略**:
- 每个阶段控制上下文在 80K 以内
- 通过 `/clear` 手动分割上下文
- 使用 OpenSpec 文档在阶段间传递信息

---

## 四、安装与使用

### 前置要求

**必需工具**:
- Claude Code v2.1.15+
- Auggie MCP（上下文检索工具）

**可选工具**:
- Codex-MCP（后端逻辑协作）
- Gemini-MCP（前端 UI 协作）

### 安装步骤

**1. 克隆仓库**:
```bash
git clone https://github.com/GuDaStudio/commands.git
cd commands
```

**2. 运行安装脚本**:

**Linux / macOS**:
```bash
# 用户级安装（所有项目生效）
./install.sh --user

# 项目级安装（仅当前项目生效）
./install.sh --project

# 自定义路径
./install.sh --target /your/custom/path
```

**Windows (PowerShell)**:
```powershell
# 用户级安装（所有项目生效）
.\install.ps1 -User

# 项目级安装（仅当前项目生效）
.\install.ps1 -Project

# 自定义路径
.\install.ps1 -Target C:\your\custom\path
```

**3. 验证安装**:
- 启动 Claude Code
- 输入 `/gudaspec`
- 应显示可用命令列表

### 配置全局提示词（强烈推荐）

在 `~/.claude/CLAUDE.md` 中添加以下提示词：

```markdown
# CLAUDE.md

## 0. Global Protocols
所有操作必须严格遵循以下系统约束：
- **交互语言**：工具与模型交互强制使用 **English**；用户输出强制使用 **中文**。
- **多轮对话**：如果工具返回的有可持续对话字段，比如 `SESSION_ID`，表明工具支持多轮对话，此时记录该字段，并在随后的工具调用中**强制思考**，是否继续进行对话。
- **沙箱安全**：严禁 Codex/Gemini 对文件系统进行写操作。所有代码获取必须请求 `unified diff patch` 格式。
- **代码主权**：外部模型生成的代码仅作为逻辑参考（Prototype），最终交付代码**必须经过重构**，确保无冗余、企业级标准。
- **风格定义**：整体代码风格**始终定位**为，精简高效、毫无冗余。该要求同样适用于注释与文档，且对于这两者，严格遵循**非必要不形成**的核心原则。
- **仅对需求做针对性改动**：严禁影响用户现有的其他功能。
- **上下文检索**：调用 `mcp__auggie-mcp__codebase-retrieval`，必须减少 search/find/grep 的次数。
- **判断依据**：始终以项目代码、grok 的搜索结果作为判断依据，严禁使用一般知识进行猜测，允许向用户表明自己的不确定性。
- **MUST** ultrathink in English.
```

---

## 五、完整使用示例

### 案例：从零生成可视化天气页面

**需求描述**:
```
生成一个美观的实时天气展示页面。要求：
1. 实时天气信息必须为真实信息，包含温度、湿度等
2. 用户可以选择北京、上海、深圳三个城市
3. 四种不同的基础天气（大风、降雨、晴天、下雪），有不同的页面展示
4. UI 设计极具美感，参考苹果公司的顶级前端设计
```

**推荐配置**: Claude Opus 4.5 + 推理模式

---

### 阶段 0: Init 项目初始化

**Step 1**: 进入项目，打开 Claude Code，键入 `/gudaspec:init`

**Step 2**: Claude 自动执行：
- 安装 OpenSpec 框架
- 检测 Codex-MCP 可用性
- 检测 Gemini-MCP 可用性

**Step 3**: 初始化完成后，键入 `/clear` 清空上下文，新开对话

**上下文消耗**: 约 10K

---

### 阶段 1: Research 需求研究

**Step 1**: 在新会话窗口中输入：
```
/gudaspec:research
我需要生成一个美观的实时天气展示页面。要求：
  1. 实时天气信息必须为真实信息，包含温度、湿度等
  2. 用户可以选择北京、上海、深圳三个城市
  3. 四种不同的基础天气（大风、降雨、晴天、下雪），有不同的页面展示。
  4. UI设计极具美感，参考苹果公司的顶级前端设计。
```

**Step 2**: Claude 自动执行：
- 调用 Auggie MCP 探索代码库
- 理解用户需求
- 识别需求中的歧义，主动征求用户意见
- 将需求转化为技术约束集
- 生成初步 OpenSpec 文档

**Step 3**: 生成初步 spec 文档后，键入 `/clear` 新开会话

**上下文消耗**: 约 59.5K（距离 80K 最佳上下文还有空间）

**输出示例**:
```
OpenSpec 初步提案：
- 约束 1: 使用真实天气 API（如和风天气）
- 约束 2: 支持三个城市切换（北京、上海、深圳）
- 约束 3: 四种天气类型有不同视觉效果
- 约束 4: UI 参考 Apple 设计语言（简洁、流畅、高端）
- 技术栈建议: React + Tailwind CSS + 天气 API
```

---

### 阶段 2: Plan 计划制定

**Step 1**: 在新会话窗口中输入：
```
/gudaspec:plan
```

**Step 2**: Claude 自动执行：
- 读取 Research 阶段生成的 OpenSpec 文档
- 启动多模型协作（Codex + Gemini）
- Codex 分析后端逻辑和 API 集成
- Gemini 分析前端 UI 和视觉设计
- 整合多模型方案，细化需求
- 消除技术模糊性
- 提取 PBT 属性

**Step 3**: 生成完整 spec 文档后，键入 `/clear` 新开会话

**上下文消耗**: 约 70K

**输出示例**:
```
完整 OpenSpec 文档：

执行计划（零决策 pipeline）:
1. 搭建 React 项目基础架构
2. 集成和风天气 API
3. 实现城市切换功能
4. 实现四种天气类型的视觉效果
5. 优化 UI 细节（动画、过渡效果）
6. 测试与验证

PBT 属性:
- 属性 1: 温度数据必须与中央气象台一致（误差 < 1°C）
- 属性 2: 城市切换后天气数据必须在 2 秒内更新
- 属性 3: 不同天气类型必须有明显不同的视觉展示
- 属性 4: UI 响应时间 < 100ms
```

---

### 阶段 3: Implementation 代码实现

**Step 1**: 在新会话窗口中输入：
```
/gudaspec:implementation
```

**Step 2**: Claude 自动执行：
- 读取 Plan 阶段生成的 OpenSpec 文档
- 识别最小可验证任务（如"搭建 React 项目基础架构"）
- 启用多模型代码原型获取：
  - 前端/UI 部分 → Gemini 生成原型
  - 后端/逻辑部分 → Codex 生成原型
- 重构原型为生产级代码
- 完成一阶段任务后暂停，询问是否继续

**Step 3**: 检查上下文窗口：
- 若 < 80K，输入 "继续" 进行下一阶段
- 若 > 80K，输入 `/clear` 新开会话，重新执行 `/gudaspec:implementation`

**Step 4**: 每完成一阶段任务后，Claude 自动启用多模型 review：
- Codex review 后端逻辑
- Gemini review 前端 UI
- 整合反馈，优化代码

**Step 5**: 重复 Step 2-4，直到所有任务完成

**上下文控制策略**:
- 任务 1（架构搭建）: 约 20K
- 任务 2（API 集成）: 约 35K
- 任务 3（城市切换）: 约 50K
- 任务 4（视觉效果）: 约 70K → `/clear` 新开会话
- 任务 5（UI 优化）: 约 30K
- 任务 6（测试验证）: 约 50K

**最终成果**: 拥有真实数据的天气系统，温度数据与中央气象台一致

---

## 六、工作流详解

### RPI 三阶段工作流

```
用户需求 → Research 阶段 → OpenSpec 初步提案 
         → Plan 阶段 → OpenSpec 完整文档 
         → Implementation 阶段 → 生产级代码
```

### 上下文管理策略

```
阶段 0: Init
├─ 上下文: ~10K
└─ 操作: /clear 新开会话

阶段 1: Research
├─ 上下文: ~60K
└─ 操作: /clear 新开会话

阶段 2: Plan
├─ 上下文: ~70K
└─ 操作: /clear 新开会话

阶段 3: Implementation
├─ 任务 1-3: ~70K
├─ 操作: /clear 新开会话
├─ 任务 4-6: ~50K
└─ 完成
```

### 多模型协作流程

**Plan 阶段**:
```
Claude 读取 OpenSpec 初步提案
  ↓
调用 Codex 分析后端逻辑
  ↓
调用 Gemini 分析前端 UI
  ↓
Claude 整合方案
  ↓
生成完整 OpenSpec 文档
```

**Implementation 阶段**:
```
Claude 读取完整 OpenSpec 文档
  ↓
识别最小可验证任务
  ↓
调用 Gemini 生成前端原型
  ↓
调用 Codex 生成后端原型
  ↓
Claude 重构为生产级代码
  ↓
调用 Codex review 后端
  ↓
调用 Gemini review 前端
  ↓
Claude 整合反馈并优化
```

---

## 七、核心优势

### 1. 有效上下文极致利用

- 基于 80K 有效上下文理论
- 多阶段手动分割上下文
- 每个阶段专注一件事
- 避免上下文过长导致注意力分散

### 2. 零决策执行

- Research 阶段将需求转化为约束集
- Plan 阶段消除所有技术不确定性
- Implementation 阶段成为纯机械执行
- 无需即时判断，提升代码质量

### 3. 多模型协作

- Claude 全局理解 + Codex 后端逻辑 + Gemini 前端 UI
- 各模型发挥专长
- 交叉验证提升质量
- 自动 review 机制

### 4. OpenSpec 规范化

- 结构化的需求-实现工作流
- 在阶段间传递信息的标准格式
- 确保可追溯性和一致性
- 支持复杂项目管理

### 5. 以人为本

- 用户掌控上下文分割时机
- 每个阶段完成后暂停询问
- 透明的执行过程
- 灵活的工作节奏

---

## 八、与其他工具对比

| 特性 | GuDaStudio Commands | GuDaStudio Skills | 原生 Claude Code |
|------|-------------------|------------------|-----------------|
| 核心功能 | RPI 工作流框架 | 多模型协作框架 | AI 编码助手 |
| 上下文管理 | 手动分割（80K 最佳） | 自动管理 | 自动管理 |
| 工作流 | 3 阶段（Research/Plan/Implementation） | 5 阶段（含上下文检索和审计） | 无固定流程 |
| 多模型协作 | ✅ Codex + Gemini | ✅ Codex + Gemini | ❌ |
| OpenSpec 规范 | ✅ | ❌ | ❌ |
| 约束集管理 | ✅ | ❌ | ❌ |
| PBT 属性提取 | ✅ | ❌ | ❌ |
| 适用场景 | 复杂长时间任务 | 复杂开发任务 | 日常开发 |
| 学习曲线 | 较陡峭 | 较陡峭 | 平缓 |
| 用户控制度 | 高（手动分割） | 中（自动管理） | 低（完全自动） |

---

## 九、使用建议

### 适合人群

✅ 需要处理复杂长时间编码任务的开发者
✅ 追求代码质量和架构设计的专业开发者
✅ 愿意学习 RPI 工作流的用户
✅ 有 Codex/Gemini MCP 的用户
✅ 关注上下文管理和效率优化的用户

### 不适合人群

❌ 简单任务场景（过度设计）
❌ 不想手动分割上下文的用户
❌ 只使用 Claude 的用户
❌ 追求快速原型的场景

### 核心价值

1. **上下文极致利用**: 80K 有效上下文理论，避免注意力分散
2. **零决策执行**: 约束集管理，消除实现阶段的不确定性
3. **多模型协作**: 发挥各模型专长，提升代码质量
4. **规范化工作流**: OpenSpec 规范，确保可追溯性
5. **以人为本**: 用户掌控节奏，透明的执行过程

### 最佳实践

**1. 推荐配置**:
- Claude Opus 4.5 + 推理模式
- 安装 Auggie MCP（必需）
- 安装 Codex-MCP 和 Gemini-MCP（可选但推荐）

**2. 上下文管理**:
- 严格遵循 80K 上下文限制
- 每个阶段完成后主动 `/clear`
- 不要在单个会话中完成所有阶段

**3. 需求描述**:
- 尽量详细描述需求
- 包含具体的技术要求
- 提供参考案例或设计风格

**4. 阶段衔接**:
- Research 阶段生成的 OpenSpec 文档是 Plan 阶段的输入
- Plan 阶段生成的完整文档是 Implementation 阶段的输入
- 不要跳过任何阶段

**5. 多模型协作**:
- 信任 Codex 的后端逻辑分析
- 信任 Gemini 的前端 UI 设计
- Claude 负责整合和重构

---

## 十、FAQ

### Q1: 什么是 OpenSpec？

OpenSpec 是一个规范化的需求-实现工作流框架，通过结构化的约束集管理，确保从需求到代码的可追溯性和一致性。

### Q2: 必须安装 Codex/Gemini MCP 吗？

不是必须的。但若要使用完整的多模型协作功能，需要安装对应的 MCP 工具。运行 `/gudaspec:init` 会检测并提示安装。

### Q3: 约束集有什么作用？

约束集将需求转化为具体的技术限制条件，消除实现阶段的决策点。每个约束都缩小解空间，使实现阶段成为纯机械执行，无需即时判断。

### Q4: 为什么要手动分割上下文？

基于有效上下文理论，Claude Code 的有效上下文约 80K。上下文过长会导致注意力分散，影响代码质量。手动分割让每个阶段专注一件事。

### Q5: 可以跳过某个阶段吗？

不建议。RPI 三阶段是完整的工作流：
- Research 阶段形成约束集
- Plan 阶段消除不确定性
- Implementation 阶段零决策执行

跳过任何阶段都会影响最终质量。

### Q6: 与 GuDaStudio Skills 有什么区别？

- **Commands**: 专注 RPI 工作流和上下文管理，适合复杂长时间任务
- **Skills**: 专注多模型协作框架，适合复杂开发任务

两者可以互补使用。

### Q7: 如何判断上下文是否超过 80K？

Claude Code 会在界面右下角显示当前上下文使用情况。建议：
- < 70K: 安全，可以继续
- 70K-80K: 注意，考虑分割
- > 80K: 建议 `/clear` 新开会话

---

## 十一、参考资源

### 官方资源

- **GitHub 仓库**: https://github.com/GuDaStudio/commands
- **官方网站**: https://code.guda.studio
- **英文文档**: https://github.com/GuDaStudio/commands/blob/main/docs/README_EN.md

### 相关工具

- **Auggie MCP**: 上下文检索工具（必需）
  - 官方文档: https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code
- **Codex-MCP**: OpenAI Codex CLI（可选）
- **Gemini-MCP**: Google Gemini CLI（可选）
- **GuDaStudio Skills**: 多模型协作框架
  - GitHub: https://github.com/GuDaStudio/skills

### 相关概念

- **RPI 理论**: Research-Plan-Implementation 编码理论
- **OpenSpec**: 规范化需求-实现工作流框架
- **有效上下文理论**: 80K 最佳上下文窗口
- **约束集管理**: 将需求转化为技术限制条件
- **Property-Based Testing**: 基于属性的测试方法

---

## 十二、总结

GuDaStudio Commands 是一个**专业且创新**的 Claude Code 命令集：

**核心价值**:
- RPI 工作流 — Research → Plan → Implementation 三阶段
- 有效上下文极致利用 — 基于 80K 理论，手动分割上下文
- 零决策执行 — 约束集管理，消除实现阶段的不确定性
- 多模型协作 — Claude + Codex + Gemini 各展所长
- OpenSpec 规范 — 结构化的需求-实现工作流

**使用建议**:
- 适合复杂长时间编码任务
- 需要学习 RPI 工作流框架
- 推荐配置 Auggie MCP + Codex-MCP + Gemini-MCP
- 严格遵循 80K 上下文限制
- 每个阶段完成后主动 `/clear`

**定位**: 专业的 RPI 工作流实现，适合作为 Claude Code 的高级扩展，提升复杂项目的开发效率和代码质量。通过有效上下文管理和多模型协作，让 Claude Code 一次只专注于一件事。

**与 GuDaStudio Skills 的关系**:
- Commands 专注 RPI 工作流和上下文管理
- Skills 专注多模型协作框架
- 两者可以互补使用，共同提升开发效率

---

**⭐ 在 GitHub 上给项目点星，支持开源！**
