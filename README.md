# LangChain MCP Sample

## 題材
`LangGraph`のチュートリアルで扱われているReAct Agentをベースに、MCPを使用してTool Callingを行う例。

- [How to create a ReAct agent from scratch](https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/)
- [Prebuilt ReAct Agent](https://langchain-ai.github.io/langgraph/how-tos/#prebuilt-react-agent)
- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
  - [Multiple MCP Servers](https://github.com/langchain-ai/langchain-mcp-adapters?tab=readme-ov-file#multiple-mcp-servers)
    - MCPサーバーが複数ある場合

## パッケージインストール

```bash
pip install -qU langgraph langchain-openai langchain-mcp-adapters python-dotenv langsmith tavily-python
```

## 実装

- [Tool Calling](./non_mcp)
- [MCP stdio](./mcp_stdio)
- [MCP SSE](./mcp_sse)
- [MCP StreamableHTTP](./mcp_streamablehttp)