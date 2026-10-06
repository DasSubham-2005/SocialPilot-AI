
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.research_agent import research_agent
from app.agents.trend_agent import trend_agent
from app.agents.verification_agent import verification_agent
from app.agents.content_generation_agent import content_generation_agent
from app.agents.linkedin_adapter import linkedin_adapter
from app.agents.qa_agent import qa_agent
from app.agents.revision_agent import revision_agent
from app.agents.human_approval import human_approval_agent
from app.agents.publishing_agent import publishing_agent
from app.agents.pre_publish_guard import pre_publish_guard


class SocialPilotState(TypedDict):
    topic: str
    brand_context: str
    platform: str
    search_query: str
    sources: list
    research_summary: str
    trend_signals: list
    trend_summary: str
    verified_facts: str
    source_count: int
    content_strategy: str
    draft_content: str
    linkedin_content: str
    qa_report: str
    qa_status: str
    revision_count: int
    human_decision: str
    approval_status: str
    approval_message: str
    publication_status: str
    publication_payload: dict
    publication_message: str
    guard_status: str
    guard_message: str
    revised_content: str


def run_research(state):
    return research_agent.invoke({
        "topic": state["topic"],
        "search_query": "",
        "sources": [],
        "research_summary": "",
    })


def run_trend_detection(state):
    return trend_agent.invoke({
        "topic": state["topic"],
        "sources": state["sources"],
        "trend_signals": [],
        "trend_summary": "",
    })


def run_verification(state):
    return verification_agent.invoke({
        "topic": state["topic"],
        "sources": state["sources"],
        "research_summary": state["research_summary"],
        "verified_facts": "",
        "source_count": 0,
    })


def run_content_generation(state):
    return content_generation_agent.invoke({
        "topic": state["topic"],
        "brand_context": state["brand_context"],
        "platform": state["platform"],
        "research_summary": state["research_summary"],
        "trend_signals": state["trend_signals"],
        "trend_summary": state["trend_summary"],
        "verified_facts": state["verified_facts"],
        "sources": state["sources"],
        "content_strategy": "",
        "draft_content": "",
    })


def run_linkedin_adapter(state):
    result = linkedin_adapter.invoke({
        "topic": state["topic"],
        "draft_content": state["draft_content"],
        "linkedin_content": "",
    })

    return {
        "linkedin_content": result["linkedin_content"],
    }


def run_qa(state):
    return qa_agent.invoke({
        "topic": state["topic"],
        "verified_facts": state["verified_facts"],
        "sources": state["sources"],
        "linkedin_content": state["linkedin_content"],
        "qa_report": "",
        "qa_status": "",
    })


def route_after_qa(state):
    if (
        state["qa_status"] == "NEEDS_REVISION"
        and state["revision_count"] < 1
    ):
        return "revision"

    return "approval_gate"


def run_revision(state):
    result = revision_agent.invoke({
        "topic": state["topic"],
        "linkedin_content": state["linkedin_content"],
        "verified_facts": state["verified_facts"],
        "sources": state["sources"],
        "qa_report": state["qa_report"],
        "revised_content": "",
    })

    revised_content = result.get(
        "revised_content",
        "",
    ).strip()

    if not revised_content:
        revised_content = state["linkedin_content"]

    return {
        "linkedin_content": revised_content,
        "revised_content": revised_content,
        "revision_count": state["revision_count"] + 1,
    }


def run_approval_gate(state):
    if state["qa_status"] == "NEEDS_REVISION":
        return {
            "approval_status": "BLOCKED",
            "approval_message": (
                "Approval blocked because the content still "
                "has unresolved QA issues after the maximum "
                "revision attempt."
            ),
        }

    return {
        "approval_status": "PENDING",
        "approval_message": (
            "Content passed QA and is waiting for human approval."
        ),
    }


def run_human_approval(state):
    return human_approval_agent.invoke({
        "linkedin_content": state["linkedin_content"],
        "qa_status": state["qa_status"],
        "qa_report": state["qa_report"],
        "human_decision": state["human_decision"],
        "approval_status": "",
        "approval_message": "",
    })


def route_after_approval(state):
    if state["approval_status"] == "APPROVED":
        return "publishing"

    return END


def run_publishing(state):
    return publishing_agent.invoke({
        "linkedin_content": state["linkedin_content"],
        "approval_status": state["approval_status"],
        "publication_status": "",
        "publication_payload": {},
        "publication_message": "",
    })


def run_pre_publish_guard(state):
    return pre_publish_guard.invoke({
        "linkedin_content": state["linkedin_content"],
        "approval_status": state["approval_status"],
        "publication_status": state["publication_status"],
        "publication_payload": state["publication_payload"],
        "guard_status": "",
        "guard_message": "",
    })


graph = StateGraph(SocialPilotState)

graph.add_node("research", run_research)
graph.add_node("trend_detection", run_trend_detection)
graph.add_node("verification", run_verification)
graph.add_node("content_generation", run_content_generation)
graph.add_node("linkedin_adapter", run_linkedin_adapter)
graph.add_node("qa", run_qa)
graph.add_node("revision", run_revision)
graph.add_node("approval_gate", run_approval_gate)
graph.add_node("human_approval", run_human_approval)
graph.add_node("publishing", run_publishing)
graph.add_node("pre_publish_guard", run_pre_publish_guard)

graph.add_edge(START, "research")
graph.add_edge("research", "trend_detection")
graph.add_edge("trend_detection", "verification")
graph.add_edge("verification", "content_generation")
graph.add_edge("content_generation", "linkedin_adapter")
graph.add_edge("linkedin_adapter", "qa")

graph.add_conditional_edges(
    "qa",
    route_after_qa,
    {
        "revision": "revision",
        "approval_gate": "approval_gate",
    },
)

graph.add_edge("revision", "qa")
graph.add_edge("approval_gate", END)

graph.add_conditional_edges(
    "human_approval",
    route_after_approval,
    {
        "publishing": "publishing",
        END: END,
    },
)

graph.add_edge("publishing", "pre_publish_guard")
graph.add_edge("pre_publish_guard", END)


socialpilot_workflow = graph.compile()
