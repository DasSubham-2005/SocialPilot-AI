from app.agents.human_approval import human_approval_agent


approved_content = """AI agents are changing how software development workflows are managed.

AI agents can assist with coding, testing, documentation, and security-related workflows.

Human oversight remains important when deploying autonomous AI systems.

What changes are you seeing in software development?

#SoftwareEngineering #AIAgents #DevOps"""


print("\n===== SOCIALPILOT AI — HUMAN APPROVAL TEST =====\n")

print("QA Status:")
print("APPROVED")

print("\nHuman Decision:")
print("APPROVE")

result = human_approval_agent.invoke({
    "linkedin_content": approved_content,
    "qa_status": "APPROVED",
    "qa_report": "All QA checks passed.",
    "human_decision": "APPROVE",
    "approval_status": "",
    "approval_message": "",
})

print("\n===== APPROVAL RESULT =====\n")

print("Approval Status:")
print(result["approval_status"])

print("\nApproval Message:")
print(result["approval_message"])

print("\n===== FINAL CONTENT =====\n")
print(approved_content)