# 架构可视化图谱

> **版本**：v2.0
> **维护者**：哈雷酱 (￣▽￣)／
> **最后更新**：2026-03-08
> **说明**：本文档使用 Mermaid 图表展示系统架构、数据流向、实体关系

---

## 系统整体架构图

展示用户交互层、知识库层、代码层、基础设施层的整体关系。

```mermaid
graph TB
    subgraph 用户交互层
        A1[Obsidian GUI]
        A2[Python CLI]
        A3[AI Agent]
    end

    subgraph 知识库层[知识库层 - 无敌战警1.0]
        B1[08-大脑核心<br/>记忆系统]
        B2[09-灵魂系统<br/>人格系统]
        B3[知识模块<br/>00-07, 10]
    end

    subgraph 代码层[代码层 - 无敌战警-engine]
        C1[Context OS v3.0<br/>上下文编排器]
        C2[工作流自动化引擎<br/>workflow_automation]
    end

    subgraph 基础设施层
        D1[LLM API<br/>OpenRouter]
        D2[Embedding API<br/>ModelScope]
        D3[Vector DB<br/>LanceDB]
        D4[File System]
    end

    A1 --> B1
    A1 --> B2
    A1 --> B3
    A2 --> C1
    A2 --> C2
    A3 --> C1

    C1 --> B1
    C1 --> B2
    C2 --> B3

    C1 --> D1
    C2 --> D2
    C2 --> D3
    C2 --> D4

    style B1 fill:#e1f5ff
    style B2 fill:#fff4e1
    style C1 fill:#f0e1ff
    style C2 fill:#e1ffe1
```

---

## Subagent 网络架构图

展示三核底座、主代理 Copilot、6 个核心 Subagent 和调度层的完整架构。

```mermaid
graph TB
    subgraph 底层公理[底层公理 Foundations]
        PF[人格公理]
        MF[记忆公理]
        EF[演进公理]
    end

    subgraph 三核[三核 Kernels]
        PK[Persona Kernel<br/>人格核]
        MK[Memory Kernel<br/>记忆核]
        EK[Evolution Kernel<br/>演进核]
    end

    subgraph 能力层[能力层 Capability Layer]
        PROF[职业身份]
        SKILL[技能包]
        METHOD[方法包]
        OUTPUT[输出协议]
    end

    subgraph 调度层[调度层 Gateway / Scheduler]
        EG[Entry Gateway<br/>入口网关]
        SR[Session Router<br/>会话路由]
        AD[Agent Dispatcher<br/>代理分发]
        CA[Channel Adapter<br/>渠道适配]
        PR[Plugin Runtime<br/>插件运行时]
    end

    subgraph 代理层[代理层 Agent Network]
        CP[Copilot<br/>主协调代理]

        subgraph Subagents[核心 Subagent]
            MA[Memory Agent<br/>记忆代理]
            RA[Research Agent<br/>研究代理]
            DA[Decision Agent<br/>决策代理]
            WA[Writing Agent<br/>写作代理]
            FA[Reflection Agent<br/>反思代理]
            EA[Evolution Agent<br/>演进代理]
        end
    end

    subgraph 数据层[数据与存储层 Data Layer]
        VAULT[Obsidian Vault]
        REG[Memory Registry]
        IDX[Retrieval Index]
        EVOLOG[Evolution Log]
    end

    PF --> PK
    MF --> MK
    EF --> EK

    PK --> PROF
    PK --> METHOD
    PK --> OUTPUT
    EK --> SKILL
    MK --> REG
    MK --> IDX

    EG --> SR
    CA --> EG
    SR --> AD
    AD --> CP

    CP --> MA
    CP --> RA
    CP --> DA
    CP --> WA
    CP --> FA
    CP --> EA

    PR --> CP
    PR --> MA
    PR --> RA
    PR --> DA
    PR --> WA
    PR --> FA
    PR --> EA

    MA --> MK
    RA --> IDX
    DA --> MK
    WA --> OUTPUT
    FA --> EVOLOG
    EA --> EK

    MK --> VAULT
    MK --> REG
    MK --> IDX
    EK --> EVOLOG

    style PK fill:#fff4e1
    style MK fill:#e1f5ff
    style EK fill:#ffe1e1
    style CP fill:#f0e1ff
    style MA fill:#e1ffe1
    style RA fill:#e1ffe1
    style DA fill:#e1ffe1
    style WA fill:#e1ffe1
    style FA fill:#e1ffe1
    style EA fill:#e1ffe1
```

---

## 调度层详细架构图

展示调度层 5 个核心模块的详细结构和交互关系。

