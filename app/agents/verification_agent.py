from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import llm


class VerificationState(TypedDict):
    topic: str
    sources: list
    research_summary: str
    verified_facts: str
    source_count: int


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, dict):
        text = content.get("text", "")
        if text:
            return str(text).strip()

        nested = content.get("content", "")
        if nested:
            return extract_text(nested)

        return ""

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                if item.strip():
                    parts.append(item.strip())

            elif isinstance(item, dict):
                text = item.get("text", "")

                if text:
                    parts.append(str(text).strip())

                elif item.get("content"):
                    nested = extract_text(item["content"])

                    if nested:
                        parts.append(nested)

            elif hasattr(item, "text"):
                text = getattr(item, "text", "")

                if text:
                    parts.append(str(text).strip())

        return "\n".join(parts).strip()

    return str(content).strip()


def verify_research(state: VerificationState):

    sources = state["sources"]

    if not sources:
        return {
            "verified_facts": (
                "No sources were available for verification."
            ),
            "source_count": 0,
        }

    source_parts = []

    for index, source in enumerate(
        sources[:5],
        start=1,
    ):
        title = str(
            source.get("title", "")
        ).strip()

        content = str(
            source.get("content", "")
        ).strip()

        if len(content) > 600:
            content = content[:600] + "..."

        source_parts.append(
            f"SOURCE {index}\n"
            f"Title: {title}\n"
            f"Content: {content}"
        )

    source_text = "\n\n".join(
        source_parts
    )

    research_summary = state["research_summary"]

    if len(research_summary) > 2000:
        research_summary = (
            research_summary[:2000] + "..."
        )

    prompt = f"""
You are the Verification Agent of SocialPilot AI.

Verify the research for this topic:

TOPIC:
{state["topic"]}

RESEARCH SUMMARY:
{research_summary}

SOURCE EVIDENCE:
{source_text}

Identify only claims that are reasonably supported by the
provided evidence.

Do not invent facts.
Do not add outside information.
Do not treat opinions or predictions as established facts.

Return ONLY:

VERIFIED FACTS
- fact 1
- fact 2
- fact 3

UNCERTAIN CLAIMS
- claim or NONE

RECOMMENDATION
- information safe to use in the social media post
"""

    try:
        response = llm.invoke(prompt)

        verified_facts = extract_text(
            response.content
        )

    except Exception:
        verified_facts = ""

    if not verified_facts:
        verified_facts = (
            "Verification Agent did not return a "
            "usable verification report."
        )

    return {
        "verified_facts": verified_facts,
        "source_count": len(sources),
    }


graph = StateGraph(VerificationState)

graph.add_node(
    "verify_research",
    verify_research,
)

graph.add_edge(
    START,
    "verify_research",
)

graph.add_edge(
    "verify_research",
    END,
)

verification_agent = graph.compile()