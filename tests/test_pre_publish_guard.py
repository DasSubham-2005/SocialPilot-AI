from app.agents.pre_publish_guard import pre_publish_guard


linkedin_content = """AI agents are changing how software development workflows are managed.

AI agents can assist with coding, testing, documentation, and security-related workflows.

Human oversight remains important when deploying autonomous AI systems.

What changes are you seeing in software development?

#SoftwareEngineering #AIAgents #DevOps"""


publication_payload = {
    "platform": "linkedin",
    "content": linkedin_content,
    "publish_mode": "manual",
}


result = pre_publish_guard.invoke({
    "linkedin_content": linkedin_content,
    "approval_status": "APPROVED",
    "publication_status": "READY",
    "publication_payload": publication_payload,
    "guard_status": "",
    "guard_message": "",
})


print("\n===== SOCIALPILOT AI — PRE-PUBLISH GUARD TEST =====\n")

print("Guard Status:")
print(result["guard_status"])

print("\nGuard Message:")
print(result["guard_message"])