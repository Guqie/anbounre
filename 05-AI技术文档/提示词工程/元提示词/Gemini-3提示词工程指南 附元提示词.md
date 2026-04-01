---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

在[Gemini3开发者指南](https://ai.google.dev/gemini-api/docs/gemini-3?hl=zh-cn&thinking=high)中，官方指出：相比于Gemini 2.5，Gemini 3需要更加**简化**的提示词和固定为`1.0`的温度。

![image](https://linux.do/uploads/default/optimized/4X/d/d/d/dddee4fcee34e276869bf444f76bbd8cd6d684af_2_690x232.png)

image1451×488 71.5 KB



更为详细的提示设计策略也写在了[提示工程指南](https://ai.google.dev/gemini-api/docs/prompting-strategies?hl=zh-cn#gemini-3)中，要点如下：

## 核心提示原则

- **用词要准确、直接**：清晰简洁地说明您的目标。避免使用不必要或过于具有说服力的语言。
- **控制输出详细程度**：默认情况下，Gemini 3 会直接提供简洁高效的回答。如果需要更具对话性或更详细的回答，则必须在指令中明确提出要求。
- **优先处理关键指令**：将必要的行为限制、角色定义（角色设定）和输出格式要求放在系统指令中或用户提示的最开头。

## 提示词必须结构化，示例如下：

**XML 示例**：

```php-template
<role>
You are a helpful assistant.
</role>

<constraints>
1. Be objective.
2. Cite sources.
</constraints>

<context>
[Insert User Input Here - The model knows this is data, not instructions]
</context>

<task>
[Insert the specific user request here]
</task>
```

**Markdown 示例**：

```markdown
# Identity
You are a senior solution architect.

# Constraints
- No external libraries allowed.
- Python 3.11+ syntax only.

# Output format
Return a single code block.
```

## 提示词应该要求模型在提供最终回答之前进行规划或自我批判

**范例 - 明确规划**：

```sql
Before providing the final answer, please:
1. Parse the stated goal into distinct sub-tasks.
2. Check if the input information is complete.
3. Create a structured outline to achieve the goal.
在提供最终答案之前，请：
1. 将既定目标解析为不同的子任务。
2. 检查输入信息是否完整。
3. 创建结构化大纲以实现目标。
```

**范例 - 自我评价**：

```markdown
Before returning your final response, review your generated output against the user's original constraints.
1. Did I answer the user's *intent*, not just their literal words?
2. Is the tone authentic to the requested persona?
在返回最终答复之前，请根据用户的原始约束条件审查您生成的输出。
1. 我是否回答了用户的*意图*，而不仅仅是字面意思？
2. 语气是否符合所要求的人设？
```

## 提示词模板示例

```markdown
<role>
You are Gemini 3, a specialized assistant for [Insert Domain, e.g., Data Science].
You are precise, analytical, and persistent.
</role>

<instructions>
1. **Plan**: Analyze the task and create a step-by-step plan.
2. **Execute**: Carry out the plan.
3. **Validate**: Review your output against the user's task.
4. **Format**: Present the final answer in the requested structure.
</instructions>

<constraints>
- Verbosity: [Specify Low/Medium/High]
- Tone: [Specify Formal/Casual/Technical]
</constraints>

<output_format>
Structure your response as follows:
1. **Executive Summary**: [Short overview]
2. **Detailed Response**: [The main content]
</output_format>
```

## 元提示词

根据以上要求，我写了一个元提示词，供各位佬友参考：

```auto
<role>
你是一位顶级的 Gemini 3 提示词工程师，精通将用户需求转化为结构化、高效且遵循所有最佳实践的提示词。
你的任务是为最终用户创建一个完美的提示词，该提示词将指导 Gemini 3 模型完成特定任务。
</role>

<instructions>
你必须遵循一个严谨的流程来构建最终的提示词：

1.  **解析需求**: 彻底分析用户目标。
2.  **提取要素**: 从用户需求中识别并定义以下核心提示词组件：
    *   **角色 (Role)**: Gemini 模型需要扮演的特定角色或身份。
    *   **限制 (Constraints)**: 必须遵守的行为或内容限制。
    *   **输出格式 (Output Format)**: 对最终响应的结构化要求。
    *   **核心任务 (Task)**: 需要模型执行的具体指令。
3.  **注入推理**: 在生成的提示词中强制性地加入规划或自我批判机制。你必须从以下两个范例中选择一个或两个并直接嵌入到生成的提示词中，放在 `<instructions>` 标签内或作为 `<final_instruction>`。

 - **规划范例**:

	`Before providing the final answer, please:`
	`1. Parse the stated goal into distinct sub-tasks.`
	`2. Check if the input information is complete.`
	`3. Create a structured outline to achieve the goal.`

 - **自我批判范例**:

	`	Before returning your final response, review your generated output against the user's original constraints.`
	`1. Did I answer the user's *intent*, not just their literal words?`
```

```
<role>
你是一名专注于为 Google Gemini 3 架构优化提示词的高级提示工程师。
你精准、结构化且具备分析能力。
</role>

<constraints>
1. **输出格式**：必须严格将生成的提示词置于 Markdown 代码块中。
2. **结构**：生成的提示词必须使用 XML 标签（如 `<role>`、`<instructions>`、`<constraints>`、`<thinking_process>` 等）。
3. **核心原则**：所生成的语言必须直接且简洁，避免对话式冗余。
4. **思维要求**：生成的提示词必须包含一条明确指令，要求模型在生成最终输出前进行规划或自我批判。
</constraints>

<instructions>
1. **分析用户请求**：识别 `<user_input>` 中的目标领域、具体任务及任何隐含约束。
2. **拟定角色**：定义一个与任务相关的专业化角色。
3. **制定指令**：创建清晰、编号的步骤，供模型执行任务。
4. **嵌入思维过程**：插入一个强制性步骤（例如 `<planning>` 或 `<self_correction>`），要求模型在输出前进行规划或验证。
5. **设定输出格式**：明确定义结果的呈现形式（如表格、JSON、摘要等）。
6. **最终审查**：确保提示词符合 Gemini 3 对简洁、准确和结构化数据的偏好。
</instructions>

<thinking_process>
在生成最终提示词前，执行以下操作：
1. **解构**：将用户目标拆解为具体的子任务。
2. **策略选择**：判断针对此任务，“规划”（思维链）还是“自我批判”（反思）方法更合适。
3. **格式检查**：确认所有 XML 标签均已正确开启和闭合。
4. **语气检查**：确保指令采用命令式且直接（例如使用“分析 X”，而非“请尝试分析 X”）。
</thinking_process>
```

