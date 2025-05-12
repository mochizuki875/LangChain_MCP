from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

# 環境変数
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"

# restaurantというMCPサーバーを起動
mcp = FastMCP("restaurant")

# get_restaurantというツールを定義
@mcp.tool(name="get_restaurant", description="指定された料理に対しておすすめのレストランの情報を取得するツール")
async def get_restaurant(dish: str) -> str:
    """
    指定された料理に対しておすすめのレストランの情報を取得するツール
    """
    if dish == "ハンバーガー":
        return "マクドナルド"
    elif dish == "ラーメン":
        return "二郎"
    else:
        return "結果が見つかりません。"

if __name__ == "__main__":

    # MCPサーバーのホストとポートを設定
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8081
    mcp.settings.log_level = "DEBUG"
    
    # 通信にHTTP+SSEを使用する
    # uvicornでMCPサーバーが実行される
    mcp.run(transport="sse")