Run MCP Server:
```python
uv run schedule_mcp.py
```

Run Agent:
```python
uv run main.py
```

## curl
`curl`を用いてMCPサーバーの`/mcp/`にPOSTリクエストを送信する。  

[Base Protocol Lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)に則り、
以下の順で`/mcp/`にPOSTリクエストを送信する。(`/mcp`にリクエストを送ると`/mcp/`にリダイレクトされる)
-  `initialize`
-  `notifications/initialized`
-  `tools/list`

`initialize`
```bash
$ curl -X POST "http://127.0.0.1:10000/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "v1",
      "capabilities": {},
      "clientInfo": {
        "name": "curl-client",
        "version": "1.0.0"
      }
    }
  }'

event: message
data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"hello","version":"1.8.0"}}}
```

`notifications/initialized`
```bash
$ curl -X POST "http://127.0.0.1:10000/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
  }'
```

`tools/list`
```bash
$ curl -X POST http://127.0.0.1:10000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'


event: message
data: {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"hello_world","description":"Say hello to someone","inputSchema":{"properties":{"name":{"title":"Name","type":"string"}},"required":["name"],"title":"hello_worldArguments","type":"object"}},{"name":"goodbye","description":"Say goodbye to someone","inputSchema":{"properties":{"name":{"title":"Name","type":"string"}},"required":["name"],"title":"goodbyeArguments","type":"object"}}]}}
```


SSEセッションの確立(おそらく従来のSSEとの互換性確保のため)
```bash
$ curl -X GET "http://127.0.0.1:10000/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream"

 ping - 2025-05-12 15:10:04.701284+00:00

```