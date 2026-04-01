---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
created: 2026-03-03
updated: 2026-03-03
---

# GuDaStudio CodexMCP 使用指南

> 让 Claude Code 与 Codex 无缝协作

**来源**: [GitHub - GuDaStudio/codexmcp](https://github.com/GuDaStudio/codexmcp)

---

## 一、项目简介

### 核心定位

**CodexMCP** — Claude Code 与 Codex 之间的协作桥梁

- 通过 MCP 协议让 Claude Code 和 Codex 优势互补
- Claude Code 负责架构设计与全局思考
- Codex 负责代码生成与细节优化
- CodexMCP 管理会话上下文，支持多轮对话与并行任务

### 项目数据

- **Stars**: 1.6k ⭐
- **Forks**: 84
- **许可证**: MIT
- **最后更新**: 2026-01-13
- **开发者**: GuDaStudio
- **语言**: Python 100%

### 设计理念

**核心问题**: AI 辅助编程生态中，不同 AI 模型各有专长

**解决方案**:
- **Claude Code**: 擅长需求分析、架构规划、代码重构
- **Codex**: 擅长算法实现、bug 定位、代码审查
- **CodexMCP**: 作为桥梁，管理会话上下文，支持多轮对话与并行任务

**企业级特性**:
- 会话持久化（多轮对话支持）
- 并行执行（多任务隔离）
- 推理追踪（详细的推理过程）
- 错误处理（完善的异常处理机制）

---

## 二、与官方版本对比

### 核心差异

| 特性 | 官方 Codex MCP | GuDaStudio CodexMCP |
|------|---------------|-------------------|
| 基本 Codex 调用 | ✅ | ✅ |
| 多轮对话 | ❌ | ✅ |
| 推理详情追踪 | ❌ | ✅ |
| 并行任务支持 | ❌ | ✅ |
| 错误处理 | ❌ | ✅ |

### 功能详解

**1. 多轮对话**:
- 官方版：每次调用都是独立的，无法保持上下文
- CodexMCP：通过 SESSION_ID 机制支持多轮对话，保持上下文连续性

**2. 推理详情追踪**:
- 官方版：仅返回最终结果
- CodexMCP：可选返回完整推理过程、工具调用等详细信息

**3. 并行任务支持**:
- 官方版：不支持并行调用
- CodexMCP：每个调用使用独立 SESSION_ID，完全隔离，支持并行

**4. 错误处理**:
- 官方版：错误处理不完善
- CodexMCP：完善的异常处理机制，返回详细错误信息

---

## 三、安装与配置

### 前置要求

**必需工具**:
- Claude Code v2.0.56+
- Codex CLI v0.61.0+
- uv 工具（Python 包管理器）

**安装 uv 工具**:

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux / macOS**:
```bash
# 使用 curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

**重要提示**: 强烈推荐 Windows 用户在 WSL 中运行本项目

### 安装步骤

**Step 1**: 移除官方 Codex MCP（如果已安装）

```bash
claude mcp remove codex
```

**Step 2**: 安装 CodexMCP

```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

**Step 3**: 验证安装

在终端中运行：
```bash
claude mcp list
```

如果看到以下描述，说明安装成功：
```
codex: uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp - ✓ Connected
```

**Step 4**: 可选配置自动允许

在 `~/.claude/settings.json` 中添加 `mcp__codex__codex` 到 allow 项，允许 Claude Code 自动与 Codex 交互。

---

## 四、工具参数详解

### codex 工具参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `PROMPT` | `str` | ✅ | - | 发送给 Codex 的任务指令 |
| `cd` | `Path` | ✅ | - | Codex 工作目录根路径 |
| `sandbox` | `Literal` | ❌ | `"read-only"` | 沙箱策略：`read-only` / `workspace-write` / `danger-full-access` |
| `SESSION_ID` | `UUID \| None` | ❌ | `None` | 会话 ID（None 则开启新会话） |
| `skip_git_repo_check` | `bool` | ❌ | `False` | 是否允许在非 Git 仓库运行 |
| `return_all_messages` | `bool` | ❌ | `False` | 是否返回完整推理信息 |
| `image` | `List[Path] \| None` | ❌ | `None` | 附加图片文件到初始提示词 |
| `model` | `str \| None` | ❌ | `None` | 指定使用的模型（默认使用用户配置） |
| `yolo` | `bool \| None` | ❌ | `False` | 无需审批运行所有命令（跳过沙箱） |
| `profile` | `str \| None` | ❌ | `None` | 从 `~/.codex/config.toml` 加载的配置文件名称 |

### 返回值结构

**成功时**:
```json
{
  "success": true,
  "SESSION_ID": "550e8400-e29b-41d4-a716-446655440000",
  "agent_messages": "Codex 的回复内容...",
  "all_messages": [...]  // 仅当 return_all_messages=True 时包含
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

## 五、使用方法与最佳实践

### 基础使用

**开启新对话**:
```python
# 不传 SESSION_ID 参数（或传 None）
# 工具会返回新的 SESSION_ID 用于后续对话
```

**继续之前的对话**:
```python
# 将之前返回的 SESSION_ID 作为参数传入
# 同一会话的上下文会被保留
```

### 调用规范

**必须遵守**:
- 每次调用 codex 工具时，必须保存返回的 SESSION_ID，以便后续继续对话
- cd 参数必须指向存在的目录，否则工具会静默失败
- 严禁 codex 对代码进行实际修改，使用 `sandbox="read-only"` 以避免意外
- 要求 codex 仅给出 unified diff patch

**推荐用法**:
- 如需详细追踪 codex 的推理过程和工具调用，设置 `return_all_messages=True`
- 对于精准定位、debug、代码原型快速编写等任务，优先使用 codex 工具

### 注意事项

- **会话管理**: 始终追踪 SESSION_ID，避免会话混乱
- **工作目录**: 确保 cd 参数指向正确且存在的目录
- **错误处理**: 检查返回值的 success 字段，处理可能的错误

---

## 六、推荐提示词配置

### CLAUDE.md 配置

在 `~/.claude/CLAUDE.md` 中添加以下内容，让 Claude Code 更好地与 Codex 协作：

```markdown
## Core Instruction for CodeX MCP

在任何时刻，你必须思考当前过程可以如何与codex进行协作，如何调用Codex 为你提供的MCP工具作为你客观全面分析的保障。
其中你**务必执行**以下几个步骤：

**1** 在你对用户需求形成初步分析后，将用户需求、初始思路告知codex，并要求其完善需求分析和实施计划。

**2** 在实施具体编码任务前，**必须向codex索要代码实现原型（要求codex仅给出unified diff patch，严禁对代码做任何真实修改）**。在获取代码原型后，你**只能以此为逻辑参考，再次对代码修改进行重写**，形成企业生产级别、可读性极高、可维护性极高的代码后，才能实施具体编程修改任务。

**3** 无论何时，只要完成切实编码行为后，**必须立即使用codex review代码改动和对应需求完成程度**。

**4** codex只能给出参考，你**必须有自己的思考，甚至需要对codex的回答提出置疑**。尽信书则不如无书，你与codex的最终使命都是达成统一、全面、精准的意见，所以你们必须不断争辩已找到通向真理的唯一途径。


## Codex Tool Invocation Specification

1. 工具概述

codex MCP 提供了一个工具 `codex`，用于执行 AI 辅助的编码任务。该工具**通过 MCP 协议调用**，无需使用命令行。

2. 工具参数

**必选**参数：
- PROMPT (string): 发送给 codex 的任务指令
- cd (Path): codex 执行任务的工作目录根路径

可选参数：
- sandbox (string): 沙箱策略，可选值：
  - "read-only" (默认): 只读模式，最安全
  - "workspace-write": 允许在工作区写入
  - "danger-full-access": 完全访问权限
- SESSION_ID (UUID | null): 用于继续之前的会话以与codex进行多轮交互，默认为 None（开启新会话）
- skip_git_repo_check (boolean): 是否允许在非 Git 仓库中运行，默认 False
- return_all_messages (boolean): 是否返回所有消息（包括推理、工具调用等），默认 False
- image (List[Path] | null): 附加一个或多个图片文件到初始提示词，默认为 None
- model (string | null): 指定使用的模型，默认为 None（使用用户默认配置）
- yolo (boolean | null): 无需审批运行所有命令（跳过沙箱），默认 False
- profile (string | null): 从 `~/.codex/config.toml` 加载的配置文件名称，默认为 None（使用用户默认配置）

返回值：
{
  "success": true,
  "SESSION_ID": "uuid-string",
  "agent_messages": "agent回复的文本内容",
  "all_messages": []  // 仅当 return_all_messages=True 时包含
}
或失败时：
{
  "success": false,
  "error": "错误信息"
}

3. 使用方式

开启新对话：
- 不传 SESSION_ID 参数（或传 None）
- 工具会返回新的 SESSION_ID 用于后续对话

继续之前的对话：
- 将之前返回的 SESSION_ID 作为参数传入
- 同一会话的上下文会被保留

4. 调用规范

**必须遵守**：
- 每次调用 codex 工具时，必须保存返回的 SESSION_ID，以便后续继续对话
- cd 参数必须指向存在的目录，否则工具会静默失败
- 严禁codex对代码进行实际修改，使用 sandbox="read-only" 以避免意外，并要求codex仅给出unified diff patch即可

推荐用法：
- 如需详细追踪 codex 的推理过程和工具调用，设置 return_all_messages=True
- 对于精准定位、debug、代码原型快速编写等任务，优先使用 codex 工具

5. 注意事项

- 会话管理：始终追踪 SESSION_ID，避免会话混乱
- 工作目录：确保 cd 参数指向正确且存在的目录
- 错误处理：检查返回值的 success 字段，处理可能的错误
```

---

## 七、协作工作流

### Claude Code + Codex 协作模式

```
用户需求
  ↓
Claude Code 初步分析
  ↓
调用 Codex 完善需求分析和实施计划
  ↓
Claude Code 整合方案
  ↓
调用 Codex 生成代码原型（unified diff patch）
  ↓
Claude Code 重构为生产级代码
  ↓
实施代码修改
  ↓
调用 Codex review 代码改动
  ↓
Claude Code 整合反馈并优化
  ↓
完成
```

### 四步协作法

**Step 1: 需求分析**
- Claude Code 对用户需求形成初步分析
- 调用 Codex 完善需求分析和实施计划
- Claude Code 整合方案

**Step 2: 代码原型**
- 调用 Codex 生成代码实现原型
- 要求 Codex 仅给出 unified diff patch
- 严禁 Codex 对代码做任何真实修改

**Step 3: 代码实施**
- Claude Code 以 Codex 原型为逻辑参考
- 重写为企业生产级别、高可读性、高可维护性的代码
- 实施具体编程修改任务

**Step 4: 代码审查**
- 完成编码后，立即调用 Codex review 代码改动
- 检查需求完成程度
- Claude Code 整合反馈并优化

### 协作原则

1. **Codex 只能给出参考**: Claude Code 必须有自己的思考
2. **批判性思维**: 甚至需要对 Codex 的回答提出质疑
3. **争辩求真**: 不断争辩以找到通向真理的唯一途径
4. **达成共识**: 最终使命是达成统一、全面、精准的意见

---

## 八、核心优势

### 1. 会话持久化

- 通过 SESSION_ID 机制支持多轮对话
- 保持上下文连续性
- 避免重复传递信息

### 2. 并行执行

- 每个调用使用独立 SESSION_ID
- 完全隔离，互不干扰
- 支持多任务并行处理

### 3. 推理追踪

- 可选返回完整推理过程
- 详细的工具调用信息
- 便于调试和优化

### 4. 错误处理

- 完善的异常处理机制
- 返回详细错误信息
- 提升系统稳定性

### 5. 优势互补

- Claude Code 擅长架构设计与全局思考
- Codex 擅长代码生成与细节优化
- CodexMCP 作为桥梁，让两者协作更高效

---

## 九、使用建议

### 适合人群

✅ 使用 Claude Code 和 Codex 的开发者
✅ 需要多 AI 模型协作的场景
✅ 追求代码质量和架构设计的专业开发者
✅ 需要多轮对话和并行任务的用户

### 不适合人群

❌ 只使用 Claude Code 的用户
❌ 不需要 Codex 协作的简单场景
❌ 不关心代码质量的快速原型场景

### 核心价值

1. **多 AI 协作**: Claude Code + Codex 优势互补
2. **会话持久化**: 多轮对话，保持上下文
3. **并行执行**: 多任务隔离，互不干扰
4. **推理追踪**: 详细的推理过程，便于调试
5. **企业级特性**: 完善的错误处理机制

### 最佳实践

**1. 推荐配置**:
- Claude Code v2.0.56+
- Codex CLI v0.61.0+
- 配置 CLAUDE.md 提示词

**2. 会话管理**:
- 始终追踪 SESSION_ID
- 避免会话混乱
- 合理使用多轮对话

**3. 安全约束**:
- 使用 `sandbox="read-only"`
- 要求 Codex 仅给出 unified diff patch
- 严禁 Codex 对代码做真实修改

**4. 协作原则**:
- Codex 只能给出参考
- Claude Code 必须有自己的思考
- 批判性思维，争辩求真

---

## 十、FAQ

### Q1: 是否需要额外付费？

CodexMCP 本身完全免费开源，无需任何额外付费！

### Q2: 并行调用会冲突吗？

不会。每个调用使用独立的 SESSION_ID，完全隔离。

### Q3: 与官方 Codex MCP 有什么区别？

CodexMCP 引入了会话持久化、并行执行、推理追踪和错误处理等企业级特性，让协作更智能高效。

### Q4: 如何保持多轮对话？

每次调用时保存返回的 SESSION_ID，后续调用时传入该 ID 即可继续对话。

### Q5: 如何确保代码安全？

- 使用 `sandbox="read-only"` 沙箱策略
- 要求 Codex 仅给出 unified diff patch
- Claude Code 作为最终实施者，人工审查后再应用

---

## 十一、参考资源

### 官方资源

- **GitHub 仓库**: https://github.com/GuDaStudio/codexmcp
- **官方网站**: https://code.guda.studio
- **英文文档**: https://github.com/GuDaStudio/codexmcp/blob/main/docs/README_EN.md

### 相关工具

- **Claude Code**: AI 编码助手
  - 官方文档: https://docs.claude.com/docs/claude-code
- **Codex CLI**: OpenAI Codex 命令行工具
  - 官方文档: https://developers.openai.com/codex/quickstart
- **uv**: Python 包管理器
  - 官方文档: https://docs.astral.sh/uv/

### 相关项目

- **GuDaStudio Skills**: 多模型协作框架
  - GitHub: https://github.com/GuDaStudio/skills
- **GuDaStudio Commands**: RPI 工作流框架
  - GitHub: https://github.com/GuDaStudio/commands

---

## 十二、总结

GuDaStudio CodexMCP 是一个**实用且强大**的 MCP 桥梁工具：

**核心价值**:
- 多 AI 协作 — Claude Code + Codex 优势互补
- 会话持久化 — 多轮对话，保持上下文
- 并行执行 — 多任务隔离，互不干扰
- 推理追踪 — 详细的推理过程，便于调试
- 企业级特性 — 完善的错误处理机制

**使用建议**:
- 适合使用 Claude Code 和 Codex 的开发者
- 需要配置 CLAUDE.md 提示词
- 遵循四步协作法（需求分析 → 代码原型 → 代码实施 → 代码审查）
- 使用 `sandbox="read-only"` 确保安全

**定位**: 专业的 MCP 桥梁工具，让 Claude Code 与 Codex 无缝协作，从单一 Agent 转变为多 Agent 协作，显著提升生产力。

**与其他 GuDaStudio 项目的关系**:
- **CodexMCP**: MCP 桥梁，让 Claude Code 与 Codex 协作
- **Skills**: 多模型协作框架（Claude + Codex + Gemini）
- **Commands**: RPI 工作流框架（Research → Plan → Implementation）

三者可以互补使用，共同提升开发效率和代码质量。

---

**⭐ 在 GitHub 上给项目点星，支持开源！**
