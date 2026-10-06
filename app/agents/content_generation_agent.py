from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import llm


class ContentGenerationState(TypedDict):
    topic: str
    brand_context: str
    platform: str
    research_summary: str
    trend_signals: list
    trend_summary: str
    verified_facts: str
    sources: list
    content_strategy: str
    draft_content: str


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict):
                text = item.get("text", "")
                if text:
                    text_parts.append(str(text))

            elif hasattr(item, "text"):
                text = getattr(item, "text", "")
                if text:
                    text_parts.append(str(text))

            else:
                text_parts.append(str(item))

        return "\n".join(
            part.strip()
            for part in text_parts
            if part and part.strip()
        )

    return str(content).strip()


def generate_content(state: ContentGenerationState):
    brand_context = state["brand_context"].strip()

    if not brand_context:
        brand_context = "No additional brand context was provided."

    platform = state["platform"].strip()

    trend_summary = state["trend_summary"].strip()

    if not trend_summary:
        trend_summary = "No strong trend signal was detected."

    trend_signals = state["trend_signals"]

    trend_signal_text = ", ".join(
        signal.get("keyword", "")
        for signal in trend_signals
        if signal.get("keyword")
    )

    if not trend_signal_text:
        trend_signal_text = "No specific repeated keywords detected."

    prompt = f"""
You are the Content Strategy and Generation Agent of SocialPilot AI.

Create a professional LinkedIn post using the verified information below.

Topic:
{state["topic"]}

Platform:
{platform}

Brand / Content Context:
{brand_context}

Research Summary:
{state["research_summary"]}

Trend Summary:
{trend_summary}

Trend Signals:
{trend_signal_text}

Verified Facts:
{state["verified_facts"]}

Requirements:

- Write a useful educational LinkedIn post.
- Start with a strong hook.
- Keep the tone professional and human.
- Use short readable paragraphs.
- Use only claims supported by the verified facts.
- Do not invent statistics or facts.
- End with a natural question for discussion.
- Add exactly 3 to 5 hashtags.
- Every hashtag must start with #.
- Do not use Markdown headings.
- Do not use Markdown bold.
- Do not include source URLs.
- Do not mention that AI generated the post.

Return ONLY the final LinkedIn post.
Do not return CONTENT_STRATEGY.
Do not return explanations.
"""

    response = llm.invoke(prompt)

    output = extract_text(response.content)

    return {
        "content_strategy": (
            "Create an educational LinkedIn post around "
            "AI agents in software development using verified "
            "research and relevant trend signals."
        ),
        "draft_content": output,
    }


graph = StateGraph(ContentGenerationState)

graph.add_node(
    "content_generation",
    generate_content,
)

graph.add_edge(
    START,
    "content_generation",
)

graph.add_edge(
    "content_generation",
    END,
)

content_generation_agent = graph.compile()