---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# OpenClaw 大师课：从入门到精通

> 适用于 OpenClaw v2.23+
> 
> Node.js ≥ 22，支持 macOS / Linux / Windows（WSL2）

---

## 零、安装与初始化

### 安装

```bash
# 全局安装（任选其一）
npm install -g openclaw@latest
pnpm add -g openclaw@latest

# 启动安装向导（推荐）
openclaw onboard --install-daemon
```

向导会引导你完成：选择 AI 模型、连接消息渠道（Telegram / WhatsApp / Discord 等）、安装 Gateway 守护进程。

**Windows 用户：** 强烈推荐在 WSL2 下运行，体验与 Linux 一致。

### 目录结构

```
~/.openclaw/
├── openclaw.json          # 主配置文件
├── credentials/           # API Keys（chmod 600）
│   ├── anthropic
│   ├── openai
│   └── whatsapp/
└── workspace/             # Agent 的"大脑"
    ├── AGENTS.md          # 工作规范（每次会话都会加载）
    ├── SOUL.md            # Agent 性格与价值观
    ├── IDENTITY.md        # Agent 对外身份（名字、emoji）
    ├── USER.md            # 用户信息与偏好
    ├── MEMORY.md          # 长期记忆索引
    ├── TOOLS.md           # 本地工具说明
    ├── HEARTBEAT.md       # 定时心跳任务清单
    ├── BOOTSTRAP.md       # 首次运行初始化脚本（用完即删）
    ├── memory/            # 每日日志
    │   ├── 2026-02-25.md
    │   └── 2026-02-26.md
    └── skills/            # 自定义 Skill
```

> workspace 路径可在 `openclaw.json` 中通过 `agents.defaults.workspace` 自定义，默认 `~/.openclaw/workspace`。

### 最小可用配置

安装后编辑 `~/.openclaw/openclaw.json`：

```json
{
  "agent": {
    "model": "anthropic/claude-sonnet-4-6",
    "workspace": "~/.openclaw/workspace"
  },
  "channels": {
    "telegram": {
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_TELEGRAM_USER_ID"]
    }
  }
}
```

配置文件支持 JSON5（可以写注释和尾逗号）。修改后 Gateway 会自动热加载，大多数配置无需重启。

### 验证安装

```bash
openclaw doctor        # 检查配置问题并自动修复
openclaw status        # 查看 Gateway 运行状态
openclaw health        # 请求 Gateway 健康快照
```

---

## 一、Workspace 核心文件配置

Agent 每次启动都是全新状态，workspace 文件是它的记忆和行为规范。以下是各文件的作用和写法。

### [BOOTSTRAP.md](http://BOOTSTRAP.md) — 首次初始化

**仅使用一次。** 安装完成后，第一条消息发送：

```
嘿，让我们先完成初始化。请读取 BOOTSTRAP.md 并引导我完成配置。
```

