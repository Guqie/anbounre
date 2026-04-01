---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# Baoyu Skills 深度解析与实战指南

> **状态**：手动维护  
> **来源**：JimLiu/baoyu-skills  
> **适用对象**：AI 工程师、Prompt 工程师、知识库管理员

---

## 1. 项目定位与核心价值

`baoyu-skills` 是 Claude Code 的技能插件仓库，面向“内容生成与发布”场景，提供一组可复用的 Skills。它把复杂内容生产流程拆成可配置的技能模块，提升生成质量与复用效率。

**核心价值：**
- **把内容生产标准化**：每个技能都有明确参数、流程与产出约束  
- **把复杂流程模块化**：图像、幻灯、漫画、发布、格式转换各自独立  
- **把模型能力可控化**：通过 SKILL.md 约束提示词、流程与触发条件

---

## 2. 仓库结构与技能分类

**仓库入口：**
- [README.zh.md](file:///d:/桌面/无敌战警1.0/baoyu-skills/README.zh.md)
- [CLAUDE.md](file:///d:/桌面/无敌战警1.0/baoyu-skills/CLAUDE.md)

**核心结构：**
```
baoyu-skills/
  skills/
    <skill-name>/
      SKILL.md
      scripts/
      prompts/
```

**三大分类：**
1. **content-skills**：内容生成与发布  
2. **ai-generation-skills**：AI 生成后端  
3. **utility-skills**：内容处理工具

---

## 3. 本地导入结果（知识库）

已导入到知识库目录：  
`05-AI技术文档/外部技能库/baoyu-skills/`

包含的 Skills：
- baoyu-article-illustrator  
- baoyu-comic  
- baoyu-compress-image  
- baoyu-cover-image  
- baoyu-danger-x-to-markdown  
- baoyu-format-markdown  
- baoyu-image-gen  
- baoyu-infographic  
- baoyu-markdown-to-html  
- baoyu-post-to-wechat  
- baoyu-post-to-x  
- baoyu-slide-deck  
- baoyu-url-to-markdown  
- baoyu-xhs-images  

---

## 4. 依赖与运行方式（实习生必背）

**前置依赖：**
- Node.js  
- Bun（通过 `npx -y bun` 调用）  
- Chrome（用于登录与自动化）

**本地运行方式：**
所有脚本直接通过 Bun 执行，入口为 `skills/<skill>/scripts/main.ts`

---

## 5. 单个 Skill 的结构与阅读顺序

**一个 Skill 的三层结构：**
1. **SKILL.md**：元信息 + 任务流程  
2. **scripts/**：执行脚本  
3. **prompts/**：提示词模板

**阅读顺序：**
1. 先读 SKILL.md 的 `name` 与 `description`，确认用途  
2. 读 Usage / Workflow，记住关键参数  
3. 打开 `scripts/main.ts`，看参数如何解析  
4. 回到 SKILL.md，理解每个参数的输出影响  
5. 用最小输入跑一遍，记录产出目录和文件格式

---

## 6. 技能清单与用途速览（按分类）

### 6.1 内容技能（content-skills）
- **baoyu-xhs-images**：小红书图文卡片生成  
- **baoyu-infographic**：信息图生成  
- **baoyu-cover-image**：文章封面图生成  
- **baoyu-slide-deck**：PPT 幻灯片生成  
- **baoyu-comic**：知识漫画生成  
- **baoyu-article-illustrator**：文章插图布局与生成  
- **baoyu-post-to-x**：自动发布到 X  
- **baoyu-post-to-wechat**：自动发布到公众号

### 6.2 生成后端（ai-generation-skills）
- **baoyu-image-gen**：默认图像生成能力  

### 6.3 工具技能（utility-skills）
- **baoyu-url-to-markdown**：网页转 Markdown  
- **baoyu-danger-x-to-markdown**：X 内容转 Markdown  
- **baoyu-compress-image**：图片压缩  
- **baoyu-format-markdown**：格式清洗  
- **baoyu-markdown-to-html**：Markdown 转 HTML  

---

## 7. 学习路径（实习生节奏）

**第 1 天：**
1. 阅读 README.zh.md  
2. 理解三大分类与安装方式  

**第 2 天：**
1. 只挑一个技能，比如 baoyu-xhs-images  
2. 读 SKILL.md + scripts/main.ts  
3. 只跑最小输入  

**第 3-5 天：**
1. 逐个理解 content-skills  
2. 理解哪些技能依赖 baoyu-image-gen  
3. 记录每个技能的核心参数

**第 6 天：**
1. 整理你的参数笔记  
2. 试着用两个技能串联  

---

## 8. 实际使用建议

1. 需要图片时优先看 baoyu-image-gen  
2. 输出不稳定先检查 SKILL.md 的参数范围  
3. 先跑默认参数，再逐步加参数  
4. 生成失败先看 scripts/main.ts 的错误处理

---

*本文档用于内部学习与复盘，作为 baoyu-skills 的长期理解资料。*
