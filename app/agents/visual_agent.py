from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import llm


class VisualState(TypedDict):
    topic: str
    linkedin_content: str
    verified_facts: str
    visual_brief: str


def create_visual_brief(state: VisualState):
    prompt = f"""
You are the Visual Strategy Agent of SocialPilot AI.

Your task is to create a visual brief for a professional LinkedIn post.

Topic:
{state["topic"]}

Verified Facts:
{state["verified_facts"]}

Approved LinkedIn Post:
{state["linkedin_content"]}

Create a visual concept that communicates the main idea of the post.

Important rules:

1. Use only information supported by the approved post and verified facts.
2. Do not introduce new statistics, claims, companies, people, or facts.
3. Keep the visual suitable for a professional LinkedIn audience.
4. Prefer a clean infographic or editorial technology visual.
5. Avoid excessive text inside the image.
6. Do not request copyrighted logos or trademark-heavy compositions.
7. The visual should support the post rather than repeat the entire post.
8. Make the concept useful for an eventual image-generation model.

Return exactly these sections:

VISUAL_TYPE
- ...

MAIN_CONCEPT
- ...

KEY_MESSAGE
- ...

VISUAL_ELEMENTS
- ...
- ...
- ...

LAYOUT
- ...

STYLE
- ...

COLOR_DIRECTION
- ...

IMAGE_TEXT
- ...

IMAGE_GENERATION_PROMPT
- ...

AVOID
- ...
- ...
"""

    response = llm.invoke(prompt)

    return {
        "visual_brief": response.content,
    }


graph = StateGraph(VisualState)

graph.add_node("create_visual_brief", create_visual_brief)

graph.add_edge(START, "create_visual_brief")
graph.add_edge("create_visual_brief", END)

visual_agent = graph.compile()