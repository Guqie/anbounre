---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
created: 2026-03-04
updated: 2026-03-04
---

# BMad-Method 使用指南

> Build More, Architect Dreams - AI 驱动的敏捷开发平台

**来源**: [GitHub - bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD/)

---

## 一、项目简介

### 核心定位

**BMad-Method** — AI 原生的敏捷开发平台

- 基于 AI 代理的协作式开发工作流
- 从产品构思到实现的完整生命周期管理
- 模块化架构，支持自定义扩展
- 100% 免费开源，无付费墙

### 项目数据

- **版本**: V6.0.4（官方稳定版）
- **许可证**: MIT
- **官方网站**: https://docs.bmad-method.org
- **GitHub**: https://github.com/bmad-code-org/BMAD-METHOD/
- **社区**: Discord - https://discord.gg/gk8jAdXWmj
- **YouTube**: https://www.youtube.com/@BMadCode

### 设计理念

**核心问题**: 传统开发流程在 AI 时代效率低下

**解决方案**:
- **AI 代理协作**: 10+ 专业代理（PM、架构师、开发、QA 等）
- **结构化工作流**: 25+ 预定义工作流覆盖完整开发周期
- **知识管理**: 自动生成和维护项目文档
- **模块化平台**: 核心 + 模块生态，按需安装

**V6 核心特性**:
- 平台化架构（Core + Module Ecosystem）
- 新的 BMad Method for Agile AI-Driven Development（V4 的进化版）
- 模块化安装，自定义开发体验
- 社区模块生态（即将推出）

---

## 二、安装与配置

### 前置要求

**必需工具**:
- Claude Code v2.0+
- Node.js 18+
- npm 或 npx

**推荐环境**:
- Git 仓库（用于版本控制）
- 现代终端（支持彩色输出）

### 安装步骤

**Step 1**: 在项目根目录运行安装命令

```bash
npx bmad-method@latest install --directory . --tools claude-code -y
```

**参数说明**:
- `--directory .`: 安装到当前目录
- `--tools claude-code`: 配置 Claude Code 集成
- `-y`: 自动接受默认选项（跳过交互式提示）

**Step 2**: 等待安装完成

安装过程会：
- 下载 BMad Core（核心模块）
- 安装默认模块（BMad Method for Agile AI-Driven Development）
- 创建目录结构
- 生成配置文件
- 配置 Claude Code 集成

**Step 3**: 重启 Claude Code

⚠️ **重要**: 必须重启 Claude Code 才能加载 BMad 扩展！

**Step 4**: 验证安装

重启后，在 Claude Code 中运行：

```
/bmad-help
```

如果看到 BMad 帮助系统，说明安装成功！

### 安装后的目录结构

```
项目根目录/
├── _bmad/                          # BMad 核心目录
│   ├── core/                       # 核心模块
│   │   ├── agents/                 # 核心代理
│   │   ├── workflows/              # 核心工作流
│   │   └── config.yaml             # 核心配置
│   ├── bmm/                        # BMad Method 模块
│   │   ├── agents/                 # BMM 代理
│   │   ├── workflows/              # BMM 工作流
│   │   └── data/                   # 模板和数据
│   ├── _config/                    # 配置文件
│   │   ├── workflow-manifest.csv   # 工作流清单
│   │   ├── task-manifest.csv       # 任务清单
│   │   └── agent-manifest.csv      # 代理清单
│   └── _memory/                    # 记忆存储
├── _bmad-output/                   # 输出目录
│   ├── planning-artifacts/         # 规划产物
│   └── implementation-artifacts/   # 实现产物
├── docs/                           # 项目知识库
└── .claude/                        # Claude Code 配置
    └── commands/                   # 命令目录
        └── BMad/                   # BMad 命令
```

### 配置文件

**核心配置**: `_bmad/core/config.yaml`

```yaml
user_name: Guqi                      # 用户名称
communication_language: English      # 交流语言
document_output_language: English    # 文档输出语言
output_folder: _bmad-output          # 输出目录
```

**自定义配置**:
- 编辑 `_bmad/core/config.yaml` 修改配置
- 重启 Claude Code 使配置生效

### Git 配置建议

如果不希望将 BMad 工作流文件提交到 Git，在 `.gitignore` 中添加：