```mermaid
graph TB
    subgraph 入口层[Entry Layer]
        E1[Obsidian 事件]
        E2[CLI 命令]
        E3[快捷命令]
        E4[移动端]
        E5[外部消息]
    end

    subgraph Gateway[Agent Gateway 调度总线]
        subgraph EG[Entry Gateway 入口网关]
            EG1[事件监听器]
            EG2[命令解析器]
            EG3[请求验证器]
        end

        subgraph SR[Session Router 会话路由]
            SR1[任务分类器]
            SR2[模式选择器]
            SR3{执行模式}
        end

        subgraph AD[Agent Dispatcher 代理分发]
            AD1[Subagent 选择器]
            AD2[协作编排器]
            AD3[上下文构建器]
        end

        subgraph CA[Channel Adapter 渠道适配]
            CA1[Obsidian Adapter]
            CA2[CLI Adapter]
            CA3[WebSocket Adapter]
            CA4[REST API Adapter]
        end

        subgraph PR[Plugin Runtime 插件运行时]
            PR1[工具注册表]
            PR2[工具调用器]
            PR3[结果缓存]
        end
    end

    subgraph 执行层[Execution Layer]
        COPILOT[Copilot 主代理]
        SUBAGENTS[Subagent 网络]
    end

    E1 --> CA1
    E2 --> CA2
    E3 --> CA1
    E4 --> CA3
    E5 --> CA4

    CA1 --> EG1
    CA2 --> EG2
    CA3 --> EG1
    CA4 --> EG2

    EG1 --> EG3
    EG2 --> EG3
    EG3 --> SR1

    SR1 --> SR2
    SR2 --> SR3

    SR3 -->|chat| AD1
    SR3 -->|research| AD1
    SR3 -->|archive| AD1
    SR3 -->|write| AD1
    SR3 -->|reflect| AD1
    SR3 -->|evolve| AD1

    AD1 --> AD2
    AD2 --> AD3
    AD3 --> COPILOT

    COPILOT --> SUBAGENTS

    PR1 --> PR2
    PR2 --> PR3
    PR3 --> SUBAGENTS

    style EG fill:#e1f5ff
    style SR fill:#fff4e1
    style AD fill:#f0e1ff
    style CA fill:#e1ffe1
    style PR fill:#ffe1e1
```

---

## 知识库模块关系图

展示知识库 10 个模块之间的关系和数据流向。

```mermaid
graph TD
    M00[00-每日工作区<br/>日常任务与信息暂存]
    M01[01-研究方法论<br/>方法论积累]
    M02[02-政策于宏观库<br/>政策研究]
    M03[03-行业研究库<br/>行业监测]
    M04[04-专题研究库<br/>专题研究]
    M05[05-AI技术文档<br/>技术积累]
    M06[06-个人成长<br/>学习成长]
    M07[07-完成归档<br/>项目归档]
    M08[08-大脑核心<br/>记忆系统]
    M09[09-灵魂系统<br/>人格系统]
    M10[10-个人日记<br/>日记计划]

    M00 -->|信息采集| M00
    M00 -->|三行摘要| M00
    M00 -->|知识沉淀| M02
    M00 -->|知识沉淀| M03
    M00 -->|知识沉淀| M04
    M00 -->|完成归档| M07

    M01 -->|方法论指导| M00
    M01 -->|方法论指导| M02
    M01 -->|方法论指导| M03
    M01 -->|方法论指导| M04

    M05 -->|技术支持| M00
    M05 -->|AI增强| M08
    M05 -->|AI增强| M09

    M08 -->|记忆加载| AI[AI Agent]
    M09 -->|人格加载| AI

    AI -->|对话精华| M08
    AI -->|决策日志| M08
    AI -->|项目记忆| M08

    M06 -->|个人成长| M10
    M10 -->|日记记录| M08

    style M08 fill:#e1f5ff
    style M09 fill:#fff4e1
    style M00 fill:#ffe1e1
    style AI fill:#f0e1ff
```

---

## 数据流向图

### 日常工作流数据流

```mermaid
flowchart TD
    START([用户输入材料])

    START --> A[00-每日工作区/01-待处理材料/]
    A --> B{AI Analyzer<br/>三行摘要}
    B --> C[00-每日工作区/03-三行摘要收集/]
    C --> D{AI Analyzer<br/>洞察提炼}
    D --> E{Knowledge Manager<br/>自动归档}

    E -->|政策类| F[02-政策于宏观库/]
    E -->|行业类| G[03-行业研究库/]
    E -->|专题类| H[04-专题研究库/]

    F --> I[索引更新]
    G --> I
    H --> I

    I --> J[08-大脑核心/项目记忆/]

    J --> END([知识沉淀完成])

    style START fill:#e1ffe1
    style END fill:#e1ffe1
    style B fill:#f0e1ff
    style D fill:#f0e1ff
    style E fill:#f0e1ff
```

