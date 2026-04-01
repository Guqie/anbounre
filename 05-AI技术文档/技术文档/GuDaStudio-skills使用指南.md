---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
created: 2026-03-03
updated: 2026-03-03
---

# GuDaStudio Skills 使用指南

> Agent Skills 集合 — 让 Claude 与多模型/工具无缝协作

**来源**: [GitHub - GuDaStudio/skills](https://github.com/GuDaStudio/skills)

---

## 一、项目简介

### 核心定位

**GuDaStudio Skills** — 多模型协作框架

- 基于 Anthropic 推出的 Agent Skills 机制
- 实现 Claude 与 Codex、Gemini 的无缝协作
- 提供完整的多模型工作流框架
- 支持算法实现、Bug 分析、代码审查

### 项目数据

- **Stars**: 1.8k ⭐
- **Forks**: 93
- **许可证**: MIT
- **最后更新**: 2025-12-23 (v0.1.9)
- **开发者**: GuDaStudio

### 设计理念

**多模型协作的必要性**:
- Claude 擅长全局理解和架构设计
- Codex 擅长算法实现和逻辑调试
- Gemini 擅长前端 UI 和样式设计

**协作模式**:
- Claude 作为主控模型（Orchestrator）
- Codex/Gemini 作为专业领域执行者
- 通过 Skills 机制实现无缝调度

---

## 二、核心 Skills

### 1. collaborating-with-codex

**功能**: 将编码任务委托给 OpenAI Codex CLI

**适用场景**:
- 算法实现（复杂逻辑、数据结构）
- Bug 分析（逻辑调试、性能优化）
- 代码审查（后端逻辑审计）

**核心特性**:
- 支持多轮对话（SESSION_ID 机制）
- 返回 Unified Diff Patch
- 零文件系统写入权限

### 2. collaborating-with-gemini

**功能**: 将编码任务委托给 Google Gemini CLI

**适用场景**:
- 前端 UI/UX 设计
- CSS/React/Vue 原型
- 样式优化

**核心特性**:
- 上下文限制 < 32k tokens
- 专注视觉设计
- 返回 Unified Diff Patch

**重要警告**: Gemini 对后端逻辑理解有缺陷，其后端建议需客观审视。

### 返回值结构

**成功时**:
```json
{
  "success": true,
  "SESSION_ID": "550e8400-e29b-41d4-a716-446655440000",
  "agent_messages": "模型回复内容...",
  "all_messages": []
}
```

**失败时**:
```json
{
  "success": false,
  "error": "错误信息描述"
}
```

---

## 三、工作流框架（Global Protocols）

### 核心原则

1. **语言协议**: 与工具/模型交互用英语，与用户交互用中文
2. **会话连续性**: 使用 SESSION_ID 维持多轮对话
3. **异步操作**: 强制并行，使用 Run in background
4. **安全约束**: Codex/Gemini 零写入权限
5. **代码主权**: Claude 是最终实施者

### Phase 1: 上下文全量检索

**工具**: Auggie MCP (`mcp__auggie-mcp__codebase-retrieval`)

**执行策略**:
- 禁止基于假设回答
- 使用自然语言构建语义查询
- 完整性检查（递归检索直到上下文完整）
- 需求对齐（向用户输出引导性问题）

### Phase 2: 多模型协作分析

**分发输入**:
- 将用户原始需求分发给 Codex 和 Gemini
- 仅给出入口文件和行索引（非代码片段）

**方案迭代**:
- 要求多角度解决方案
- 交叉验证（整合各方思路）
- 迭代优化（逻辑推演和优劣势互补）
- 生成 Step-by-step 实施计划

**强制阻断 (Hard Stop)**:
- 向用户展示最终实施计划
- 必须输出："Shall I proceed with this plan? (Y/N)"
- 立即终止当前回复
- 禁止在收到 "Y" 之前执行 Phase 3

### Phase 3: 原型获取

**Route A: 前端/UI/样式 (Gemini Kernel)**
- 限制：上下文 < 32k
- 指令：请求 CSS/React/Vue 原型
- 定位：最终前端设计原型与视觉基准

**Route B: 后端/逻辑/算法 (Codex Kernel)**
- 能力：逻辑运算与 Debug
- 指令：请求逻辑实现原型

**通用约束**:
- 必须明确要求返回 Unified Diff Patch
- 严禁 Codex/Gemini 做任何真实修改

### Phase 4: 编码实施

**执行准则**:
1. **逻辑重构**: 基于原型，重写为企业发布级代码
2. **文档规范**: 非必要不生成注释，代码自解释
3. **最小作用域**: 变更仅限需求范围，强制审查副作用

### Phase 5: 审计与交付

**自动审计**:
- 变更生效后，强制立即调用 Codex 与 Gemini 同时进行 Code Review
- 整合修复建议

**交付**:
- 审计通过后反馈给用户

---

## 四、Resource Matrix（资源调度矩阵）

| Workflow Phase | Functionality | Designated Model / Tool | Input Strategy | Output Constraints | Critical Constraints |
|:--------------|:-------------|:----------------------|:--------------|:------------------|:-------------------|
| **Phase 1** | Context Retrieval | Auggie | Natural Language (English) | Raw Code / Definitions | 禁止 grep/关键词搜索；强制递归检索 |
| **Phase 2** | Analysis & Planning | Codex AND Gemini | Raw Requirements (English) | Step-by-Step Plan | 交叉验证；消除逻辑缺口 |
| **Phase 3 (Route A)** | Frontend / UI / UX | Gemini | English (< 32k tokens) | Unified Diff Patch | CSS/React/Vue 权威；忽略后端建议 |
| **Phase 3 (Route B)** | Backend / Logic | Codex | English | Unified Diff Patch | 复杂调试和算法；零写入权限 |
| **Phase 4** | Refactoring | Claude (Self) | N/A | Production Code | 最终实施者；简洁高效 |
| **Phase 5** | Audit & QA | Codex AND Gemini | Unified Diff + Target File | Review Comments | 变更后立即触发；整合反馈 |

---

## 五、安装与使用

### 前置要求

**必需工具**:
- Python 3.8+ (开发测试版本: 3.10)
- Claude Code CLI
- OpenAI Codex CLI (可选)
- Google Gemini CLI (可选)

### 安装步骤

**1. 克隆仓库**:
```bash
git clone --recursive https://github.com/GuDaStudio/skills.git
cd skills
```

**2. 运行安装脚本**:

**Linux / macOS**:
```bash
./install.sh
```

**Windows (PowerShell)**:
```powershell
.\install.ps1
```

**3. 验证安装**:
- 启动 Claude Code
- Skills 会自动加载
- 可通过 `/skills` 命令查看已安装的 Skills

### 配置提示词（强烈推荐）

在 `~/.claude/CLAUDE.md` 中配置/追加 Global Protocols 提示词（见上文"工作流框架"部分）。

**重要**: 该提示词使用了 auggie-mcp，需先安装配置。

---

## 六、核心优势

### 1. 多模型协作

- Claude 全局理解 + Codex 逻辑实现 + Gemini UI 设计
- 交叉验证消除逻辑缺口
- 各模型发挥专长

### 2. 完整工作流

- 5 个 Phase 覆盖完整开发流程
- 强制阻断机制确保用户控制
- 自动审计保证代码质量

### 3. 安全约束

- Codex/Gemini 零写入权限
- 仅返回 Unified Diff Patch
- Claude 作为最终实施者

### 4. 会话管理

- SESSION_ID 机制支持多轮对话
- 上下文连续性
- 异步并行执行

---

## 七、与其他技能库对比

| 特性 | GuDaStudio Skills | Baoyu Skills | knowledge-butler |
|------|------------------|--------------|------------------|
| 核心功能 | 多模型协作框架 | 通用工具集 | 知识库管理 |
| 模型支持 | Claude + Codex + Gemini | Claude | Claude |
| 工作流 | 5 Phase 完整流程 | 独立 Skills | 知识管理流程 |
| 适用场景 | 复杂开发任务 | 日常开发辅助 | 文档管理 |
| 学习曲线 | 较陡峭 | 平缓 | 平缓 |
| 安装方式 | 一键脚本 | 手动/脚本 | 手动 |

---

## 八、使用建议

### 适合人群

✅ 需要多模型协作的复杂项目
✅ 追求代码质量和架构设计的开发者
✅ 愿意学习完整工作流的用户
✅ 有 Codex/Gemini API 的用户

### 不适合人群

❌ 简单任务场景（过度设计）
❌ 不想配置复杂提示词的用户
❌ 只使用 Claude 的用户

### 核心价值

1. **多模型协作**: 发挥各模型专长
2. **完整工作流**: 从需求到交付的闭环
3. **质量保证**: 自动审计机制
4. **安全可控**: 用户始终掌控决策权

---

## 九、集成建议

### 与现有知识库集成

**方案 1: 直接安装**
```bash
cd ~/.claude/skills
git clone --recursive https://github.com/GuDaStudio/skills.git guda-skills
```

**方案 2: 符号链接**
```bash
# 克隆到外部目录
git clone --recursive https://github.com/GuDaStudio/skills.git ~/guda-skills

# 创建符号链接
ln -s ~/guda-skills ~/.claude/skills/guda-skills
```

**方案 3: Submodule 管理**
```bash
cd ~/.claude/skills
git submodule add https://github.com/GuDaStudio/skills.git guda-skills
git submodule update --init --recursive
```

### 与 Baoyu Skills 共存

- GuDaStudio Skills 专注多模型协作
- Baoyu Skills 提供通用工具
- 两者互补，可同时使用

### 配置优先级

1. 在 `~/.claude/CLAUDE.md` 中配置 Global Protocols
2. 确保 auggie-mcp 已安装
3. 配置 Codex/Gemini CLI（如需使用）
4. 测试 Skills 是否正常加载

---

## 十、FAQ

### Q1: 什么是 Agent Skills？

Agent Skills 是 Anthropic 推出的模块化能力扩展机制，让 LLM 能够按需加载专业领域知识与工作流。

### Q2: 是否需要额外付费？

- Claude Code 本身需要订阅
- 如使用 Codex/Gemini，需对应 API 费用
- Skills 本身开源免费（MIT 许可证）

### Q3: 多轮对话时 SESSION_ID 有什么作用？

SESSION_ID 用于维持上下文连续性，确保后续请求能够访问之前的对话历史。

### Q4: 如何确保代码安全？

- Codex/Gemini 零写入权限
- 仅返回 Unified Diff Patch
- Claude 作为最终实施者，人工审查后再应用

---

## 十一、参考资源

### 官方资源

- **GitHub 仓库**: https://github.com/GuDaStudio/skills
- **官方网站**: https://code.guda.studio
- **Anthropic Skills 文档**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

### 相关工具

- **Auggie MCP**: 上下文检索工具
- **OpenAI Codex CLI**: 后端逻辑协作
- **Google Gemini CLI**: 前端 UI 协作

---

## 十二、总结

GuDaStudio Skills 是一个**专业且强大**的多模型协作框架：

**核心价值**:
- 多模型协作 — Claude + Codex + Gemini 各展所长
- 完整工作流 — 5 Phase 覆盖开发全流程
- 质量保证 — 自动审计机制
- 安全可控 — 用户掌控决策权

**使用建议**:
- 适合复杂项目和追求质量的开发者
- 需要学习完整工作流框架
- 与 Baoyu Skills 互补使用

**定位**: 专业的多模型协作框架，适合作为 Claude Code 的高级扩展，提升复杂项目的开发效率和代码质量。

---

**⭐ 在 GitHub 上给项目点星，支持开源！**
