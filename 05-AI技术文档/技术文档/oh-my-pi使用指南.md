---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
created: 2026-03-03
updated: 2026-03-03
---

# oh-my-pi (OPMP) 使用指南

> 极简终端 AI 编码框架 — 会话可回溯分叉 + 工具调用可控 + 高度可扩展

**来源**: [linux.do 社区分享](https://linux.do/t/topic/1680535)

---

## 一、OPMP 是什么

### 核心定位

**pi (π)** — 极简终端编码框架
- 类似 vim 的定位:装了什么也没有,需要自己拼装
- 实现了会话可回溯分叉、工具调用可控、可扩展和嵌入的基本功能
- 默认只有 `read`、`write`、`edit`、`bash` 四个工具

**oh-my-pi (omp)** — pi 的"发行版"
- 把整个 pi 项目 fork 过来改造,集成了大量实用工具
- 类比关系: pi = Linux Kernel, omp = Ubuntu/Fedora 等发行版
- 开箱即用,内置 subagents/Task Tool、多模型角色路由、MCP、LSP、AST 等

### 与其他工具对比

| 工具 | 定位 | 特点 |
|------|------|------|
| Claude Code CLI | 官方 CLI 工具 | 全局理解、Plan Mode、Subagent |
| Codex CLI | 终端 AI 编码 | 快速迭代、工具丰富 |
| OpenCode | 开源 AI 编码 | 插件生态、oh-my-opencode |
| **oh-my-pi** | 极简编排底座 | 会话树回溯、无 sandbox、高度可定制 |

**重要警告**: omp 没有 sandbox 安全隔离机制,相当于运行 `codex --yolo` 或 `claude --dangerously-skip-permissions`!

---

## 二、核心特性

### 1. 会话可回溯分叉

**传统对话流程**:
```
用户: 写个 hello world
模型: 已生成代码
用户: 加个 "Nice to meet you"
模型: 已添加
用户: (后悔了,想改成别的)
     → 只能重新开始或手动修改
```

**pi 的会话树机制**:
```
用户: 写个 hello world
模型: 已生成代码
用户: 加个 "Nice to meet you"
模型: 已添加
用户: /tree (切回到"加内容"那个节点)
     → 重新说: 改成 "Never gonna give you up"
     → 从这个节点分叉出新的路径
```

- 每条消息/工具调用都是带 `parentId` 的节点
- 可以回溯到任意节点重新分叉
- 可以 fork 整个会话,并行尝试不同方案
- 类似 git 的分支管理思维

### 2. 多模型角色路由

可以为不同模型分配不同角色:

| 角色 | 用途 | 切换方式 |
|------|------|----------|
| **Default** | 主模型,正常聊天和工具调用 | 默认 |
| **Fast (SMOL)** | 快速/便宜的模型,处理简单任务 | Ctrl+P 切换 |
| **Thinking (SLOW)** | 慢速/强力的模型,深度思考 | Ctrl+P 切换 |
| **Architect (PLAN)** | Plan Mode 中的架构设计模型 | 自动调用 |

**示例配置**:
- Default: GPT-5.2
- Fast: Gemini-3-Flash
- Thinking: GPT-5.3-Codex
- Architect: Claude Opus

### 3. Subagents 机制

支持子代理并行处理任务:

```
主 Agent: 收到复杂任务
  ↓
创建多个 Task 子代理并行工作:
  - Task 1: 探索代码库
  - Task 2: 规划架构
  - Task 3: 实现功能
  - Task 4: 评审代码
  ↓
汇总结果返回主 Agent
```

**配置项**:
- `Task max concurrency`: 最大并发子代理数量
- `Task max recursion depth`: 子代理递归层数上限
- `Task isolation`: 隔离环境(none/worktree/fuse-overlay)

### 4. TTSR 规则系统

可以设置规则约束工具调用:

**示例**: 限制文件操作范围
```bash
# 在聊天框中说:
"帮我配置一个 TTSR 规则,要求 omp 只能在当前目录下操作文件"

# omp 会自动生成规则文件并启用
```

**用途**:
- 防止访问敏感目录
- 禁止使用 deprecated API
- 强制代码规范
- 项目级约束

### 5. LSP/AST 集成

- **LSP (Language Server Protocol)**: 代码补全、诊断、格式化
- **AST (Abstract Syntax Tree)**: 符号级代码重写
- **配置项**:
  - `Format on write`: 保存时自动格式化
  - `Diagnostics on write`: 写入后立即诊断
  - `Diagnostics on edit`: 编辑后也诊断(更频繁)

---

## 三、安装与配置

### 安装

```bash
# 使用官方安装脚本
curl -fsSL https://raw.githubusercontent.com/can1357/oh-my-pi/main/scripts/install.sh | sh
```

**终端配置**: omp 使用 Kitty keyboard protocol,可能需要额外配置终端。参见[官方文档](https://github.com/can1357/oh-my-pi?tab=readme-ov-file#terminal-setup)。

### 模型配置

创建 `models.yml` 文件:

```yaml
providers:
  your-provider:
    baseUrl: https://your-api.com/v1
    apiKey: sk-your-api-key
    models:
      - id: gpt-5.2
        name: gpt-5.2
        api: openai-responses
        reasoning: true
        input: [text, image]
        contextWindow: 400000
        maxTokens: 128000
        cost:
          input: 1.75
          output: 14.0
          cacheRead: 0.175
          cacheWrite: 0
```

**重要**: `contextWindow` 和 `maxTokens` 必须按真实情况配置,影响 compact 功能!

### 核心配置项

打开项目后,使用 `/settings` 进入配置:

#### Agent 配置
- **Thinking level**: 思考强度(off/minimal/low/medium/high/xhigh)
- **Follow-up mode**: 模型能否自己追问(one-at-a-time/all)
- **Auto-compact**: 自动压缩上下文
- **Memories**: 项目级长期记忆(从历史 session 提取经验)

#### Tools 配置
- **Eager task delegation**: 是否鼓励模型积极调用子代理
- **Task max concurrency**: 子代理并发上限
- **Skill commands**: 是否注册 skills 为快捷命令
- **MCP project config**: 是否加载项目 MCP 配置

#### Config 配置
- **Read hash lines**: 使用 hashline 格式(行号+哈希校验)
- **Hide secrets**: 脱敏敏感信息(密钥/令牌)

---

## 四、使用方式

### 基本工作流

```bash
# 1. 打开项目
cd ~/your-project
omp

# 2. 进入 Plan Mode (可选)
/plan

# 3. 描述任务
"用 HTML/CSS/JS 做一个天气卡片,iOS 18 风格"

# 4. 模型规划并执行
# - 创建计划文件
# - 询问细节
# - 生成代码
# - 调用工具

# 5. 查看会话树
/tree

# 6. 管理扩展
/extensions

# 7. 管理子代理
/agents
```

### 常用命令

| 命令 | 功能 |
|------|------|
| `/plan` | 进入/退出 Plan Mode |
| `/tree` | 查看会话树,回溯分叉 |
| `/settings` | 打开配置界面 |
| `/extensions` | 管理扩展(Skills/MCP/Commands) |
| `/agents` | 管理子代理 |
| `Ctrl+P` | 切换模型(Default/Fast/Thinking) |
| `Esc Esc` | 快捷操作(默认打开 /tree) |

### Plan Mode 工作流

```bash
# 1. 进入 Plan Mode
/plan

# 2. 描述需求
"实现用户认证系统,支持 JWT"

# 3. 模型规划
# - 创建 .omp/plans/xxx.md
# - 分析需求
# - 提出问题
# - 生成实施计划

# 4. 确认并执行
# 选择"同意并执行"
# → 开启新 session 按计划实施
```

---

## 五、核心优势

### 1. 会话管理灵活性

- 可回溯分叉,并行尝试方案
- 不怕走错路,随时回退
- 适合探索性开发

### 2. 高度可定制

- 从底层工具到上层工作流都可定制
- TTSR 规则系统约束行为
- 多模型角色路由优化成本

### 3. 工具生态完整

- LSP/AST 符号级操作
- MCP 协议集成
- Skills/Commands 扩展
- Subagents 并行处理

### 4. 可嵌入性

- 提供 RPC/SDK 接口
- 可以作为底座嵌入其他项目
- OpenClaw 就是基于 pi 构建的

---

## 六、使用建议

### 适合人群

✅ 喜欢折腾、愿意深度定制工作流的开发者
✅ 需要会话回溯分叉能力的探索性开发
✅ 想要完全掌控 AI 编码工具的用户

### 不适合人群

❌ 需要开箱即用、零配置的用户 → 推荐 Claude Code CLI
❌ 需要强安全隔离的生产环境 → omp 无 sandbox
❌ 不想学习新概念的用户 → 学习曲线较陡

### 安全注意事项

⚠️ **无 sandbox 隔离**: omp 可以执行任意命令,相当于 `--yolo` 模式
⚠️ **生产环境慎用**: 建议先在测试环境/隔离环境使用
⚠️ **TTSR 规则**: 使用规则系统约束工具调用范围
⚠️ **代码审查**: 执行前仔细审查生成的代码

---

## 七、与 Claude Code 对比

| 特性 | Claude Code CLI | oh-my-pi |
|------|----------------|----------|
| 会话管理 | 线性对话 + compact | 树状回溯分叉 |
| 安全隔离 | 权限确认机制 | 无 sandbox (yolo 模式) |
| 工具生态 | MCP + Skills | MCP + Skills + LSP/AST |
| 学习曲线 | 较平缓 | 较陡峭 |
| 定制能力 | 中等 | 极高 |
| Plan Mode | 内置 | 内置 |
| Subagents | Task tool | Task tool + 自定义 agents |
| 适用场景 | 通用开发 | 探索性开发 + 深度定制 |

---

## 八、参考资源

### 官方资源

- **oh-my-pi 仓库**: https://github.com/can1357/oh-my-pi
- **pi 原始仓库**: https://github.com/badlogic/pi-mono
- **pi 官网**: https://pi.dev
- **模型配置文档**: https://github.com/can1357/oh-my-pi/blob/main/docs/models.md

### 社区资源

- **linux.do 教程**: https://linux.do/t/topic/1680535
- **Discord 社区**: https://discord.com/invite/3cU7Bz4UPx

---

## 九、总结

oh-my-pi 是一个**极简但强大**的终端 AI 编码框架:

**核心价值**:
- 会话可回溯分叉 — 探索性开发的利器
- 高度可定制 — 从工具到工作流全面掌控
- 工具生态完整 — LSP/AST/MCP/Subagents

**使用建议**:
- 适合喜欢折腾、追求极致定制的开发者
- 需要注意安全问题(无 sandbox)
- 学习曲线较陡,但上限很高

**定位**: pi 是终端 AI 编排底座,omp 是开箱即用的发行版,适合作为 Claude Code/Codex/OpenCode 的补充或替代方案。
