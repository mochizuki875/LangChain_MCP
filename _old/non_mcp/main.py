from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from typing import Literal
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults

# 環境変数
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langchain-study"

@tool
def get_weather(city: Literal["tokyo", "Hokkaido", "else"]) -> str:
    """
    指定された都市の天候に関する情報を取得するツール
    """
    if city == "tokyo":
        return "東京の天気は晴れです。"
    elif city == "Hokkaido":
        return "北海道の天気は曇りです。"
    else:
        return "結果が見つかりません。"

@tool
def get_restaurant(dish: str) -> str:
    """
    指定された料理に対しておすすめのレストランの情報を取得するツール
    """
    if dish == "ハンバーガー":
        return "マクドナルド"
    elif dish == "ラーメン":
        return "二郎"
    else:
        return "結果が見つかりません。"
    
web_search = TavilySearchResults(max_results=5)

# モデルの定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def main():
    prompt = """
    "あなたは旅行アシスタントです。"
    "ユーザーからの質問に答えてください。"
    "各ツールを実行して特定の情報を取得できなかった場合は、その内容について必ずWeb検索を行い、その結果を踏まえて回答してください。"
    "Web検索は、web_searchツールを使用してください。"
    """
    tools = [get_weather, get_restaurant, web_search]
    agent = create_react_agent(model, tools=tools, prompt=prompt)

    result = agent.invoke({"messages": "山形で餃子が食べたいな。天気も心配だ。"})

    print("=== 全てのメッセージを表示 ===")
    for message in result["messages"]:
        print(f"{message.__class__.__name__}: {message}")

    print("=== 最終的な回答のみを表示 ===")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()