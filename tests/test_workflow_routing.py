from app.workflow import route_after_qa, route_after_approval


print("\n===== SOCIALPILOT AI — WORKFLOW ROUTING TEST =====\n")


qa_revision_state = {
    "qa_status": "NEEDS_REVISION"
}

qa_approved_state = {
    "qa_status": "APPROVED"
}


approval_approved_state = {
    "approval_status": "APPROVED"
}

approval_rejected_state = {
    "approval_status": "REJECTED"
}


print("QA = NEEDS_REVISION")
print("Route:", route_after_qa(qa_revision_state))

print("\nQA = APPROVED")
print("Route:", route_after_qa(qa_approved_state))

print("\nHuman Approval = APPROVED")
print("Route:", route_after_approval(approval_approved_state))

print("\nHuman Approval = REJECTED")
print("Route:", route_after_approval(approval_rejected_state))