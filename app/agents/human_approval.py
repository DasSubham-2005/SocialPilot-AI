from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class ApprovalState(TypedDict):
    linkedin_content: str
    qa_status: str
    qa_report: str
    human_decision: str
    approval_status: str
    approval_message: str


def human_approval(state: ApprovalState):
    qa_status = state["qa_status"]
    human_decision = state.get("human_decision", "").upper()

    if qa_status != "APPROVED":
        return {
            "approval_status": "BLOCKED",
            "approval_message": (
                "Human approval is blocked because the QA Agent "
                "marked the content as NEEDS_REVISION."
            ),
        }

    if human_decision == "APPROVE":
        return {
            "approval_status": "APPROVED",
            "approval_message": (
                "Content was approved by the human reviewer "
                "and can proceed to publishing."
            ),
        }

    if human_decision == "REJECT":
        return {
            "approval_status": "REJECTED",
            "approval_message": (
                "Content was rejected by the human reviewer "
                "and must be revised before publishing."
            ),
        }

    return {
        "approval_status": "PENDING",
        "approval_message": (
            "Content passed QA and is waiting for human approval."
        ),
    }


graph = StateGraph(ApprovalState)

graph.add_node("human_approval", human_approval)

graph.add_edge(START, "human_approval")
graph.add_edge("human_approval", END)

human_approval_agent = graph.compile()