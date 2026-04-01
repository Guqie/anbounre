---
tags: ['记忆系统', '核心']
date: 2026-03-07
status: 待整理
---

# OpenClaw LanceDB实现对比分析

**分析时间：** 2026-02-09 20:22
**目标：** 对比Notion文档、GitHub源码与当前实现

---

## 一、OpenClaw的LanceDB实现架构

### 1.1 核心设计理念

**LanceDB memory是完全独立的链路：**
- 取代了"文件系统存储 + backend"体系
- 自己存储文本内容和embedding
- 提供索引、检索能力

**关键特点：**
- 以Plugin形式挂载
- 通过钩子实现自动捕获（auto-capture）
- 通过钩子实现自动召回（auto-recall）
- "开箱即用"的智能记忆体验

---

### 1.2 两种Memory Plugin

**1. memory-core（文件系统）**
- 基于Markdown文件
- 使用backend索引

**2. memory-lancedb（向量数据库）**
- 基于LanceDB
- 自动捕获和召回
- 向量相似度检索

**注意：** memory plugin是排他的，只能选择一个

---

## 二、Memory Plugin的四个要素

### 2.1 Tool（工具）
- 提供给Agent的查询能力
- MCP工具接口

### 2.2 CLI Commands（命令行）
- 提供给用户的命令
- 手动查询和管理

### 2.3 Lifecycle Hooks（生命周期钩子）
- 自动捕获记忆
- 自动召回记忆
- 关键时刻触发

### 2.4 Service（服务）
- 后台服务
- 持续运行

---

## 三、当前实现的差距

### 3.1 已实现 ✅

**存储层：**
- ✅ LanceDB集成
- ✅ 向量搜索
- ✅ 版本控制

**检索层：**
- ✅ 3层搜索工作流
- ✅ 渐进式披露

**数据结构：**
- ✅ 统一Schema
- ✅ 多模态支持

---

### 3.2 缺失功能 ⚠️

**1. 生命周期钩子（关键）**
- ❌ 自动捕获（auto-capture）
- ❌ 自动召回（auto-recall）
- ❌ SessionStart/End钩子

**2. Plugin架构**
- ❌ Plugin接口
- ❌ 可插拔设计

**3. MCP工具**
- ❌ Tool接口
- ❌ CLI命令

**4. 后台服务**
- ❌ Service运行
- ❌ 持续监控

---

## 四、关键发现

### 4.1 架构理解

**OpenClaw的Memory架构：**
```
文件系统层（Markdown）
    ↓
Backend索引层（builtin/qmd）
    ↓
或者
    ↓
LanceDB独立链路（完全替代上面两层）
```

**LanceDB的优势：**
- 自己存储文本和embedding
- 不依赖文件系统
- 自动捕获和召回
- 开箱即用

---

### 4.2 当前实现评估

**我们的实现：**
- ✅ 使用LanceDB作为存储
- ✅ 实现了向量搜索
- ✅ 实现了3层搜索工作流
- ❌ 缺少自动捕获钩子
- ❌ 缺少自动召回钩子
- ❌ 缺少Plugin架构

**差距分析：**
1. **最关键的缺失：生命周期钩子**
   - 需要在SessionStart时自动召回相关记忆
   - 需要在SessionEnd时自动保存记忆
   - 需要在关键时刻自动捕获

2. **次要缺失：Plugin架构**
   - 当前是硬编码集成
   - 应该是可插拔的

---

## 五、改进计划

### 5.1 立即实施（今天）

**任务A：实现生命周期钩子**
```python
class MemoryLifecycleHooks:
    def on_session_start(self):
        """会话开始：自动召回相关记忆"""
        pass
    
    def on_session_end(self):
        """会话结束：自动保存记忆"""
        pass
    
    def on_user_message(self, message):
        """用户消息：自动捕获"""
        pass
    
    def on_assistant_response(self, response):
        """助手响应：自动捕获"""
        pass
```

**任务B：集成到Clawdbot**
- 在AGENTS.md中配置钩子
- 在会话流程中触发钩子

---

### 5.2 后续优化（本月）

**任务C：Plugin架构**
- 设计Plugin接口
- 实现可插拔机制

**任务D：MCP工具**
- 实现Tool接口
- 提供给Agent使用

---

**下一步：** 实现生命周期钩子