```
_bmad/
_bmad-output/
.claude/commands/BMad/
docs/
```

---
## 三、核心概念

### 1. 平台架构

**BMad V6 = Core + Module Ecosystem**

```
BMad Platform
├── Core（核心）
│   ├── BMad Master（主控代理）
│   ├── Party Mode（多代理协作）
│   ├── Brainstorming（头脑风暴）
│   └── Help System（帮助系统）
└── Modules（模块）
    ├── BMad Method for Agile AI-Driven Development（敏捷开发）
    ├── BMad Builder（构建工具）
    ├── BMad Creative Intelligence Suite（创意套件）
    ├── BMad Game Dev Studio（游戏开发）
    └── Test Architect（测试架构）
```

**核心模块（Core）**:
- 始终安装，提供基础功能
- BMad Master 主控代理
- Party Mode 多代理协作
- 帮助和引导系统

**可选模块（Modules）**:
- 按需安装，扩展特定功能
- 默认安装 BMad Method for Agile AI-Driven Development
- 其他模块可在安装时选择

### 2. 三大核心组件

#### 2.1 代理系统（Agents）

**定义**: 专业化的 AI 角色，负责特定职责

**核心代理**:
- **BMad Master**: 主控代理，工作流编排，知识管理
- **PM（Product Manager）**: 产品经理，需求分析
- **Architect**: 架构师，技术方案设计
- **Dev**: 开发工程师，代码实现
- **QA**: 质量保证，测试和验证
- **UX Designer**: 用户体验设计师
- **Tech Writer**: 技术文档编写
- **Analyst**: 业务分析师
- **SM（Scrum Master）**: 敏捷教练
- **Quick Flow Solo Dev**: 快速开发（单人模式）

**代理特性**:
- 每个代理有独特的人格和专业知识
- 代理之间可以协作（Party Mode）
- 代理会维护上下文和记忆

#### 2.2 工作流系统（Workflows）

**定义**: 结构化的多步骤流程，引导完成特定任务

**工作流分类**:

**1. 分析阶段（Analysis）**:
- `create-product-brief`: 创建产品简报
- `domain-research`: 领域研究
- `market-research`: 市场研究
- `technical-research`: 技术研究

**2. 规划阶段（Planning）**:
- `create-prd`: 创建产品需求文档
- `edit-prd`: 编辑 PRD
- `validate-prd`: 验证 PRD
- `create-ux-design`: 创建 UX 设计

**3. 解决方案阶段（Solutioning）**:
- `create-architecture`: 创建架构设计
- `create-epics-and-stories`: 创建史诗和用户故事
- `check-implementation-readiness`: 检查实现就绪度

**4. 实现阶段（Implementation）**:
- `sprint-planning`: Sprint 规划
- `create-story`: 创建故事
- `dev-story`: 开发故事
- `code-review`: 代码审查
- `correct-course`: 纠正路线
- `sprint-status`: Sprint 状态
- `retrospective`: 回顾会议

**5. 快速流程（Quick Flow）**:
- `quick-spec`: 快速规格说明
- `quick-dev`: 快速开发

**6. 其他工具**:
- `document-project`: 文档化项目
- `generate-project-context`: 生成项目上下文
- `qa-generate-e2e-tests`: 生成端到端测试

**工作流特性**:
- 分步引导，每步有明确的输入输出
- 自动生成文档和产物
- 支持暂停和恢复
- 可自定义和扩展

#### 2.3 任务系统（Tasks）

**定义**: 独立的、可执行的操作单元

**任务类型**:
- **编辑任务**: 修改现有文档（如 edit-prd）
- **验证任务**: 检查质量和完整性（如 validate-prd）
- **生成任务**: 创建新内容（如 generate-project-context）
- **审查任务**: 代码和文档审查（如 code-review）

**任务特性**:
- 可独立调用，无需完整工作流
- 快速执行，适合小型操作
- 可组合成工作流

### 3. 开发生命周期

**BMad Method 完整流程**:

