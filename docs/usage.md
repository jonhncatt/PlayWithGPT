# GPT 使用指南

## 1. 准备工作

1. 在 [OpenAI 平台](https://platform.openai.com/) 注册账号并创建 API Key。
2. 安装 OpenAI 官方 SDK，例如 Python 版本：

   ```bash
   pip install openai
   ```

3. 配置环境变量：

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

   在生产环境可使用密钥管理服务或 CI/CD 密文变量。

## 2. 基础请求示例

以 Chat Completions API 为例，使用 Python 发送对话请求：

```python
from openai import OpenAI

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "帮我写一段产品介绍文案"},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(response.choices[0].message.content)
```

要点：

- `model` 字段决定调用的具体模型，选择时需平衡成本与能力。
- 通过调整 `temperature`、`top_p` 控制输出的随机性。
- 设置 `max_tokens` 限制生成长度，避免超出预算。

## 3. 提示词（Prompt）设计

- **明确指令**：交代目标、语气、长度、格式。
- **提供上下文**：给出背景信息、已知事实，提高准确性。
- **给出示例**：使用少样本学习方式展示输入输出格式。
- **分步骤引导**：复杂任务中拆解流程，逐步推理。

示例：

```
你是一名资深客服，请按照以下格式回复：
1. 问题理解
2. 解答步骤
3. 注意事项

客户问题：{{用户提问}}
```

## 4. 函数调用与结构化输出

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=[
        {
            "name": "search_knowledge_base",
            "description": "根据用户问题检索知识库",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "检索关键词"}
                },
                "required": ["query"],
            },
        }
    ],
)

choice = response.choices[0]
if choice.finish_reason == "tool_calls":
    tool_call = choice.message.tool_calls[0]
    print(tool_call.function.name, tool_call.function.arguments)
```

收到工具调用后，执行相应函数并将结果重新传入对话即可。

## 5. 最佳实践

- **日志与监控**：记录请求与响应，便于调优与审计。
- **缓存与重试**：对幂等查询可使用缓存，遇到网络问题进行重试。
- **敏感内容过滤**：结合安全策略与人工审核保障内容合规。
- **成本控制**：监控 token 消耗，按需选择模型或裁剪上下文。

## 6. 常见错误

| 错误码 | 原因 | 解决方案 |
| ------ | ---- | -------- |
| 401    | 未授权 | 检查 API Key 是否正确或过期 |
| 429    | 触发限流 | 降低并发、使用队列、申请更高配额 |
| 500    | 服务异常 | 重试或联系支持渠道 |

遇到具体问题时，请参考 [docs/faq.md](faq.md)。
