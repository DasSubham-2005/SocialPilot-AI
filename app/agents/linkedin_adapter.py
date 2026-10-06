import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class LinkedInAdapterState(TypedDict):
    topic: str
    draft_content: str
    linkedin_content: str


def clean_linkedin_content(content: str) -> str:
    if not content:
        return ""

    content = content.strip()

    content = content.replace("**", "")
    content = content.replace("__", "")

    content = re.sub(r"(?m)^#{1,6}\s+", "", content)

    content = re.sub(r"[ \t]+", " ", content)

    content = re.sub(r"\n{3,}", "\n\n", content)

    content = re.sub(r"[ \t]+\n", "\n", content)

    content = re.sub(r"\n[ \t]+", "\n", content)

    content = re.sub(r"(?<=[a-zA-Z])([.!?,;:])(?=[A-Za-z])", r"\1 ", content)

    return content.strip()


def adapt_for_linkedin(state: LinkedInAdapterState):
    draft_content = state["draft_content"]

    linkedin_content = clean_linkedin_content(draft_content)

    return {
        "linkedin_content": linkedin_content
    }


graph = StateGraph(LinkedInAdapterState)

graph.add_node("linkedin_adapter", adapt_for_linkedin)

graph.add_edge(START, "linkedin_adapter")
graph.add_edge("linkedin_adapter", END)

linkedin_adapter = graph.compile()