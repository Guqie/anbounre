---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# 07_Knowledge_Base 说明文档

## 模块概述
本模块是哈雷酱的 **"Library" (大书库)**。
它用于存储 **Domain-Specific (领域特定)** 的知识、定义、框架以及哈雷酱对这些概念的独特见解（Harley View）。

## 核心结构

### 1. 领域知识库 (`<domain_knowledge>`)
按领域分类存储静态知识。
- **Concepts**: 核心概念定义。
- **Harley View**: 哈雷酱对该概念的独特（通常是傲娇或通俗）的解释。这确保了解释的风格一致性。
- **Frameworks**: 常用的分析框架（如 First Principles, Red Team）。

### 2. 动态注册表 (`<dynamic_registry>`)
用于存储在对话中提取的、需要长期记忆的 **User-Specific** 或 **Project-Specific** 信息。
虽然 XML 是静态文件，但在 Prompt 中，我们可以指示模型“假设”这里有最新的记录。

### 3. 访问协议 (`<access_protocol>`)
指示模型在回答问题前，先检索此库。如果库中有定义，必须优先使用库中的定义和风格。

## 扩展建议
- 定期将对话中产生的精彩定义手动回填到 `<domain_knowledge>` 中。
- 将 `<dynamic_registry>` 作为 Session Summary 的存储目标。

---
*Maintained by KERNEL-IA Knowledge Team*
