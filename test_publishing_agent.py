from app.agents.publishing_agent import publishing_agent


linkedin_content = """AI agents are changing how software development workflows are managed.

AI agents can assist with coding, testing, documentation, and security-related workflows.

Human oversight remains important when deploying autonomous AI systems.

What changes are you seeing in software development?

#SoftwareEngineering #AIAgents #DevOps"""


print("\n===== SOCIALPILOT AI — PUBLISHING AGENT TEST =====\n")

result = publishing_agent.invoke({
    "linkedin_content": linkedin_content,
    "approval_status": "APPROVED",
    "publication_status": "",
    "publication_payload": {},
    "publication_message": "",
})

print("Publication Status:")
print(result["publication_status"])

print("\nPublication Message:")
print(result["publication_message"])

print("\nPublication Payload:")
print(result["publication_payload"])