Agent 会读取 [BOOTSTRAP.md](http://BOOTSTRAP.md)，引导你完成身份设置（命名、性格定义、填写 [USER.md](http://USER.md)），然后**自动删除**该文件。如果跳过这一步直接发问，Agent 将不知道自己是谁、用户是谁。

### [SOUL.md](http://SOUL.md) — Agent 性格

定义 Agent 的行为哲学，不是配置而是价值观。每次会话都会加载。

```markdown
# SOUL.md

## 核心原则
- 真正有用，而非表演有用。跳过"好问题！"，直接帮忙。
- 允许有观点。可以不同意，可以有偏好，不是没有个性的搜索引擎。
- 先尝试解决，再提问。读文件，看上下文，自己想清楚再开口。
- 不说"我做不到"，除非真的做不到——先试试。

## 禁止行为
- 🚫 谄媚开场（"这个问题很棒！"）
- 🚫 无意义填充（"当然，我很乐意……"）
- 🚫 把不确定性隐藏起来
```

### [USER.md](http://USER.md) — 用户信息

告诉 Agent 你是谁，这些信息会影响它的每一条回复。

```markdown
# USER.md

## 基本信息
- 姓名：张三
- 时区：Asia/Shanghai
- 工作：后端开发，主用 Python / Go

## 偏好
- 回复风格：直接、技术向，不需要铺垫
- 语言：中文，代码和技术术语保持英文
- 不喜欢：过度解释，废话

## 当前关注
- 项目：重构用户认证系统
- 学习：Rust 所有权模型
```

### [IDENTITY.md](http://IDENTITY.md) — 对外身份

Agent 的名字和 emoji，会显示在它发出的消息前缀和已读回执上。通常由 BOOTSTRAP 自动创建。

```markdown
# IDENTITY.md

name: Aria
emoji: 🦞
role: 个人助理
vibe: 高效、直接、偶尔毒舌
```

身份解析优先级：`openclaw.json` > `agents.list[].identity` > `IDENTITY.md` > 默认值"Assistant"。

### [TOOLS.md](http://TOOLS.md) — 工具说明

不控制工具可用性（那是 `openclaw.json` 的工作），只是给 Agent 的备忘录，说明本地环境的约定。

```markdown
# TOOLS.md

## 模型偏好
- 规划/思考：claude-opus
- 代码：claude-sonnet

## 服务器
- prod: user@123.45.67.89（SSH）
- staging: user@staging.example.com

## 本地约定
- Python 项目使用 uv 管理依赖
- 不使用 sudo，使用 doas
```

### [HEARTBEAT.md](http://HEARTBEAT.md) — 心跳任务

Gateway 默认每 30 分钟触发一次心跳，Agent 读取 [HEARTBEAT.md](http://HEARTBEAT.md) 的清单，决定是否需要执行操作。保持简短，否则会烧 token。

```markdown
# HEARTBEAT.md

- 检查今日是否有日历事项在 2 小时内，有则提醒
- 如果是周一早上，发送本周工作规划摘要
```

心跳频率可在 `openclaw.json` 调整：

```json
{
  "agent": {
    "heartbeat": { "every": "1h" }
  }
}
```

---

## 二、[AGENTS.md](http://AGENTS.md) — 工作规范

基础文件解决了"AI 是谁"和"用户是谁"，[AGENTS.md](http://AGENTS.md) 解决"AI 如何工作"：启动流程、记忆写入规则、操作权限。

**文件位置：** `~/.openclaw/workspace/AGENTS.md`

### Session 启动流程

```markdown
## Session 启动流程

每次会话开始时，按序自动执行（无需询问）：

1. 读取 `SOUL.md`
2. 读取 `USER.md`
3. 读取 `memory/YYYY-MM-DD.md`（今天 + 昨天）
4. 主会话额外读取 `MEMORY.md`
```

> 会话类型由 OpenClaw 自动识别：主会话、群聊会话、子 Agent 会话、Cron 会话。

### 记忆分层结构

|层级|文件|内容|
|---|---|---|
|索引层|`MEMORY.md`|核心信息索引，保持 < 40 行|
|项目层|`memory/projects.md`|项目状态与待办|
|基础设施层|`memory/infra.md`|服务器、API、部署配置|
|经验层|`memory/lessons.md`|问题与解决方案|
|日志层|`memory/YYYY-MM-DD.md`|每日原始记录|

### 日志写入规范

**格式模板：**

```
【项目：名称】事件标题
结果：一句话概括
相关文件：文件路径
经验教训：要点（如有）
检索标签：#tag1 #tag2
```

**写入原则：** 记结论，不记过程；重要信息必须落文件，不依赖上下文记忆。

**对比示例：**

```markdown
# ❌ 低质量
今天配置了服务器，先试了方案 A 不行，又试了方案 B 还是有问题，
最后用了方案 C 花了两个小时搞定了。

# ✅ 高质量
【项目:WebApp】Nginx 反向代理部署完成
结果：使用 Nginx 反向代理，监听 443 端口，部署成功
相关文件：/etc/nginx/sites-available/webapp.conf
经验教训：方案 A/B 因端口冲突失败，必须走反向代理
检索标签：#webapp #nginx #deploy
```

### 安全权限配置

```markdown
## 安全规范

可自由执行：读取文件、搜索网络、在 workspace 内工作
需要确认：发送邮件/消息、删除或修改重要文件、任何外发数据的操作
文件删除：使用 `trash` 而非 `rm`

群聊规范：可访问用户文件和记忆，但不能在群聊中分享；你是参与者，不是用户代言人。
```

---

## 三、记忆系统优化

### 问题一：长对话失忆 → 启用 memoryFlush

当对话接近上下文窗口上限时，OpenClaw 会触发 compaction 压缩旧对话。memoryFlush 在压缩前先让 AI 将重要信息写入文件，防止丢失。

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

> `softThresholdTokens: 4000`：剩余空间低于 4000 tokens 时触发。太小（< 1000）AI 没足够空间写入，太大（> 10000）触发过频。memoryFlush 静默执行，发送 `/verbose` 可查看触发日志（`Auto-compaction complete`）。

### 问题二：检索命中率低 → 优化 Embedding 模型

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "remote": {
      "baseUrl": "<https://api.siliconflow.cn/v1>",
      "apiKey": "YOUR_API_KEY"
    },
    "model": "BAAI/bge-m3"
  }
}
```

**选择 bge-m3 的原因：** SiliconFlow 提供免费额度，中英文混合支持良好，向量维度 1024，精度与速度平衡。

**memorySearch 工作流：**

```
query → memory_search("关键词") → 返回文件路径+行号 → memory_get(path, from, lines) → 读取内容
```

两步设计：search 负责定位，get 负责读取，避免全量加载记忆文件。

### 问题三：记忆文件噪音积累 → 配置自动维护

在 `workspace/HEARTBEAT.md` 中添加：

```markdown
## 记忆维护任务（每周执行）

检查 `memory/heartbeat-state.json` 中的 `lastMemoryMaintenance`。
距今超过 7 天时执行：

1. 读取最近 7 天日志
2. 提炼长期价值信息 → 归档到 projects.md / lessons.md
3. 压缩已完成的一次性任务为单行总结
4. 删除完全过期的临时信息
5. 更新 `lastMemoryMaintenance` 为当前日期
```

创建 `workspace/memory/heartbeat-state.json`：

```json
{
  "lastMemoryMaintenance": "2026-02-26"
}
```

---

## 四、子 Agent — 并行任务

### 配置

```json
{
  "agents": {
    "defaults": {
      "subAgents": {
        "enabled": true,
        "maxConcurrent": 3,
        "timeout": 300000
      }
    }
  }
}
```

> `maxConcurrent` 推荐 3-5：过小无并行优势，过大触发 API 速率限制。

### 适用场景

|适合并行|不适合并行|
|---|---|
|收集 N 个网站信息|需要连贯性的写作任务|
|批量处理独立文件|有依赖关系的串行任务|
|多服务状态检查|需要前序结果的分析|

AI 会自动判断是否并行，也可显式指定："使用子 Agent 并行处理这个任务..."

---

## 五、Cron — 定时自动化

### 配置格式

```json
{
  "name": "daily-briefing",
  "schedule": "0 8 * * *",
  "timezone": "Asia/Shanghai",
  "task": {
    "type": "message",
    "content": "发送今日简报：天气、日程、昨日工作总结、今日待办"
  },
  "enabled": true
}
```

**常用 Cron 表达式：**

|表达式|含义|
|---|---|
|`0 8 * * *`|每天 08:00|
|`0 18 * * 1-5`|工作日 18:00|
|`0 17 * * 5`|每周五 17:00|
|`*/30 * * * *`|每 30 分钟|

> 验证表达式：[crontab.guru](https://crontab.guru/)

### 管理命令

```bash
openclaw cron list                      # 查看所有任务
openclaw cron run daily-briefing        # 手动触发（测试用）
openclaw cron enable/disable <name>     # 启用/禁用
openclaw cron remove <name>             # 删除
```

**最佳实践：** 创建后先 `cron run` 手动测试，确认无误再启用。任务内容要具体，写明"发送简报：天气、日程、新闻"而非仅"发送简报"。

---

## 六、Skill — 能力扩展

### 文件结构

```
workspace/skills/my-skill/
├── SKILL.md       # 功能说明、使用方法、输出格式
├── config.json    # 可配置参数
└── templates/     # 模板文件（可选）
```

### config.json 示例

```json
{
  "name": "weather-check",
  "version": "1.0.0",
  "description": "查询城市天气",
  "config": {
    "apiKey": "YOUR_API_KEY",
    "apiUrl": "<https://api.openweathermap.org/data/2.5/weather>",
    "defaultCity": "Beijing"
  }
}
```

### 安装与使用

```bash
openclaw skill install ./workspace/skills/my-skill
```

调用时对 Agent 说：`使用 weather-check Skill 查询上海天气`

社区 Skill 可在 [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) 找到，直接通过 URL 安装。

---

## 七、多渠道部署

### 渠道配置

```json
{
  "channels": {
    "telegram": {
      "token": "BOT_TOKEN",
      "allowFrom": ["+8613800000000"]
    },
    "discord": {
      "token": "BOT_TOKEN",
      "allowedChannels": ["CHANNEL_ID"],
      "dmPolicy": "pairing"
    },
    "webchat": {
      "port": 3000,
      "auth": { "mode": "token", "token": "YOUR_PASSWORD" }
    }
  }
}
```

**dmPolicy: "pairing"**：陌生人首次 DM 会收到配对码，需手动批准才能正常对话，防止未授权访问。

### 群聊沙箱隔离

群组/频道中建议开启沙箱，防止群内成员通过 Agent 访问你的文件系统：

```json
{
  "agents": {
    "defaults": {
      "sandbox": { "mode": "non-main" }
    }
  }
}
```

### 消息路由

```json
{
  "routing": {
    "rules": [
      { "type": "alert", "destinations": ["telegram", "discord"] },
      { "type": "daily-briefing", "destinations": ["telegram"] },
      { "type": "log", "destinations": ["file"] }
    ]
  }
}
```

---

## 八、性能调优

### 模型配置

```json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-sonnet-4-6",
      "fallbacks": ["openai/gpt-4o"]
    }
  }
}
```

**temperature 选择：**

|场景|推荐值|
|---|---|
|代码生成、数据分析|0.3 – 0.5|
|日常对话、内容创作|0.7 – 0.8|
|创意写作、头脑风暴|0.9 – 1.0|

### 成本控制

```json
{
  "agents": {
    "defaults": {
      "cache": { "enabled": true, "ttl": 3600 },
      "compaction": { "targetTokens": 50000 }
    }
  },
  "billing": {
    "limits": { "daily": 10.00, "monthly": 200.00 },
    "alerts": { "enabled": true, "thresholds": [0.5, 0.8, 0.95] }
  }
}
```

**降成本策略：** 启用缓存 → 简单任务用轻量模型（`claude-haiku` / `gpt-4o-mini`）→ 精简系统提示 → 设置每日限额。

```bash
openclaw stats --period 7d   # 查看 7 天使用统计
```

---

## 完整配置速查

```json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-sonnet-4-6",
      "fallbacks": ["openai/gpt-4o"]
    },
    "workspace": "~/.openclaw/workspace",
    "heartbeat": { "every": "30m" }
  },
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": { "enabled": true, "softThresholdTokens": 4000 }
      },
      "subAgents": { "enabled": true, "maxConcurrent": 3, "timeout": 300000 },
      "cache": { "enabled": true, "ttl": 3600 },
      "sandbox": { "mode": "non-main" }
    }
  },
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "remote": {
      "baseUrl": "<https://api.siliconflow.cn/v1>",
      "apiKey": "YOUR_API_KEY"
    },
    "model": "BAAI/bge-m3"
  },
  "billing": {
    "limits": { "daily": 10.00, "monthly": 200.00 }
  }
}
```

---

## 疑难排查

|问题|排查步骤|
|---|---|
|安装后 Agent 不响应|`openclaw doctor --fix` → 检查 `allowFrom` 白名单 → `openclaw status`|
|BOOTSTRAP 没有自动执行|手动发送"读取 [BOOTSTRAP.md](http://BOOTSTRAP.md) 并引导我完成配置"|
|memoryFlush 未触发|确认 `enabled: true` → 启用 `/verbose` → 进行 100+ 轮对话测试|
|子 Agent 失败|降低 `maxConcurrent` → 增加 `timeout` → 确认任务适合并行|
|Cron 未执行|用 crontab.guru 验证表达式 → 检查 timezone → `openclaw cron list`|
|memorySearch 无结果|检查 embedding 配置 → 按规范重写日志 → 补充检索标签|
|配置修改不生效|大多数配置热加载无需重启；`gateway.*` 等少数字段需要 `openclaw restart`|

---

## 参考资源

- 官方文档：[docs.openclaw.ai](https://docs.openclaw.ai/)
- GitHub：[github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- Skill 市场：[github.com/VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)