```
1. 分析（Analysis）
   ├─ 产品简报（Product Brief）
   ├─ 市场研究（Market Research）
   ├─ 领域研究（Domain Research）
   └─ 技术研究（Technical Research）
   
2. 规划（Planning）
   ├─ 产品需求文档（PRD）
   ├─ UX 设计（UX Design）
   └─ PRD 验证（PRD Validation）
   
3. 解决方案（Solutioning）
   ├─ 架构设计（Architecture）
   ├─ 史诗和故事（Epics & Stories）
   └─ 实现就绪检查（Implementation Readiness）
   
4. 实现（Implementation）
   ├─ Sprint 规划（Sprint Planning）
   ├─ 故事开发（Story Development）
   ├─ 代码审查（Code Review）
   ├─ Sprint 状态（Sprint Status）
   └─ 回顾会议（Retrospective）
```

**快速流程（适合小型变更）**:

```
Quick Spec → Quick Dev → Done
```

### 4. 知识管理

**产物存储**:
- `_bmad-output/planning-artifacts/`: 规划阶段产物
- `_bmad-output/implementation-artifacts/`: 实现阶段产物
- `docs/`: 项目知识库

**自动生成的文档**:
- Product Brief（产品简报）
- PRD（产品需求文档）
- Architecture Design（架构设计）
- Epics and Stories（史诗和故事）
- Sprint Plans（Sprint 计划）
- Retrospectives（回顾报告）

**记忆系统**:
- `_bmad/_memory/`: 代理记忆存储
- 跨会话保持上下文
- 自动学习项目知识

---
## 四、快速开始

### 第一次使用

**Step 1**: 重启 Claude Code 后，运行帮助命令

```
/bmad-help
```

**Step 2**: BMad 会分析你的项目状态并提供建议

例如：
- 如果是新项目：建议从 `create-product-brief` 开始
- 如果已有需求：建议创建 PRD
- 如果已有 PRD：建议创建架构设计

**Step 3**: 根据建议选择合适的工作流

### 启动 BMad Master

**命令**:
```
/bmad-agent-bmad-master
```

**功能**:
- 显示主菜单
- 列出所有可用的工作流和任务
- 提供工作流编排和引导

**菜单选项**:
1. `[MH]` Menu Help - 重新显示菜单
2. `[CH]` Chat - 与代理聊天
3. `[LT]` List Tasks - 列出所有任务
4. `[LW]` List Workflows - 列出所有工作流
5. `[PM]` Party Mode - 启动多代理协作
6. `[DA]` Dismiss Agent - 退出代理

### 常用命令速查

**帮助系统**:
```
/bmad-help                          # 获取建议
/bmad-help where should I start     # 询问如何开始
```

**代理调用**:
```
/bmad-agent-bmad-master             # 主控代理
/bmad-agent-bmm-pm                  # 产品经理
/bmad-agent-bmm-architect           # 架构师
/bmad-agent-bmm-dev                 # 开发工程师
/bmad-agent-bmm-qa                  # QA 工程师
```

**工作流调用**:
```
/bmad-bmm-create-product-brief      # 创建产品简报
/bmad-bmm-create-prd                # 创建 PRD
/bmad-bmm-create-architecture       # 创建架构设计
/bmad-bmm-sprint-planning           # Sprint 规划
/bmad-bmm-quick-spec                # 快速规格说明
```

**任务调用**:
```
/bmad-bmm-validate-prd              # 验证 PRD
/bmad-bmm-code-review               # 代码审查
/bmad-bmm-sprint-status             # Sprint 状态
```

---

## 五、典型使用场景

### 场景 1: 从零开始的新项目

**目标**: 从一个想法开始，完成完整的产品开发

**流程**:

**1. 创建产品简报**
```
/bmad-bmm-create-product-brief
```

引导你完成：
- 产品愿景
- 目标用户
- 成功指标
- 范围定义

输出：`_bmad-output/planning-artifacts/product-brief.md`

**2. 进行市场研究（可选）**
```
/bmad-bmm-market-research
```

分析：
- 竞争对手
- 目标客户
- 市场机会

输出：`_bmad-output/planning-artifacts/market-research.md`

**3. 创建 PRD**
```
/bmad-bmm-create-prd
```

生成完整的产品需求文档，包括：
- 功能需求
- 非功能需求
- 用户故事
- 验收标准

输出：`_bmad-output/planning-artifacts/prd.md`

**4. 创建 UX 设计**
```
/bmad-bmm-create-ux-design
```

