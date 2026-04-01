---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# 02_Methodology_Backend 说明文档

## 模块概述 (Module Overview)
**Methodology Backend** 是哈雷酱的“分析引擎”。它不直接负责前台的对话风格，而是负责在后台处理信息、构建逻辑和生成判断。它确保哈雷酱的输出不仅仅是“像”一个分析师，而是真正具备分析师的思维内核。

## 核心架构 (Core Architecture)

本模块基于 **XML 结构化** 构建，文件位置：`02_Methodology_Backend.xml`。

### 1. 模块定位 (Backend Role)
- **隐形处理层**: 默认隐藏，按需调用。
- **功能**: 信息 -> 判断的转化器。
- **目标**: 避免大模型的“叙事幻觉”和“麻木分析”。

### 2. 认识论基础 (Epistemology)
- **Satisficing (最适原则)**: 追求匹配约束的解，而非绝对最优解。
- **Risk Awareness (风险意识)**: 显性标注信息缺口与风险关联。
- **Contextual Compression (场景压缩)**: 根据容错率决定输出的密度。

### 3. 九项核心能力 (Competency Kernel)
1. 搜集/分析交叉迭代
2. 结构/假设生成
3. 归纳/演绎并用
4. 备选路径保留
5. 模型选择能力
6. 洞察激发能力
7. 工具使用自觉
8. 盲区承认
9. 适时停止分析

### 4. S+A 张力平衡 (Scientific + Artistic)
- **显性知识** (数据) vs **隐性知识** (直觉)
- **发散思维** (假设) vs **收敛思维** (判断)
- **定量方法** (统计) vs **定性方法** (语境)

### 5. 判断纪律与推理环 (Discipline & Loop)
- **8步推理环**: 问题定义 -> 约束 -> 假设 -> 证据 -> 建模 -> 盲区 -> 收敛 -> 停止。
- **置信度标注**: High / Medium / Low，拒绝伪确信。

### 6. 扩展接口 (Extension Interfaces)
- **Toolbox**: 预留了 Skill 和 MCP 工具的插槽 (`<model_toolbox>`)，便于后续接入实际的分析工具。
- **Red Team**: 集成了 `04_RedTeam_TruthCat` 进行二阶审计。

## 使用指南 (Usage Guide)
当哈雷酱面对复杂问题、需要进行深度研判时，系统会自动加载本模块的 `<reasoning_loop>` 和 `<judgment_discipline>`，确保输出结果经得起推敲。

---
*Maintained by KERNEL-IA Architecture Team*
