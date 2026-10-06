import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import llm


class RevisionState(TypedDict):
    topic: str
    linkedin_content: str
    verified_facts: str
    sources: list
    qa_report: str
    revised_content: str


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            elif hasattr(item, "text"):
                parts.append(item.text)

        return "\n".join(
            part.strip()
            for part in parts
            if part and part.strip()
        )

    return str(content).strip()


def clean_revision(content: str) -> str:
    if not content:
        return ""

    content = content.strip()

    content = content.replace("**", "")
    content = content.replace("__", "")

    content = re.sub(
        r"(?m)^#{1,6}\s+",
        "",
        content,
    )

    content = re.sub(
        r"(?m)^\s*\*\s+",
        "- ",
        content,
    )

    content = re.sub(
        r"\n{3,}",
        "\n\n",
        content,
    )

    return content.strip()


def revise_linkedin_post(state: RevisionState):

    original_content = state["linkedin_content"]

    verified_facts = state["verified_facts"]

    if len(verified_facts) > 4000:
        verified_facts = verified_facts[:4000] + "..."

    qa_report = state["qa_report"]

    if len(qa_report) > 5000:
        qa_report = qa_report[:5000] + "..."

    prompt = f"""
You are the Revision Agent of SocialPilot AI.

Revise the LinkedIn post based on the QA report.

TOPIC:
{state["topic"]}

CURRENT POST:
{original_content}

VERIFIED FACTS:
{verified_facts}

QA REPORT:
{qa_report}

RULES:

1. Fix the issues identified by QA.
2. Preserve valid information and the core message.
3. Use only information supported by VERIFIED FACTS.
4. Never invent facts, statistics, events, companies, quotes,
   results, experiences, or technical claims.
5. Keep a professional and informative LinkedIn tone.
6. Use short readable paragraphs.
7. Keep exactly 3 to 5 relevant hashtags.
8. Every hashtag must start with #.
9. Do not use Markdown.
10. Do not include source URLs.
11. Do not mention this revision process.
12. Return ONLY the complete revised LinkedIn post.
13. Never return an empty response.
"""

    try:
        response = llm.invoke(prompt)

        revised_content = extract_text(response.content)
        revised_content = clean_revision(revised_content)

    except Exception:
        revised_content = ""

    if not revised_content:
        return {
            "revised_content": original_content
        }

    return {
        "revised_content": revised_content
    }


graph = StateGraph(RevisionState)

graph.add_node(
    "revision",
    revise_linkedin_post
)

graph.add_edge(
    START,
    "revision"
)

graph.add_edge(
    "revision",
    END
)

revision_agent = graph.compile()