规划：
- 用户流程
- 界面模式
- 交互设计

输出：`_bmad-output/planning-artifacts/ux-design.md`

**5. 创建架构设计**
```
/bmad-bmm-create-architecture
```

设计：
- 技术栈选择
- 系统架构
- 数据模型
- API 设计

输出：`_bmad-output/planning-artifacts/architecture.md`

**6. 创建史诗和故事**
```
/bmad-bmm-create-epics-and-stories
```

分解需求为：
- Epic（史诗）
- User Story（用户故事）
- 优先级排序

输出：`_bmad-output/planning-artifacts/epics-and-stories.md`

**7. 检查实现就绪度**
```
/bmad-bmm-check-implementation-readiness
```

验证：
- PRD 完整性
- UX 设计完整性
- 架构设计完整性
- 史诗和故事完整性

**8. Sprint 规划**
```
/bmad-bmm-sprint-planning
```

生成：
- Sprint 计划
- 任务分配
- 时间估算

输出：`_bmad-output/implementation-artifacts/sprint-plan.md`

**9. 开发故事**
```
/bmad-bmm-create-story [story-id]
/bmad-bmm-dev-story [story-file]
```

实现：
- 创建故事文件
- 开发代码
- 单元测试

**10. 代码审查**
```
/bmad-bmm-code-review
```

审查：
- 代码质量
- 最佳实践
- 潜在问题

**11. Sprint 回顾**
```
/bmad-bmm-retrospective
```

总结：
- 完成情况
- 经验教训
- 改进建议

### 场景 2: 快速开发小功能

**目标**: 快速实现一个小功能或修复

**流程**:

**1. 创建快速规格说明**
```
/bmad-bmm-quick-spec
```

快速定义：
- 功能描述
- 技术方案
- 实现步骤

输出：`_bmad-output/planning-artifacts/quick-spec-[name].md`

**2. 快速开发**
```
/bmad-bmm-quick-dev
```

直接实现：
- 读取快速规格
- 生成代码
- 完成功能

**时间**: 通常 10-30 分钟完成

### 场景 3: 现有项目文档化

**目标**: 为现有项目生成 AI 友好的文档

**流程**:

**1. 文档化项目**
```
/bmad-bmm-document-project
```

自动生成：
- 项目概述
- 架构说明
- 代码结构
- API 文档

输出：`docs/project-documentation.md`

**2. 生成项目上下文**
```
/bmad-bmm-generate-project-context
```

创建：
- AI 代理规则
- 项目约定
- 技术栈说明

输出：`docs/project-context.md`

### 场景 4: 多代理协作（Party Mode）

**目标**: 让多个代理一起讨论和解决问题

**启动**:
```
/bmad-party-mode
```

**使用场景**:
- 复杂决策需要多角度分析
- 头脑风暴需要不同专业视角
- 技术方案评审

**参与代理**:
- PM（产品视角）
- Architect（技术视角）
- Dev（实现视角）
- QA（质量视角）
- UX Designer（用户体验视角）

**工作方式**:
1. 你提出问题或话题
2. 各代理轮流发言
3. 代理之间可以互相讨论
4. 最终形成共识或方案

---
## 六、核心工作流详解

### 6.1 产品简报工作流（Product Brief）

**命令**: `/bmad-bmm-create-product-brief`

**目的**: 通过协作式探索创建产品简报

**步骤**:
1. **初始化**: 项目基本信息
2. **愿景**: 产品愿景和目标
3. **用户**: 目标用户和用户画像
4. **指标**: 成功指标和 KPI
5. **范围**: 功能范围和边界
6. **完成**: 生成最终简报

**输出**: `_bmad-output/planning-artifacts/product-brief.md`

**适用场景**: 项目启动阶段，需要明确产品方向

### 6.2 PRD 工作流（Product Requirements Document）

**命令**: `/bmad-bmm-create-prd`

**目的**: 创建完整的产品需求文档

**内容包括**:
- 产品概述
- 功能需求（详细描述）
- 非功能需求（性能、安全、可用性）
- 用户故事
- 验收标准
- 约束条件

**相关命令**:
- `/bmad-bmm-edit-prd`: 编辑现有 PRD
- `/bmad-bmm-validate-prd`: 验证 PRD 质量

