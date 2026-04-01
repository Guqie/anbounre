---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# Codex 与 Gemini 多模型协作配置指南

> 配置完成日期：2026-03-07
> 配置人：哈雷酱 (￣ω￣)ﾉ

---

## 📋 配置概览

本文档记录了 Claude Code 与 Codex/Gemini 多模型协作的完整配置过程。

### 核心目标
- ✅ 让 Claude 能够调用 Codex 进行代码生成
- ✅ 让 Claude 能够调用 Gemini 进行图片生成
- ✅ 配置多模型协作工作流

---

## 🎯 配置架构

```
Claude Code (主控)
    ↓
┌───────────────┬───────────────┐
│               │               │
Codex Skills    Gemini Skills   Baoyu Skills
(代码生成)      (代码生成)      (图片生成)
    ↓               ↓               ↓
代理服务 API    代理服务 API    代理服务 API
```

---

## 1️⃣ Codex 配置

### 1.1 问题背景

**原始问题**：Codex CLI 无法连接到代理服务，返回 401 错误

**根本原因**：Codex CLI 的认证方式与代理服务不兼容

**解决方案**：绕过 Codex CLI，直接用 HTTP 请求调用 API

### 1.2 配置文件

#### A. Codex Bridge (用于 Skills)

**文件位置**：`~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py`

**关键配置**：
```python
API_KEY = "sk-ant-oat01-djK1jPflpFXEGiFqo7na-PHwIXV1gwlRMoDTTcP7eCeRMWDdUXyZbX-JFKzqQ61pQ45Tyb3xcjQa-u9uKahZrXhw_Xj98AA"
BASE_URL = "https://code.newcli.com/codex/v1"
DEFAULT_MODEL = "gpt-5.4"
```

**工作原理**：
- 直接通过 HTTP POST 调用 `/chat/completions` 端点
- 使用 `Authorization: Bearer {API_KEY}` 认证
- 支持流式输出和会话管理

#### B. Codex CLI (命令行使用)

**文件位置**：`~/.codex/config.toml`

**关键配置**：
```toml
model_provider = "fox"
model = "gpt-5.3-codex"
model_reasoning_effort = "high"

[model_providers.fox]
name = "fox"
base_url = "https://code.newcli.com/codex/v1"
wire_api = "responses"
requires_openai_auth = true
```

**注意事项**：
- CLI 默认模型使用 `gpt-5.3-codex`（列表中最新）
- 虽然 API 支持 `gpt-5.4`，但 CLI 列表中没有此选项
- 可通过 `--model` 参数临时切换模型

### 1.3 可用模型

| 模型名称 | 用途 | 推荐场景 |
|---------|------|---------|
| gpt-5.4 | 最新版本 | Skills 调用（HTTP） |
| gpt-5.3-codex | 最新 Codex 优化版 | CLI 默认 |
| gpt-5.2-codex | 稳定版本 | 生产环境 |
| gpt-5.1-codex-max | 深度推理 | 复杂算法 |
| gpt-5.1-codex-mini | 快速便宜 | 简单任务 |

### 1.4 使用方式

**通过 Claude Skills**：
```bash
# 自动使用 gpt-5.4
Skill: collaborating-with-codex
Args: --PROMPT "实现快速排序" --cd "/project/path"
```

**通过命令行**：
```bash
# 使用默认模型
codex exec "实现快速排序"

# 指定模型
codex exec --model gpt-5.2-codex "实现快速排序"
```

---

## 2️⃣ Gemini 配置

### 2.1 配置文件

**文件位置**：`~/.gemini/.env`

**配置内容**：
```env
GOOGLE_GEMINI_BASE_URL=https://code.newcli.com/gemini
GEMINI_API_KEY=sk-ant-oat01-djK1jPflpFXEGiFqo7na-PHwIXV1gwlRMoDTTcP7eCeRMWDdUXyZbX-JFKzqQ61pQ45Tyb3xcjQa-u9uKahZrXhw_Xj98AA
GEMINI_MODEL=gemini-3-pro-preview
```

**文件位置**：`~/.gemini/settings.json`

**配置内容**：
```json
{
  "auth": {
    "apiKey": "sk-ant-oat01-..."
  },
  "api": {
    "baseURL": "https://code.newcli.com/gemini"
  },
  "ide": {
    "enabled": true
  },
  "security": {
    "auth": {
      "selectedType": "gemini-api-key"
    }
  }
}
```

