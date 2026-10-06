
from app.workflow import SocialPilotState
from app.agents.content_generation_agent import ContentGenerationState


def test_workflow_state():
    required_fields = {
        "topic",
        "brand_context",
        "platform",
        "search_query",
        "sources",
        "research_summary",
        "verified_facts",
        "source_count",
        "content_strategy",
        "draft_content",
        "linkedin_content",
        "qa_report",
        "qa_status",
        "revision_count",
        "human_decision",
        "approval_status",
        "approval_message",
        "publication_status",
        "publication_payload",
        "publication_message",
        "guard_status",
        "guard_message",
        "revised_content",
    }

    actual_fields = set(
        SocialPilotState.__annotations__.keys()
    )

    missing_fields = required_fields - actual_fields

    if missing_fields:
        print("WORKFLOW STATE TEST: FAIL")
        print("Missing fields:", sorted(missing_fields))
        return False

    print("WORKFLOW STATE TEST: PASS")
    return True


def test_content_generation_state():
    required_fields = {
        "topic",
        "brand_context",
        "platform",
        "research_summary",
        "verified_facts",
        "sources",
        "content_strategy",
        "draft_content",
    }

    actual_fields = set(
        ContentGenerationState.__annotations__.keys()
    )

    missing_fields = required_fields - actual_fields

    if missing_fields:
        print("CONTENT GENERATION STATE TEST: FAIL")
        print("Missing fields:", sorted(missing_fields))
        return False

    print("CONTENT GENERATION STATE TEST: PASS")
    return True


if __name__ == "__main__":

    print("===== SOCIALPILOT AI — STATE FLOW TEST =====")

    workflow_ok = test_workflow_state()
    content_ok = test_content_generation_state()

    print()

    if workflow_ok and content_ok:
        print("STATE FLOW TEST: PASSED")
    else:
        print("STATE FLOW TEST: FAILED")

    print("===== TEST COMPLETE =====")