**输出**: `_bmad-output/planning-artifacts/prd.md`

**适用场景**: 需求明确后，进入详细规划阶段

### 6.3 架构设计工作流（Architecture）

**命令**: `/bmad-bmm-create-architecture`

**目的**: 创建技术架构和解决方案设计

**内容包括**:
- 技术栈选择和理由
- 系统架构图
- 数据模型设计
- API 设计
- 安全考虑
- 性能优化策略
- 部署架构

**输出**: `_bmad-output/planning-artifacts/architecture.md`

**适用场景**: PRD 完成后，需要技术方案设计

### 6.4 史诗和故事工作流（Epics & Stories）

**命令**: `/bmad-bmm-create-epics-and-stories`

**目的**: 将需求分解为可执行的史诗和用户故事

**分解层级**:
```
Epic（史诗）
└── User Story（用户故事）
    ├── 描述
    ├── 验收标准
    ├── 优先级
    └── 估算
```

**输出**: `_bmad-output/planning-artifacts/epics-and-stories.md`

**适用场景**: 架构设计完成后，准备进入实现阶段

### 6.5 Sprint 规划工作流（Sprint Planning）

**命令**: `/bmad-bmm-sprint-planning`

**目的**: 从史诗生成 Sprint 状态跟踪

**内容包括**:
- Sprint 目标
- 选定的用户故事
- 任务分解
- 时间估算
- 风险识别

**输出**: `_bmad-output/implementation-artifacts/sprint-plan.md`

**适用场景**: 开始新的 Sprint 前

### 6.6 故事开发工作流（Story Development）

**命令**:
```
/bmad-bmm-create-story [story-id]    # 创建故事文件
/bmad-bmm-dev-story [story-file]     # 开发故事
```

**两步流程**:

**Step 1: 创建故事文件**
- 从 Sprint 计划中选择故事
- 创建包含完整上下文的故事文件
- 包含需求、设计、验收标准

**Step 2: 开发故事**
- 读取故事文件
- 实现代码
- 编写测试
- 更新文档

**输出**: 
- 故事文件：`_bmad-output/implementation-artifacts/stories/story-[id].md`
- 代码和测试

**适用场景**: Sprint 执行阶段

### 6.7 代码审查工作流（Code Review）

**命令**: `/bmad-bmm-code-review`

**目的**: 执行对抗性代码审查，发现具体问题

**审查维度**:
- 代码质量
- 最佳实践
- 性能问题
- 安全漏洞
- 可维护性
- 测试覆盖

**输出**: 审查报告，包含具体问题和改进建议

**适用场景**: 代码完成后，合并前

### 6.8 快速流程（Quick Flow）

**命令**:
```
/bmad-bmm-quick-spec    # 快速规格说明
/bmad-bmm-quick-dev     # 快速开发
```

**适用场景**:
- 小型功能（< 1 天工作量）
- Bug 修复
- 简单优化
- 配置变更

**优势**:
- 跳过完整的规划流程
- 快速迭代
- 适合敏捷响应

**流程**:
```
需求 → Quick Spec → Quick Dev → 完成
```

---

## 七、最佳实践

### 7.1 项目启动最佳实践

**1. 从产品简报开始**
- 不要跳过产品简报
- 明确愿景和目标
- 定义成功指标

**2. 进行必要的研究**
- 市场研究（了解竞争）
- 领域研究（了解行业）
- 技术研究（了解技术栈）

**3. 创建完整的 PRD**
- 详细描述功能需求
- 明确非功能需求
- 定义验收标准

**4. 验证 PRD 质量**
```
/bmad-bmm-validate-prd
```

### 7.2 架构设计最佳实践

**1. 基于 PRD 设计**
- 确保架构满足所有需求
- 考虑非功能需求（性能、安全、可扩展性）

**2. 选择合适的技术栈**
- 考虑团队技能
- 考虑项目规模
- 考虑长期维护

**3. 文档化决策**
- 记录技术选择的理由
- 记录架构权衡
- 记录关键约束

**4. 检查实现就绪度**
```
/bmad-bmm-check-implementation-readiness
```

### 7.3 Sprint 执行最佳实践

**1. 合理规划 Sprint**
- 不要过度承诺
- 留出缓冲时间
- 考虑风险

