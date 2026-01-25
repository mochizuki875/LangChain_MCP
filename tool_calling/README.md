Run Agent:
```python
uv run main.py
```

## Tool Calling Test
```bash
curl http://edgexpert01:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d @- <<'EOF'
{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "user", "content": "What's the weather in Tokyo?"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get weather information for a location.",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "The city to get the weather for."
            }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
EOF
```

```json
{
  "id": "chatcmpl-593",
  "object": "chat.completion",
  "created": 1769362145,
  "model": "gpt-oss:20b",
  "system_fingerprint": "fp_ollama",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "",
        "reasoning": "We need to call get_weather with city \"Tokyo\".",
        "tool_calls": [
          {
            "id": "call_mprj9l1c",
            "index": 0,
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\":\"Tokyo\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 137,
    "completion_tokens": 35,
    "total_tokens": 172
  }
}
```