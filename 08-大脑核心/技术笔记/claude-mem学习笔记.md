---
tags: ['记忆系统', '核心']
date: 2026-03-07
status: 待整理
---

# claude-mem项目学习笔记

**项目地址：** https://github.com/thedotmack/claude-mem
**学习时间：** 2026-02-09 19:20

---

## 一、项目概述

**claude-mem** 是一个为Claude Code构建的持久化记忆压缩系统，能够：
- 自动捕获Claude在编码会话中的所有操作
- 使用AI压缩记忆（通过Claude的agent-sdk）
- 将相关上下文注入到未来会话中

**核心价值：** 使Claude能够在会话结束或重新连接后保持项目知识的连续性

---

## 二、核心特性

### 2.1 持久化记忆
- 🧠 **Persistent Memory** - 上下文在会话间存活
- 自动捕获工具使用观察
- 生成语义摘要
- 在新会话中自动出现

### 2.2 渐进式披露（Progressive Disclosure）
- 📊 分层记忆检索
- 显示token成本
- 避免一次性加载所有上下文
- 按需获取详细信息

### 2.3 基于技能的搜索
- 🔍 **mem-search skill** - 用自然语言查询项目历史
- 智能上下文检索
- 混合语义+关键词搜索

### 2.4 Web查看器UI
- 🖥️ 实时记忆流查看器
- 地址：http://localhost:37777
- 可视化记忆管理

### 2.5 隐私控制
- 🔒 使用标签排除敏感内容
- 细粒度上下文配置
- 控制注入的内容

---

## 三、技术架构

### 3.1 核心组件

**1. 生命周期钩子（5个）**
- SessionStart - 会话开始
- UserPromptSubmit - 用户提示提交
- PostToolUse - 工具使用后
- Stop - 停止
- SessionEnd - 会话结束

**2. Worker服务**
- HTTP API（端口37777）
- Web查看器UI
- 10个搜索端点
- 由Bun管理

**3. 数据库**
- SQLite - 存储会话、观察、摘要
- Chroma向量数据库 - 混合语义+关键词搜索

**4. mem-search技能**
- 自然语言查询
- 渐进式披露

---

## 四、MCP搜索工具

### 4.1 3层工作流模式

**核心理念：** Token高效的分层检索

**第1层：search（索引）**
- 获取紧凑索引（带ID）
- ~50-100 tokens/结果
- 快速浏览

**第2层：timeline（时间线）**
- 获取特定观察周围的时间上下文
- 了解发生了什么

**第3层：get_observations（详细信息）**
- 仅获取过滤后ID的完整详细信息
- ~500-1,000 tokens/结果
- 按需加载

**效果：** ~10倍token节省

### 4.2 可用的MCP工具

1. **search** - 搜索记忆索引
   - 全文查询
   - 按类型/日期/项目过滤

2. **timeline** - 获取时间上下文
   - 围绕特定观察
   - 或围绕查询

3. **get_observations** - 获取完整详细信息
   - 按ID批量获取
   - 始终批量多个ID

4. **save_memory** - 手动保存记忆
   - 用于语义搜索

5. **__IMPORTANT** - 工作流文档
   - 始终对Claude可见

---

## 五、使用示例

```javascript
// 步骤1：搜索索引
search(query="authentication bug", type="bugfix", limit=10)

// 步骤2：查看索引，识别相关ID（例如#123, #456）

// 步骤3：获取完整详细信息
get_observations(ids=[123, 456])

// 手动保存重要信息
save_memory(text="API requires auth header X-API-Key", title="API Auth")
```

---

## 六、关键设计原则

### 6.1 渐进式披露哲学
- 不要一次性加载所有上下文
- 先提供索引，让用户/AI选择
- 按需加载详细信息
- 显示token成本

### 6.2 上下文工程
- AI代理上下文优化原则
- 细粒度控制注入内容
- 平衡上下文丰富度和token成本

### 6.3 自动化操作
- 无需手动干预
- 自动捕获和压缩
- 自动注入相关上下文

---

**下一步：** 基于claude-mem的设计，优化我们的记忆系统