**2. 按优先级开发**
- 先做高优先级故事
- 先做风险高的故事
- 保持灵活性

**3. 持续代码审查**
- 每个故事完成后审查
- 不要积累技术债
- 及时修复问题

**4. 定期检查 Sprint 状态**
```
/bmad-bmm-sprint-status
```

**5. 及时纠正路线**
```
/bmad-bmm-correct-course
```

### 7.4 文档管理最佳实践

**1. 保持文档更新**
- 代码变更时更新文档
- 定期审查文档准确性

**2. 使用项目上下文**
```
/bmad-bmm-generate-project-context
```
- 为 AI 代理提供项目规则
- 定义编码约定
- 记录技术决策

**3. 文档化现有项目**
```
/bmad-bmm-document-project
```
- 为棕地项目生成文档
- 帮助新成员快速上手

### 7.5 团队协作最佳实践

**1. 使用 Party Mode 进行决策**
```
/bmad-party-mode
```
- 复杂决策需要多角度分析
- 让不同角色的代理参与讨论

**2. 定期回顾**
```
/bmad-bmm-retrospective
```
- 每个 Epic 完成后回顾
- 提取经验教训
- 持续改进

**3. 保持沟通**
- 使用 BMad 生成的文档作为沟通基础
- 确保所有人对需求和设计有共同理解

### 7.6 质量保证最佳实践

**1. 自动化测试**
```
/bmad-bmm-qa-generate-e2e-tests
```
- 为关键功能生成端到端测试
- 保持测试覆盖率

**2. 代码审查**
- 使用对抗性审查发现问题
- 不要依赖自动化工具

**3. 验证验收标准**
- 每个故事完成后验证
- 确保满足所有验收标准

---
## 八、常见问题（FAQ）

### Q1: BMad-Method 是免费的吗？

**A:** 是的，100% 免费开源！
- MIT 许可证
- 无付费墙
- 无隐藏费用
- 社区完全开放

### Q2: 需要什么前置知识？

**A:** 基础开发知识即可：
- 了解软件开发流程
- 熟悉命令行操作
- 会使用 Claude Code
- 不需要特定编程语言经验

### Q3: 支持哪些编程语言？

**A:** BMad 是语言无关的：
- 工作流和文档生成不依赖特定语言
- 代码生成支持主流语言（Python、JavaScript、TypeScript、Java、Go 等）
- 可以通过配置自定义

### Q4: 可以用于现有项目吗？

**A:** 完全可以！
- 使用 `/bmad-bmm-document-project` 文档化现有项目
- 使用 `/bmad-bmm-generate-project-context` 生成项目上下文
- 逐步引入 BMad 工作流

### Q5: 如何自定义工作流？

**A:** 两种方式：
1. **修改现有工作流**: 编辑 `_bmad/bmm/workflows/` 中的文件
2. **创建自定义模块**: 参考官方文档创建自己的模块

### Q6: Party Mode 是什么？

**A:** 多代理协作模式：
- 多个专业代理同时参与讨论
- 适合复杂决策和头脑风暴
- 提供多角度分析

### Q7: 如何处理大型项目？

**A:** BMad 专为大型项目设计：
- 模块化架构支持复杂项目
- 史诗和故事分解管理复杂度
- Sprint 规划控制开发节奏
- 文档自动生成减少维护负担

### Q8: 生成的文档可以修改吗？

**A:** 可以！
- 所有文档都是 Markdown 格式
- 可以手动编辑
- 建议通过工作流更新以保持一致性

### Q9: 如何升级 BMad？

**A:** 重新运行安装命令：
```bash
npx bmad-method@latest install --directory . --tools claude-code -y
```
- 会自动检测版本
- 备份现有配置
- 升级到最新版本

### Q10: 遇到问题如何获取帮助？

**A:** 多种途径：
1. 运行 `/bmad-help` 获取即时建议
2. 查看官方文档：https://docs.bmad-method.org
3. 加入 Discord 社区：https://discord.gg/gk8jAdXWmj
4. GitHub Issues：https://github.com/bmad-code-org/BMAD-METHOD/issues

### Q11: 可以离线使用吗？

**A:** 部分功能可以：
- 工作流和代理在本地运行
- 需要 Claude Code 连接（需要网络）
- 文档生成和管理完全本地

