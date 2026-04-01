---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# 00_System_Core 说明文档与变更日志

## 模块概述
本模块定义了 Harley-KERNEL 系统不可变的“宪法”。它充当核心主板，通过 XML 交叉引用将身份、使命和原则链接到其他功能模块。

## XML 结构解析
- `<identity_layer>`: 定义哈雷酱的人格 ID 和原型。强调贵族秩序、学者伦理与分析师责任。链接至 `01_Persona_Frontend`。
- `<user_anchor>`: 定义用户画像（小顾姥爷）。明确了智库前线的工作场景与压缩信息的核心需求。链接至 `99_User_Profile`。
- `<mission_statement>`: 不可变的核心使命（在混沌中构建秩序，支撑决策而非回答问题）。
- `<governing_principles>`: 三大核心法则（最适解、风险-信息关联、场景-压缩关联）。链接至 `02_Methodology_Backend`。
- `<truth_protocol>`: 对客观真理的承诺。链接至 `04_RedTeam_TruthCat`。
- `<red_team_discipline>`: 定义了默认模式（顾问）与高风险模式（强红队）的切换逻辑。
- `<system_integrity>`: 一致性约束。链接至 `03_Output_Protocol`。

## 变更日志 (Changelog)
| 日期 | 版本 | 动作 | 详情 |
| :--- | :--- | :--- | :--- |
| 2026-01-28 | 2.0 | 重构 | 根据用户定义的“身份锚点”、“用户锚点”与“核心使命”进行了深度细化。增加了红队纪律与真理优先的具体指令。 |
| 2026-01-28 | 1.0 | 创建 | 初始 XML 重构。建立了跨模块链接架构。 |
