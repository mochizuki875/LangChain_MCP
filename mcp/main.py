from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# 環境変数
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"

# モデルの定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = """
"あなたは旅行アシスタントです。"
"ユーザーからの質問に答えてください。"
"各ツールを実行して特定の情報を取得できなかった場合は、その内容について必ずWeb検索を行い、その結果を踏まえて回答してください。"
"Web検索は、web_searchツールを使用してください。"
"""

async def main():

    async with MultiServerMCPClient(
    {
        "weather": {
            "url": "http://localhost:8080/sse",
            "transport": "sse",
        },
        "restaurant": {
            "url": "http://localhost:8081/sse",
            "transport": "sse",
        },
        "tavily": {
            "url": "http://localhost:8082/sse",
            "transport": "sse",
        }
    }
) as client:
        
        agent = create_react_agent(model, client.get_tools(), prompt=prompt)
        result = await agent.ainvoke({"messages": "山形で餃子が食べたいな。天気も心配だ。"})

        print("=== 全てのメッセージを表示 ===")
        for message in result["messages"]:
            print(f"{message.__class__.__name__}: {message}")

        print("=== 最終的な回答のみを表示 ===")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())