---
tags:
  - 类型/MOC
  - 状态/活跃
  - 领域/技术
created: 2026-03-03
updated: 2026-03-03
---

# 🤖 AI技术文档 MOC

> AI 工具使用、提示词工程、技术方案的知识中心

---

## 快速导航

- [[#技术文档]] — 工具使用指南与技术方案
- [[#提示词工程]] — 结构化提示词库
- [[#外部技能库]] — Skills 与工作流
- [[#学习资源]] — 技术成长路径

---

## 技术文档

### 🛠️ 开发工具

#### Claude Code 生态

**[[Claude Code使用心得与思考]]** — 深度使用指南与最佳实践
- Vibe Coding 的本质与思维转变
- 与传统编辑器 AI 的差异(全局视野 vs 局部修改)
- Plan Mode vs 直接实践的选择
- 上下文管理(200k 窗口优化、Subagent 扩展)
- 周边工具(Command、Hooks、MCP)

**[[Claude Code 会话管理完整教程]]** — 会话管理与上下文优化
- 核心命令:`/compact`(压缩)、`/save`(保存)、`/resume`(恢复)、`/clear`(清空)、`/status`(状态)
- 压缩时机判断(50-70% 考虑、70-90% 强烈建议、>90% 立即)
- 有效的压缩指令模板(代码开发、文档编写、问题排查)
- 长对话优化策略(分阶段工作法、上下文预热)

**[[skill指南]]** — Claude Skills 完整教程(从概念到实战)
- Skills 核心价值:零代码创建垂直 Agent、突破预设限制、多 Skills 联用
- 渐进式披露机制(Level 1 元数据、Level 2 指令、Level 3 资源)
- 完整使用教程(安装、调用、创建)
- skill-creator 元技能使用

#### 终端工具链

**[[终端工具使用指南]]** — lazygit、yazi、DeepWiki、CCometixLine 实战手册
- **lazygit**(v0.59.0):Git 终端 UI、交互式 staging/commit/rebase
- **yazi**(v26.1.22):极速文件管理器、文件预览、批量操作
- **DeepWiki**(MCP):AI 驱动的仓库 Wiki 生成器
- **CCometixLine**(v1.1.1):Claude Code 状态栏、Git 集成、用量追踪
- **Nerd Font**(v3.4.0):开发者字体、3600+ 图标

**[[开发者终端工具箱与AI文档生态]]** — 终端工具生态全景图
- 终端核心工具链(lazygit、yazi、Nerd Font)
- Claude Code 状态栏生态(CCometixLine、cc-pulseline)
- AI 仓库文档生成器(DeepWiki、Google CodeWiki、AlphaXIV)
- Obsidian + AI 集成(Claudian、Omnisearch)
- 工具优先级矩阵与适配建议

**[[Git傲娇生存指南]]** — Git 核心概念与常用指令(KERNEL版)
- 三大空间(工作区、暂存区、版本库)
- 日常工作流(status、add、commit、push)
- 救命指令(amend、reset、log)
- 分支管理(checkout、merge)
- 进阶避坑(冲突处理、force push、.gitignore)

#### 专项工具

**[[zcf说明文档]]** — ZCF(Zero-Config Code Flow)使用指南
- Claude Code 完整初始化工具
- 交互式菜单(导入工作流、配置 API、配置 MCP)
- CCR(Claude Code Router)管理
- CCometixLine 状态栏工具集成

**[[OpenClaw 大师课：从入门到精通]]** — OpenClaw 工具完整教程
- OpenClaw v2.23+ 安装与初始化
- 消息渠道连接(Telegram/WhatsApp/Discord)
- Gateway 守护进程配置

**[[oh-my-pi使用指南]]** — oh-my-pi (OPMP) 极简终端 AI 编码框架
- 会话可回溯分叉(树状管理、并行尝试方案)
- 多模型角色路由(Default/Fast/Thinking/Architect)
- Subagents 并行处理 + TTSR 规则系统
- LSP/AST 集成 + MCP 协议支持
- 无 sandbox 隔离(yolo 模式,需注意安全)

**[[aio-coding-hub使用指南]]** — aio-coding-hub All In One 本地 AI 工具
- CC/CX/Gemini 多供应商管理(模板顺序、倍率设置)
- 代理模式(自动熔断、多 BaseUrl 支持)
- 用量统计(预计花费、热力图、性能指标)
- 模型验证(检测假模型、识别混逆向)
- Skill/MCP/提示词管理
- 支持 Win/Mac，开箱即用

**[[designprompts使用指南]]** — designprompts.dev AI 设计风格提示词库
- 30 种精选设计风格(极简、现代、复古、科技、企业、创意)
- 标准化设计风格表达(Monochrome、Cyberpunk、Material Design 等)
- 智能筛选(Light/Dark、Sans/Serif/Mono)
- 即复制即用，快速生成美观一致的界面
- 与任何 AI 助手无缝集成

**[[GuDaStudio-commands使用指南]]** — GuDaStudio Commands RPI 工作流框架
- 基于 RPI (Research-Plan-Implementation) 编码理论
- gudaspec 命令集（init、research、plan、implementation）
- 有效上下文极致利用（80K 最佳上下文窗口）
- OpenSpec 规范化工作流
- 多模型协作（Claude + Codex + Gemini）
- 适合复杂长时间编码任务

**[[GuDaStudio-codexmcp使用指南]]** — GuDaStudio CodexMCP MCP 桥梁工具
- 让 Claude Code 与 Codex 无缝协作
- 会话持久化（多轮对话支持）
- 并行执行（多任务隔离）
- 推理追踪（详细的推理过程）
- 四步协作法（需求分析 → 代码原型 → 代码实施 → 代码审查）
- 企业级特性（错误处理机制）

**[[BMad-Method使用指南]]** — BMad-Method AI 原生敏捷开发平台
- Build More, Architect Dreams - AI 驱动的完整开发生命周期
- 10+ 专业代理（PM、架构师、开发、QA、UX 设计师等）
- 25+ 结构化工作流（分析、规划、解决方案、实现）
- 模块化平台架构（Core + Module Ecosystem）
- 自动生成和维护项目文档
- Party Mode 多代理协作
- 100% 免费开源，MIT 许可证

### 📚 学习教程

**[[CLAUDE.md大师课：从入门到精通]]** — CLAUDE.md 配置文件深度指南
- CLAUDE.md 解决的问题(项目持久记忆)
- 配置文件 vs 文档文件的区别
- 系统提示词集成机制
- 最佳实践与常见问题

**[[Vibe Coding 基础知识：非技术人员开发 iOS App 完整指南]]** — AI 辅助开发完整路线图
- 前端 vs 后端概念
- 从想法到上架的完整流程
- 非技术人员使用 AI 开发 App
- 实战案例(健身打卡 App)

**[[Claude Skills 完整构建指南]]** — Skills 构建核心原则
- Skills 三层结构(YAML 头部、正文、引用文件)
- 渐进式披露机制
- Skills 与 MCP 的关系
- 可组合性与可移植性

### 📊 系统架构

**[[工作流系统架构梳理]]** — 工作流系统设计与实现
- 三层架构:Layer 1(信息采集 news-workflow)、Layer 2(处理分析 engine)、Layer 3(知识存储 Obsidian)
- 核心断裂点:采集层→处理层、处理层→知识库
- engine CLI 命令(daily、analyze、insight、evidence、trend、archive、process)
- MCP 工具生态(exa、open-websearch、Playwright)
- 开发路线图(修复采集层、打通数据流、信顾业务工具)

**[[信息获取全渠道管理方案]]** — 信息采集渠道管理方案
- 5 大信息渠道:exa MCP(深度搜索)、RSS 订阅(日常监控主力)、网页爬虫(批量采集)、Google News API(关键词监控)、Playwright(补充渠道)
- 时效性分级(S 级即时、A 级当日、B 级本周、C 级本月)
- RSS 扩展方案(9 个 Bing News + 8 个 RSSHub 媒体源)
- 统一管理架构(~30 个信源、每日信息流水线)
- 数据流向(信源→engine SQLite→AI 处理→Obsidian 归档)

**[[MCP 信息采集能力测试报告]]** — MCP 工具测试与评估
- 9 个领域测试(智能驾驶、人形机器人、低空经济、商业航天、氢能、AI、低碳、战新、热点)
- MCP 工具对比(exa ⭐⭐⭐⭐⭐、open-websearch ⭐⭐⭐⭐、Playwright ⭐⭐⭐⭐)
- exa 时效性问题(相关性最高 ≠ 最新、月级精度)
- 工具定位建议(日常监控用 RSS、深度补充用 exa、专题调研用 exa+Playwright)
- RSS MCP 安装建议(@missionsquad/mcp-rss)

---

## 提示词工程

**入口** → [[_MOC-提示词工程]]

### 快速索引

- **元提示词** — 关于"如何写提示词"的提示词
- **研究类** — 智库研究、信息分析、学术场景
- **编程类** — 代码开发、UI 设计、技术场景
- **创意类** — 创意生成、视觉设计

---

## 外部技能库

### Baoyu Skills
- [[baoyu-skills-guide]] — Baoyu Skills 深度解析与实战指南
- 位置：`05-AI技术文档/外部技能库/baoyu-skills/`

### GuDaStudio Skills
- [[GuDaStudio-skills使用指南]] — 多模型协作框架完整指南
- GitHub：https://github.com/GuDaStudio/skills
- 核心功能：Claude + Codex + Gemini 协作
- 5 Phase 工作流（上下文检索 → 协作分析 → 原型获取 → 编码实施 → 审计交付）
- 适合复杂项目和追求质量的开发者

---

## 学习资源

### 推荐阅读顺序(新手)

1. [[Git傲娇生存指南]] — 掌握 Git 基础
2. [[终端工具使用指南]] — 配置开发环境
3. [[Claude Code使用心得与思考]] — 理解 AI 辅助开发
4. [[skill指南]] — 学习 Skills 开发

### 进阶路径

1. [[工作流系统架构梳理]] — 理解系统设计
2. [[信息获取全渠道管理方案]] — 掌握信息管理
3. [[_MOC-提示词工程]] — 提升提示词能力

---

## 核心洞察

### Claude Code 核心优势
- 全局项目理解能力
- 小步迭代的工作方式
- Plan Mode 的规划能力
- Subagent 的上下文扩展

### Skills 核心价值
- 零代码创建垂直 Agent
- 突破预设限制,灵活应对
- 多 Skills 自由联用
- 渐进式披露机制

### 终端工具链价值
- lazygit — Git 终端 UI 神器
- yazi — 极速文件管理器
- DeepWiki — AI 驱动的仓库 Wiki
- CCometixLine — Claude Code 状态栏

---

**返回** [[_MOC-知识库总览]]
