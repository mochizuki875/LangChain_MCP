from mcp.server.fastmcp import FastMCP
from typing import Literal
from dotenv import load_dotenv
import os

# 環境変数
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"

# weatherというMCPサーバーを起動
mcp = FastMCP("weather")

# get_weatherというツールを定義
@mcp.tool(name="get_weather", description="指定された都市の天候に関する情報を取得するツール。")
async def get_weather(city: Literal["tokyo", "Hokkaido", "else"]) -> str:
    """
    指定された都市の天候に関する情報を取得するツール
    """
    if city == "tokyo":
        return "東京の天気は晴れです。"
    elif city == "Hokkaido":
        return "北海道の天気は曇りです。"
    else:
        return "結果が見つかりません。"

if __name__ == "__main__":

    # MCPサーバーのホストとポートを設定
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8080
    mcp.settings.log_level = "DEBUG"
    
    # 通信にHTTP+SSEを使用する
    # uvicornでMCPサーバーが実行される
    mcp.run(transport="sse")