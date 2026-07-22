from langchain_core.tools import tool
from app.core.config import tavily_client

@tool
def web_search(query: str) -> str:
    """Searches the web for current information, news, or factual data."""
    results = tavily_client.invoke(query)
    print("tool result ***************",results)
    return f"[Search Results: {results}]"