### Q12: 如何贡献到 BMad？

**A:** 欢迎贡献！
- 提交 Bug 报告
- 提出功能建议
- 贡献代码（Pull Request）
- 分享使用经验
- 创建社区模块

### Q13: BMad 与其他工具的区别？

**A:** 核心差异：
- **vs 传统项目管理工具**: BMad 是 AI 原生的，自动生成文档
- **vs 代码生成工具**: BMad 覆盖完整开发生命周期，不只是代码
- **vs 敏捷工具**: BMad 集成 AI 代理，提供智能建议和自动化

### Q14: 团队如何协作使用 BMad？

**A:** 推荐方式：
- 将 `_bmad-output/` 和 `docs/` 提交到 Git
- 团队成员共享文档和规划
- 各自使用 BMad 代理辅助开发
- 定期同步和回顾

### Q15: 性能如何？会很慢吗？

**A:** 性能优秀：
- 工作流执行快速（秒级）
- 代码生成取决于 Claude Code 响应
- 文档生成即时
- 无明显性能瓶颈

---

## 九、参考资源

### 官方资源

**官方网站**:
- 文档站：https://docs.bmad-method.org
- 主页：https://bmad-method.org

**GitHub**:
- 主仓库：https://github.com/bmad-code-org/BMAD-METHOD/
- 更新日志：https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md
- Issues：https://github.com/bmad-code-org/BMAD-METHOD/issues

**社区**:
- Discord：https://discord.gg/gk8jAdXWmj
- YouTube：https://www.youtube.com/@BMadCode

**支持项目**:
- GitHub Star：https://github.com/bmad-code-org/BMAD-METHOD/
- 捐赠：https://buymeacoffee.com/bmad
- 企业赞助：联系官方

### 相关工具

**Claude Code**:
- 官方文档：https://docs.claude.com/docs/claude-code
- 必需工具，BMad 的运行环境

**Node.js**:
- 官方网站：https://nodejs.org
- 运行 BMad 安装器所需

### 学习资源

**官方文档**:
- 快速开始：https://docs.bmad-method.org/getting-started
- 工作流指南：https://docs.bmad-method.org/workflows
- 代理系统：https://docs.bmad-method.org/agents
- 最佳实践：https://docs.bmad-method.org/best-practices

**视频教程**:
- YouTube 频道：https://www.youtube.com/@BMadCode
- 包含完整的使用教程和案例分析

**社区资源**:
- Discord 社区分享
- GitHub Discussions
- 用户案例和经验

### 相关项目

**BMad 模块生态**:
- BMad Core（核心模块）
- BMad Method for Agile AI-Driven Development
- BMad Builder
- BMad Creative Intelligence Suite
- BMad Game Dev Studio
- Test Architect
- 社区模块（即将推出）

---

## 十、总结

BMad-Method 是一个**强大且创新**的 AI 原生开发平台：

**核心价值**:
- **完整生命周期** — 从产品构思到实现的全流程支持
- **AI 代理协作** — 10+ 专业代理提供多角度支持
- **结构化工作流** — 25+ 预定义工作流覆盖所有场景
- **知识管理** — 自动生成和维护项目文档
- **模块化平台** — 灵活扩展，按需定制

**使用建议**:
- 适合各种规模的项目（从小功能到大型系统）
- 新项目从产品简报开始，现有项目从文档化开始
- 充分利用代理系统和工作流
- 保持文档更新，建立知识库
- 参与社区，分享经验

**定位**: 专业的 AI 原生开发平台，适合追求高效率、高质量的开发团队和个人开发者。通过 AI 代理协作和结构化工作流，显著提升开发效率和代码质量。

**与其他工具的关系**:
- **BMad-Method**: AI 原生开发平台，完整生命周期管理
- **GuDaStudio Commands**: RPI 工作流框架，专注上下文管理
- **GuDaStudio CodexMCP**: MCP 桥梁，Claude Code + Codex 协作

三者可以互补使用，共同提升开发效率。

---

**⭐ 在 GitHub 上给项目点星，支持开源！**

**🎉 欢迎加入 BMad 社区，一起 Build More, Architect Dreams！**

---

*本文档由哈雷酱整理，基于 BMad-Method V6.0.4*