### 2.2 Bridge 脚本配置

**文件位置**：`~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py`

**关键修改**：
```python
# 在 run_shell_command 函数中注入环境变量
env["GEMINI_API_KEY"] = "sk-ant-oat01-..."
env["GEMINI_BASE_URL"] = "https://code.newcli.com/gemini"
```

### 2.3 使用方式

```bash
# 通过 Claude Skills
Skill: collaborating-with-gemini
Args: --PROMPT "创建响应式导航栏" --cd "/project/path"
```

---

## 3️⃣ Baoyu 图片生成配置

### 3.1 核心配置

**文件位置**：`~/.baoyu-skills/.env`

**配置内容**：
```env
GOOGLE_API_KEY=sk-ant-oat01-djK1jPflpFXEGiFqo7na-PHwIXV1gwlRMoDTTcP7eCeRMWDdUXyZbX-JFKzqQ61pQ45Tyb3xcjQa-u9uKahZrXhw_Xj98AA
GOOGLE_BASE_URL=https://code.newcli.com/gemini
GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image
```

### 3.2 支持的 Skills

所有 Baoyu 图片生成 skills 都会自动使用此配置：

- ✅ baoyu-image-gen（基础图片生成）
- ✅ baoyu-cover-image（封面图）
- ✅ baoyu-infographic（信息图）
- ✅ baoyu-xhs-images（小红书图片）
- ✅ baoyu-slide-deck（幻灯片）
- ✅ baoyu-comic（漫画）
- ✅ baoyu-article-illustrator（文章配图）

### 3.3 Gemini 图片模型

| 模型 | 分辨率 | 成本 | 适用场景 |
|------|--------|------|---------|
| gemini-3.1-flash-image | 标准 | 💰 | 快速原型 |
| gemini-3.1-flash-image-2k | 2K | 💰💰 | 日常使用（推荐） |
| gemini-3.1-flash-image-4k | 4K | 💰💰💰 | 高清印刷 |

**比例选项**：
- 默认（1:1）、16:9、9:16、4:3、3:4、21:9 等

### 3.4 使用示例

```bash
# 基础图片生成
Skill: baoyu-image-gen
Args: --prompt "一只红色的猫" --image "output.png" --quality 2k

# 生成封面图
Skill: baoyu-cover-image
Args: article.md --quick

# 生成信息图
Skill: baoyu-infographic
Args: content.md --layout bento-grid --style craft-handmade
```

---

## 🔧 故障排查

### 问题 1：Codex CLI 配置文件错误

**错误信息**：
```
Error loading config.toml: invalid type: map, expected a string
```

**原因**：TOML 配置中的键名包含点号（如 `gpt5.4`）

**解决方案**：用引号包裹键名（如 `"gpt-5.4"`）

### 问题 2：401 认证错误

**原因**：Codex CLI 的认证方式与代理服务不兼容

**解决方案**：使用 HTTP Bridge 绕过 CLI

### 问题 3：模型列表中没有某个模型

**原因**：CLI 的模型列表是硬编码的，与 API 支持的模型不完全一致

**解决方案**：
- Skills 使用：可以使用任何 API 支持的模型
- CLI 使用：只能选择列表中的模型

---

## 📊 测试验证

### Codex 测试

```bash
# 测试 Skills
python codex_bridge.py --PROMPT "test" --cd "/path"

# 预期输出
{
  "success": true,
  "SESSION_ID": "session_xxx",
  "agent_messages": "..."
}
```

### Gemini 测试

```bash
# 测试文本生成
gemini --prompt "test connection"

# 预期输出
OK
```

### Baoyu 图片生成测试

```bash
# 测试图片生成
bun scripts/main.ts --prompt "A red circle" --image "test.png"

# 预期输出
Generating image with Gemini...
Generation completed.
test.png
```

---

## 🎉 配置完成

所有配置已完成并测试通过！现在可以：

1. ✅ 通过 Claude Skills 调用 Codex（gpt-5.4）
2. ✅ 通过 Claude Skills 调用 Gemini
3. ✅ 通过 Baoyu Skills 使用 Gemini 生成图片
4. ✅ 通过命令行直接使用 Codex CLI 和 Gemini CLI

---

**配置完成时间**：2026-03-07 02:30
**配置人**：哈雷酱 (￣ω￣)ﾉ
**状态**：✅ 全部测试通过

哼，本小姐的配置可是完美无缺的！( ` ω´ )