### AI 会话数据流

```mermaid
flowchart TD
    START([用户发起会话])

    START --> A{Context OS v3.0<br/>加载记忆}

    A --> B1[读取用户画像]
    A --> B2[读取偏好设定]
    A --> B3[读取上下文快照]
    A --> B4[读取项目记忆]

    B1 --> C{Orchestrator<br/>编排上下文}
    B2 --> C
    B3 --> C
    B4 --> C

    C --> D1[Intent 验证]
    C --> D2[Budget 检查]
    C --> D3[装箱策略]

    D1 --> E{Provider Adapter<br/>格式化消息}
    D2 --> E
    D3 --> E

    E --> F[调用 LLM API]
    F --> G[返回响应]
    G --> H[提取对话精华]
    H --> I[存档到 08-大脑核心/对话精华/]

    I --> END([会话结束])

    style START fill:#e1ffe1
    style END fill:#e1ffe1
    style A fill:#f0e1ff
    style C fill:#f0e1ff
    style E fill:#f0e1ff
    style F fill:#ffe1e1
```

---

## Context OS v3.0 架构图

展示 Context OS v3.0 的核心组件和工作流程。

```mermaid
graph TB
    subgraph Input[输入层]
        I1[用户问题]
        I2[记忆块配置]
        I3[人格配置]
    end

    subgraph ContextOS[Context OS v3.0]
        subgraph IntentSystem[Intent System]
            IS1[Intent 分类器]
            IS2[directive<br/>指令/规则]
            IS3[reference<br/>参考/上下文]
        end

        subgraph BudgetManager[Budget Manager]
            BM1[Total Budget<br/>12000 tokens]
            BM2[Reserve<br/>1500 tokens]
            BM3[System Max<br/>8000 tokens]
        end

        subgraph Orchestrator[Orchestrator 编排器]
            OR1[读取 ContextBlock]
            OR2[Intent 验证]
            OR3[Budget 分配]
            OR4[装箱策略]
            OR5[优先级排序]
        end

        subgraph ProviderAdapter[Provider Adapter]
            PA1[OpenAI 格式]
            PA2[Anthropic 格式]
            PA3[OpenRouter 格式]
        end
    end

    subgraph Output[输出层]
        O1[格式化消息]
        O2[LLM API 调用]
        O3[响应返回]
    end

    I1 --> OR1
    I2 --> OR1
    I3 --> OR1

    OR1 --> IS1
    IS1 --> IS2
    IS1 --> IS3

    IS2 --> OR2
    IS3 --> OR2

    OR2 --> BM1
    BM1 --> BM2
    BM1 --> BM3

    BM3 --> OR3
    OR3 --> OR4
    OR4 --> OR5

    OR5 --> PA1
    OR5 --> PA2
    OR5 --> PA3

    PA1 --> O1
    PA2 --> O1
    PA3 --> O1

    O1 --> O2
    O2 --> O3

    style IntentSystem fill:#e1f5ff
    style BudgetManager fill:#fff4e1
    style Orchestrator fill:#f0e1ff
    style ProviderAdapter fill:#e1ffe1
```

---

## Subagent 协作模式图

展示 4 种 Subagent 协作模式。

### 模式 1：串行（Sequential）

```mermaid
graph LR
    START([任务开始]) --> MA[Memory Agent<br/>唤醒记忆]
    MA --> RA[Research Agent<br/>信息研究]
    RA --> WA[Writing Agent<br/>生成输出]
    WA --> END([任务完成])

    style MA fill:#e1ffe1
    style RA fill:#e1ffe1
    style WA fill:#e1ffe1
```

### 模式 2：并行（Parallel）

```mermaid
graph TB
    START([任务开始]) --> SPLIT{任务分发}

    SPLIT --> RA[Research Agent<br/>信息研究]
    SPLIT --> DA[Decision Agent<br/>决策分析]
    SPLIT --> WA[Writing Agent<br/>草稿生成]

    RA --> MERGE{结果汇总}
    DA --> MERGE
    WA --> MERGE

    MERGE --> END([任务完成])

    style RA fill:#e1ffe1
    style DA fill:#e1ffe1
    style WA fill:#e1ffe1
```

### 模式 3：条件分支（Conditional）

```mermaid
graph TB
    START([任务开始]) --> MA[Memory Agent<br/>读取上下文]
    MA --> JUDGE{判断任务类型}

    JUDGE -->|研究类| RA[Research Agent]
    JUDGE -->|决策类| DA[Decision Agent]
    JUDGE -->|写作类| WA[Writing Agent]

    RA --> END([任务完成])
    DA --> END
    WA --> END

    style MA fill:#e1ffe1
    style RA fill:#e1ffe1
    style DA fill:#e1ffe1
    style WA fill:#e1ffe1
```

