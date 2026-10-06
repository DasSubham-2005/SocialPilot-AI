from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class PrePublishState(TypedDict):
    linkedin_content: str
    approval_status: str
    publication_status: str
    publication_payload: dict
    guard_status: str
    guard_message: str


def run_pre_publish_guard(state: PrePublishState):

    issues = []

    if state["approval_status"].upper() != "APPROVED":
        issues.append("Human approval is not APPROVED.")

    if state["publication_status"].upper() != "READY":
        issues.append("Publication status is not READY.")

    content = state["linkedin_content"].strip()

    if not content:
        issues.append("LinkedIn content is empty.")

    payload = state["publication_payload"]

    if not isinstance(payload, dict):
        issues.append("Publication payload is invalid.")
    else:
        if payload.get("platform") != "linkedin":
            issues.append("Publication platform is not LinkedIn.")

        if payload.get("content", "").strip() != content:
            issues.append("Publication payload content does not match approved content.")

        if payload.get("publish_mode") != "manual":
            issues.append("Unexpected publish mode.")

    if issues:
        return {
            "guard_status": "BLOCKED",
            "guard_message": (
                "Pre-publish guard blocked publication:\n"
                + "\n".join(f"- {issue}" for issue in issues)
            ),
        }

    return {
        "guard_status": "PASSED",
        "guard_message": (
            "All pre-publish checks passed. "
            "The approved LinkedIn content is safe to proceed "
            "to the publishing layer."
        ),
    }


graph = StateGraph(PrePublishState)

graph.add_node(
    "pre_publish_guard",
    run_pre_publish_guard
)

graph.add_edge(
    START,
    "pre_publish_guard"
)

graph.add_edge(
    "pre_publish_guard",
    END
)

pre_publish_guard = graph.compile()