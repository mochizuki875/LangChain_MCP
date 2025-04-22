# math_server.py
from mcp.server.fastmcp import FastMCP

# MathというMCPサーバーを起動
mcp = FastMCP("Math")

# addというツールを定義
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# multiplyというツールを定義
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")