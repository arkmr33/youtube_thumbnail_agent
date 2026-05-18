from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilySearch(
    max_results=5,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(state):
    topic = state["topic"]

    results = tavily.invoke(
        {"query": f"YouTube thumbnail ideas for {topic}"}
    )

    summaries = []

    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")

        summaries.append(
            f"- {title}: {content[:200]}"
        )

    return {
        "search_summary": "\n".join(summaries)
    }