### 模式 4：循环迭代（Iterative）

```mermaid
graph TB
    START([任务开始]) --> RA[Research Agent<br/>信息研究]
    RA --> DA[Decision Agent<br/>决策分析]
    DA --> JUDGE{质量检查}

    JUDGE -->|不满足| RA
    JUDGE -->|满足| FA[Reflection Agent<br/>反思总结]
    FA --> END([任务完成])

    style RA fill:#e1ffe1
    style DA fill:#e1ffe1
    style FA fill:#e1ffe1
```

---

## 记忆权限控制图

展示不同 Subagent 对记忆的读写权限分级。

```mermaid
graph TB
    subgraph 记忆层级[记忆层级 Memory Hierarchy]
        L1[工作记忆<br/>Working Memory]
        L2[用户记忆<br/>User Memory]
        L3[决策记忆<br/>Decision Memory]
        L4[角色记忆<br/>Role Memory]
        L5[能力升级<br/>Capability Upgrade]
        L6[演进规则<br/>Evolution Rules]
    end

    subgraph 权限级别[权限级别 Permission Levels]
        P1[普通写回<br/>Normal Write]
        P2[重要写回<br/>Important Write]
        P3[高门槛写回<br/>Critical Write]
    end

    subgraph Subagent权限[Subagent 权限矩阵]
        MA[Memory Agent]
        RA[Research Agent]
        DA[Decision Agent]
        WA[Writing Agent]
        FA[Reflection Agent]
        EA[Evolution Agent]
    end

    L1 --> P1
    L2 --> P2
    L3 --> P2
    L4 --> P3
    L5 --> P3
    L6 --> P3

    MA -->|读:全部<br/>写:L1,L2| P1
    MA -->|需确认| P2

    RA -->|读:L1,知识库<br/>写:L1| P1

    DA -->|读:全部<br/>写:L1,L3| P1
    DA -->|需确认| P2

    WA -->|读:L1,L3<br/>写:输出文档| P1

    FA -->|读:全部<br/>写:L1,反思记录| P1

    EA -->|读:全部<br/>写:L4,L5,L6| P3

    style L1 fill:#e1ffe1
    style L2 fill:#fff4e1
    style L3 fill:#fff4e1
    style L4 fill:#ffe1e1
    style L5 fill:#ffe1e1
    style L6 fill:#ffe1e1
    style P1 fill:#e1f5ff
    style P2 fill:#f0e1ff
    style P3 fill:#ffe1e1
```

---

## AI 会话时序图

展示用户与 AI 交互的完整时序流程。

```mermaid
sequenceDiagram
    actor User as 用户
    participant Obsidian as Obsidian
    participant CLI as Python CLI
    participant ContextOS as Context OS v3.0
    participant KB as 知识库
    participant LLM as LLM API

    User->>Obsidian: 1. 复制上下文快照
    Obsidian->>User: 返回快照内容
    User->>LLM: 2. 粘贴快照 + 提问

    Note over LLM: 或通过 CLI 自动加载

    User->>CLI: 3. python main.py analyze
    CLI->>ContextOS: 初始化上下文编排器
    ContextOS->>KB: 读取用户画像
    KB-->>ContextOS: 返回画像数据
    ContextOS->>KB: 读取偏好设定
    KB-->>ContextOS: 返回偏好数据
    ContextOS->>KB: 读取项目记忆
    KB-->>ContextOS: 返回记忆数据

    ContextOS->>ContextOS: Intent 分类
    ContextOS->>ContextOS: Budget 检查
    ContextOS->>ContextOS: 装箱策略

    ContextOS->>LLM: 调用 API（格式化消息）
    LLM-->>ContextOS: 返回响应

    ContextOS->>CLI: 返回分析结果
    CLI->>User: 展示结果

    User->>CLI: 4. 提取对话精华
    CLI->>KB: 存档到 08-大脑核心/对话精华/
    KB-->>CLI: 存档成功

    CLI->>User: 完成
```

---

## 颜色编码说明

| 颜色 | 含义 |
|------|------|
| 蓝色（#e1f5ff） | 记忆系统相关 |
| 黄色（#fff4e1） | 人格系统相关 |
| 紫色（#f0e1ff） | 代码层/AI 相关 |
| 绿色（#e1ffe1） | 基础设施/工具 |
| 红色（#ffe1e1） | 工作区/临时数据 |

---

**维护者**：哈雷酱 (￣▽￣)／
**最后更新**：2026-03-07
