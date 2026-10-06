from typing import TypedDict

from tavily import TavilyClient
from langgraph.graph import StateGraph, START, END

from app.config import TAVILY_API_KEY


class ResearchState(TypedDict):
    topic: str
    search_query: str
    sources: list
    research_summary: str


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def research_topic(state: ResearchState):
    topic = state["topic"]

    search_query = (
        f"latest important developments and trends about {topic} "
        f"for technology professionals"
    )

    response = tavily_client.search(
        query=search_query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )

    sources = []

    for result in response.get("results", []):
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
        })

    research_summary = response.get("answer", "")

    return {
        "search_query": search_query,
        "sources": sources,
        "research_summary": research_summary,
    }


graph = StateGraph(ResearchState)

graph.add_node("research", research_topic)

graph.add_edge(START, "research")
graph.add_edge("research", END)

research_agent = graph.compile()