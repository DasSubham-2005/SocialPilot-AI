from app.workflow import SocialPilotState


print("\n===== SOCIALPILOT AI — WORKFLOW STATE TEST =====\n")


required_fields = [
    "topic",
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
    "human_decision",
    "approval_status",
    "approval_message",
    "publication_status",
    "publication_payload",
    "publication_message",
    "guard_status",
    "guard_message",
    "revised_content",
]


annotations = SocialPilotState.__annotations__

missing_fields = [
    field
    for field in required_fields
    if field not in annotations
]


if missing_fields:
    print("State validation: FAILED")
    print("Missing fields:")
    for field in missing_fields:
        print("-", field)
else:
    print("State validation: PASSED")
    print(f"Total state fields: {len(annotations)}")
    print("All workflow state fields are defined correctly.")