from mcp.server.fastmcp import FastMCP

# Initialize schedule MCP server for STDIO transport
mcp = FastMCP("schedule")

# Mock schedule data
SCHEDULES = {
    "today": [
        {"time": "01:00", "event": "Talk with Stefan at NativeCamp", "location": "NativeCamp"},
        {"time": "09:00", "event": "Drop off kids at kindergarten", "location": "Kindergarten"},
        {"time": "13:30", "event": "Get a haircut in Shinjuku", "location": "Shinjuku"},
        {"time": "17:00", "event": "Pick up kids from kindergarten", "location": "Kindergarten"},
        {"time": "18:00", "event": "AI meeting with colleagues", "location": "Online"},
    ],
    "tomorrow": [
        {"time": "10:00", "event": "Sprint planning", "location": "Conference Room B"},
        {"time": "13:00", "event": "Lunch with team", "location": "Cafeteria"},
        {"time": "15:00", "event": "Technical workshop", "location": "Training room"},
    ],
}

@mcp.tool()
def get_schedule(period: str) -> str:
    """Get schedule for a specific period. (e.g. 'today' or 'tomorrow')"""
    # Only accept 'today' or 'tomorrow'
    if period not in ["today", "tomorrow"]:
        return "No Schedule"
    
    schedules = SCHEDULES.get(period, [])
    
    if not schedules:
        return f"No schedules found for {period}."
    
    result = f"Schedule for {period}:\n\n"
    for item in schedules:
        result += f"• {item['time']}: {item['event']}\n  Location: {item['location']}\n\n"
    
    return result.strip()

if __name__ == "__main__":
    # Run MCP server using STDIO transport
    mcp.run(transport="stdio")
