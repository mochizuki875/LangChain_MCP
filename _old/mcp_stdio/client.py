import os
from dotenv import load_dotenv
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import pprint

# 環境変数を設定
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # モデルを定義

async def main():
    # MCPサーバをサブプロセスとして起動(MCPサーバーを起動するコードを実行)
    # StdioServerParametersクラスのコンストラクタによりStdioServerParametersオブジェクトを取得
    server_params = StdioServerParameters(command="python", args=["./math_server.py"])

    # MCPクライアントを起動
    # StdioServerParametersオブジェクトから受信用Stream(stdout)と送信用Stream(stdin)を取得
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:   # 使用するStreamを使ってセッションを生成
            await session.initialize()  # セッションの初期化

            tools = await load_mcp_tools(session)  # セッションを使ってツールをロード(Agentが使用するツールをMCPサーバーから取得)

            agent = create_react_agent(model, tools)  # ReAct Agentを作成(prebuiltパッケージのcreate_react_agent関数を使用)
            agent_response = await agent.ainvoke({"messages": "(3 + 5) x 12はいくつですか？"})  # エージェントにメッセージを渡して実行

            # print(agent_response)  # エージェントの応答を出力
            pprint.pprint(agent_response)  # エージェントの応答を出力

            print("===== 最終回答 =====")
            print(agent_response["messages"][-1].content)
            

if __name__ == "__main__":
    asyncio.run(main())