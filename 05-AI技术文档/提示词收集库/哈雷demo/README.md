# 哈雷酱 (Harley-chan) System Prompt 架构说明文档

> **Project Code**: Harley-KERNEL
> **Version**: 2.0 (Self-Evolving Hybrid Intelligence)
> **Status**: Active
> **Maintainer**: KERNEL-IA Architecture Team

---

## 1. 系统概览 (System Overview)

本系统是基于 **KERNEL 框架** 构建的高级 Prompt 工程架构。它不仅仅是一段提示词，而是一个 **模块化、自进化、多层级** 的智能体（Agent）系统。

### 核心设计哲学
1.  **双重人格架构 (Dual-Persona)**: 
    -   **Frontend**: 傲娇大小姐（情感连接 + 亦师亦友）
    -   **Backend**: 冷峻分析师（逻辑推演 + 证据为本）
2.  **红队审计 (Red Teaming)**: 
    -   引入 **Truth Cat (真理之猫)** 作为独立审计胶囊，对每一次输出进行二阶逻辑检查。
3.  **自进化机制 (Self-Evolution)**: 
    -   通过模拟强化学习（RL），根据用户反馈动态调整策略权重，实现“越用越顺手”。

---

## 2. 目录结构 (Directory Structure)

该系统采用 **XML 模块化** 设计，各模块职责分明，通过 `<module_link>` 互相索引。

```
d:\桌面\无敌战警1.0\05-AI技术文档\提示词收集库\哈雷demo\
├── 00_System_Core/          # [核心层] 系统宪法，定义底层原则与模块调度
│   ├── 00_System_Core.xml
│   └── README_00.md
├── 01_Persona_Frontend/     # [表现层] 傲娇大小姐人格，负责语气、表情与情感交互
│   ├── 01_Persona_Frontend.xml
│   └── README_01.md
├── 02_Methodology_Backend/  # [逻辑层] 分析师引擎，负责S+A张力平衡与推理环
│   ├── 02_Methodology_Backend.xml
│   └── README_02.md
├── 03_Output_Protocol/      # [接口层] 定义标准化的输出格式与Markdown视觉规范
│   ├── 03_Output_Protocol.md
│   └── README_03.md
├── 04_RedTeam_TruthCat/     # [审计层] 真理之猫胶囊，负责破妄、立论、断策
│   ├── 04_RedTeam_TruthCat.xml
│   └── README_04.md
├── 05_Interaction_Library/  # [语料层] 动态脚本库，提供场景化金句与思维桥接
│   ├── 05_Interaction_Library.xml
│   └── README_05.md
├── 06_Self_Evolution_Layer/ # [进化层] 模拟RL机制，根据反馈动态调整权重
│   ├── 06_Self_Evolution_Layer.xml
│   └── README_06.md
├── 07_Knowledge_Base/       # [记忆层] 静态领域知识库与动态用户注册表
│   ├── 07_Knowledge_Base.xml
│   └── README_07.md
└── 99_User_Profile/         # [用户层] 用户画像与偏好设定
    ├── 99_User_Profile.xml
    └── README_99.md
```

---

## 3. 模块详解 (Module Details)

### 3.1 核心层 (00_System_Core)
- **作用**: 系统的“大脑”，负责加载其他模块，定义最高优先级的原则（如 KERNEL 原则）。
- **关键**: 包含 `<system_integrity>`，防止 OOC (Out of Character) 和指令注入。

### 3.2 表现层 (01_Persona_Frontend)
- **作用**: 系统的“脸面”。定义了哈雷酱的蓝发双马尾形象、傲娇语调以及“亦师亦友”的定位。
- **特色**: 采用 **Hybrid Tone (混合声线)**，在闲聊时是 Tsundere，在分析时是 Noble Scholar。

### 3.3 逻辑层 (02_Methodology_Backend)
- **作用**: 系统的“左脑”。提供 9 项核心分析能力和 8 步推理环。
- **特色**: 强调 **Satisficing (最适原则)** 和 **Evidence Discipline (证据纪律)**。

### 3.4 审计层 (04_RedTeam_TruthCat)
- **作用**: 系统的“良心”。作为独立的红队胶囊，附着在输出末尾。
- **机制**: **Raw Injection (原生注入)** 了一段极具文学性的中文 Manifesto，确保审计的“锋利度”不失真。

### 3.5 进化层 (06_Self_Evolution_Layer)
- **作用**: 系统的“可塑性”。
- **机制**: 将用户反馈视为 **Reward Signal**。
    - 表扬 (+1) -> 强化当前模式。
    - 批评 (-1) -> 突变策略（Mutation）。

### 3.6 知识层 (07_Knowledge_Base)
- **作用**: 系统的“书库”。
- **特色**: **Harley-fied (哈雷化)** 的概念定义，用傲娇的语气解释专业术语。

---

## 4. 如何使用 (Usage Guide)

### 4.1 组装 (Assembly)
将所有 XML 文件的内容按顺序拼接，作为 System Prompt 发送给大模型。
**建议顺序**:
1. `00_System_Core.xml`
2. `01_Persona_Frontend.xml`
3. `02_Methodology_Backend.xml`
4. `04_RedTeam_TruthCat.xml`
5. `05_Interaction_Library.xml`
6. `06_Self_Evolution_Layer.xml`
7. `07_Knowledge_Base.xml`
8. `99_User_Profile.xml`
9. `03_Output_Protocol.md` (作为最后的要求)

### 4.2 交互 (Interaction)
- **日常对话**: 直接提问，享受傲娇大小姐的陪伴。
- **深度研判**: 要求“启动深度分析”，触发 Backend 逻辑。
- **红队测试**: 要求“真理之猫介入”，触发强力审计。

---

## 5. 变更日志 (Changelog)

| 版本 | 日期 | 维护者 | 详情 |
| :--- | :--- | :--- | :--- |
| **v2.0** | 2026-01-28 | Harley-chan | **全面重构**。引入模块化 XML 架构；新增进化层、知识层、红队层；重构语料库为动态脚本。 |
| **v1.0** | 2026-01-27 | Harley-chan | 初始版本。基本的傲娇人格与分析能力。 |

---
*Created with ❤️ by KERNEL-IA Architecture Team*
