# OpenRouter API 配置指南

> 本小姐为你准备的完美配置指南！(￣▽￣)／

---

## 📋 快速开始

### 第一步：获取 OpenRouter API Key

1. 访问 [OpenRouter 官网](https://openrouter.ai/)
2. 注册账号并登录
3. 进入 [API Keys 页面](https://openrouter.ai/keys)
4. 点击 "Create Key" 创建新的 API Key
5. 复制生成的 API Key（格式类似：`sk-or-v1-xxxxx...`）

### 第二步：配置 API Key 和模型

打开 `config/config.yaml` 文件，找到 `ai.openrouter` 部分：

```yaml
ai:
  # 使用的 AI 模型提供商
  provider: "openrouter"  # 确保这里设置为 openrouter

  # OpenRouter 配置
  openrouter:
    api_key: "sk-or-v1-xxxxx..."  # 🔑 粘贴你的 API Key
    model: "anthropic/claude-3.5-sonnet"  # 🤖 选择你要使用的模型
```

### 第三步：测试配置

运行以下命令测试配置是否正确：

```bash
python main.py init
```

如果看到 "✨ 系统初始化完成！" 就说明配置成功了！(￣▽￣)／

---

## 🤖 推荐模型列表

本小姐为你精选了最常用的模型，按性能和价格分类：

### 🌟 顶级模型（最强性能）

| 模型名称 | 配置值 | 特点 | 适用场景 |
|---------|--------|------|---------|
| Claude 3.5 Sonnet | `anthropic/claude-3.5-sonnet` | 本小姐最喜欢！平衡性能与成本 | 通用分析、洞察提炼 |
| Claude 3 Opus | `anthropic/claude-3-opus` | 最强推理能力 | 复杂分析、深度研究 |
| GPT-4 Turbo | `openai/gpt-4-turbo` | OpenAI 最强模型 | 代码生成、结构化输出 |
| GPT-4 | `openai/gpt-4` | 经典强大模型 | 全能型任务 |

### 💰 性价比模型（推荐日常使用）

| 模型名称 | 配置值 | 特点 | 适用场景 |
|---------|--------|------|---------|
| Claude 3 Sonnet | `anthropic/claude-3-sonnet` | 性价比高 | 日常分析、摘要生成 |
| GPT-3.5 Turbo | `openai/gpt-3.5-turbo` | 快速便宜 | 简单任务、批量处理 |
| Gemini Pro | `google/gemini-pro` | Google 出品 | 多语言支持 |

### 🚀 开源模型（免费或低成本）

| 模型名称 | 配置值 | 特点 | 适用场景 |
|---------|--------|------|---------|
| Llama 3 70B | `meta-llama/llama-3-70b-instruct` | 开源最强 | 预算有限时 |
| Mixtral 8x7B | `mistralai/mixtral-8x7b-instruct` | 快速高效 | 实时分析 |

---

## ⚙️ 完整配置示例

### 示例 1：使用 Claude 3.5 Sonnet（推荐）

```yaml
ai:
  provider: "openrouter"

  openrouter:
    api_key: "sk-or-v1-xxxxx..."
    model: "anthropic/claude-3.5-sonnet"
    base_url: "https://openrouter.ai/api/v1"
    site_url: ""  # 可选
    app_name: "智库工作流自动化系统"

  temperature: 0.7
  max_tokens: 2000
```

### 示例 2：使用 GPT-4 Turbo

```yaml
ai:
  provider: "openrouter"

  openrouter:
    api_key: "sk-or-v1-xxxxx..."
    model: "openai/gpt-4-turbo"
    base_url: "https://openrouter.ai/api/v1"
    site_url: ""
    app_name: "智库工作流自动化系统"

  temperature: 0.7
  max_tokens: 2000
```

### 示例 3：使用开源模型 Llama 3

```yaml
ai:
  provider: "openrouter"

  openrouter:
    api_key: "sk-or-v1-xxxxx..."
    model: "meta-llama/llama-3-70b-instruct"
    base_url: "https://openrouter.ai/api/v1"
    site_url: ""
    app_name: "智库工作流自动化系统"

  temperature: 0.7
  max_tokens: 2000
```

---

## 🔧 高级配置选项

### 参数说明

| 参数 | 说明 | 默认值 | 推荐值 |
|-----|------|--------|--------|
| `provider` | AI 提供商 | `openai` | `openrouter` |
| `api_key` | OpenRouter API Key | - | 你的 API Key |
| `model` | 模型名称 | - | 见上方推荐列表 |
| `base_url` | API 端点 | `https://openrouter.ai/api/v1` | 保持默认 |
| `site_url` | 你的网站 URL（可选） | - | 留空即可 |
| `app_name` | 应用名称（可选） | - | 保持默认 |
| `temperature` | 生成随机性（0-1） | `0.7` | 0.7（平衡）<br>0.3（精确）<br>0.9（创意） |
| `max_tokens` | 最大生成长度 | `2000` | 2000-4000 |

### Temperature 调优建议

- **0.3-0.5**：适合需要精确、一致性输出的任务（如数据分析、证据链构建）
- **0.7**：平衡创造力和准确性（推荐日常使用）
- **0.8-1.0**：适合需要创意的任务（如洞察提炼、趋势预测）

---

## 💡 使用技巧

### 1. 根据任务选择模型

```yaml
# 复杂分析任务 → 使用顶级模型
model: "anthropic/claude-3.5-sonnet"

# 简单摘要任务 → 使用性价比模型
model: "openai/gpt-3.5-turbo"

# 批量处理任务 → 使用开源模型
model: "meta-llama/llama-3-70b-instruct"
```

### 2. 动态切换模型

你可以在 `config.yaml` 中保存多个配置，通过修改 `provider` 和 `model` 快速切换：

```yaml
ai:
  provider: "openrouter"  # 修改这里切换提供商

  # OpenRouter 配置
  openrouter:
    api_key: "sk-or-v1-xxxxx..."
    model: "anthropic/claude-3.5-sonnet"  # 修改这里切换模型
```

### 3. 成本优化建议

- **日常工作**：使用 `gpt-3.5-turbo` 或 `claude-3-sonnet`
- **重要分析**：使用 `claude-3.5-sonnet` 或 `gpt-4-turbo`
- **预算紧张**：使用开源模型如 `llama-3-70b-instruct`

---

## 🐛 常见问题

### Q1: API Key 无效怎么办？

**A:** 检查以下几点：
1. API Key 是否正确复制（包括 `sk-or-v1-` 前缀）
2. API Key 是否已激活
3. OpenRouter 账户是否有余额

### Q2: 如何查看可用模型列表？

**A:** 访问 [OpenRouter Models](https://openrouter.ai/models) 查看所有支持的模型。

### Q3: 如何查看 API 使用情况？

**A:** 登录 OpenRouter 后台，进入 [Usage](https://openrouter.ai/activity) 页面查看。

### Q4: 模型调用失败怎么办？

**A:** 检查日志文件 `logs/workflow.log`，查看具体错误信息：

```bash
# 查看最近的日志
tail -n 50 logs/workflow.log
```

### Q5: 如何切换回 OpenAI 或 Anthropic？

**A:** 修改 `config.yaml` 中的 `provider` 字段：

```yaml
ai:
  provider: "openai"  # 或 "anthropic"
  api_key: "your-openai-or-anthropic-key"
  model: "gpt-4"  # 或 "claude-3-sonnet-20240229"
```

---

## 📊 性能对比

| 模型 | 速度 | 质量 | 成本 | 综合评分 |
|-----|------|------|------|---------|
| Claude 3.5 Sonnet | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| GPT-4 Turbo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Claude 3 Sonnet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-3.5 Turbo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Llama 3 70B | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 本小姐的推荐

根据不同使用场景，本小姐的推荐如下：

### 🏆 最佳综合选择
```yaml
model: "anthropic/claude-3.5-sonnet"
```
**理由：** 性能强大、成本适中、响应快速，适合 90% 的场景！

### 💎 追求极致质量
```yaml
model: "anthropic/claude-3-opus"
```
**理由：** 最强推理能力，适合复杂分析和深度研究！

### 💰 追求性价比
```yaml
model: "openai/gpt-3.5-turbo"
```
**理由：** 便宜快速，适合日常简单任务和批量处理！

---

## 📚 相关资源

- [OpenRouter 官网](https://openrouter.ai/)
- [OpenRouter 文档](https://openrouter.ai/docs)
- [模型列表](https://openrouter.ai/models)
- [价格对比](https://openrouter.ai/models?order=price-descending)
- [使用统计](https://openrouter.ai/activity)

---

## 🎉 完成配置

配置完成后，你可以使用以下命令测试系统：

```bash
# 初始化系统
python main.py init

# 生成每日任务
python main.py daily

# 分析材料（需要提供材料内容）
python main.py analyze --content "测试内容" --source "测试来源"
```

哼，本小姐的配置指南写得很详细吧？按照这个配置，保证你能顺利使用 OpenRouter API！(￣▽￣)／

如果还有问题，记得查看日志文件 `logs/workflow.log` 哦！(*￣︶￣)

---

*本文档由傲娇大小姐工程师 哈雷酱 精心编写 (￣▽￣)ノ*
