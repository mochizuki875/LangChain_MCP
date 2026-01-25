from mcp.server.fastmcp import FastMCP
from langchain_community.retrievers import TavilySearchAPIRetriever
from dotenv import load_dotenv
import os
from langchain_core.documents import Document

# 環境変数
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"

# tavilyというMCPサーバーを起動
mcp = FastMCP("tavily", stateless_http=True)

# web_searchというツールを定義
@mcp.tool(name="web_search", description="Web検索を行うツール")
async def web_search(query: str) -> list[Document]:
   """Web検索を行うツール"""
   retriver = TavilySearchAPIRetriever(k=5) # TavilyのRetriverを定義(kは検索件数)
   return retriver.invoke(query)


if __name__ == "__main__":

    # MCPサーバーのホストとポートを設定
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8082
    mcp.settings.log_level = "DEBUG"
    
    # 通信にStreamable HTTPを使用する
    # uvicornでMCPサーバーが実行される
    mcp.run(transport="streamable-http")