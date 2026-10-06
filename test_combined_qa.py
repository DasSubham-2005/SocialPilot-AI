from app.agents.qa_agent import qa_agent
from app.validators.linkedin_validator import validate_linkedin_content


topic = "AI Agents in modern software development"

verified_facts = """
AI agents are increasingly being used to assist with software
development workflows including coding, testing, documentation,
security-related tasks, and tool orchestration.

Human oversight, access controls, audit trails, and review processes
are important considerations when deploying autonomous AI systems.
"""

sources = [
    {
        "title": "Cached source for QA testing",
        "url": "https://example.com/source",
        "content": (
            "AI agents can assist with software development workflows "
            "including coding, testing, documentation, and tool orchestration."
        ),
    }
]


linkedin_content = """AI agents are changing how software development workflows are managed.

AI agents can assist with coding, testing, documentation, and security-related workflows. They can also help coordinate multiple tools.

Human oversight remains important when deploying autonomous AI systems.

What changes are you seeing in software development?

SoftwareEngineering #AIAgents #DevOps"""


print("\n===== SOCIALPILOT AI — COMBINED QA TEST =====\n")

print("LinkedIn Content")
print("----------------")
print(linkedin_content)


print("\n===== QWEN QA =====\n")

qa_result = qa_agent.invoke({
    "topic": topic,
    "verified_facts": verified_facts,
    "sources": sources,
    "linkedin_content": linkedin_content,
    "qa_report": "",
    "qa_status": "",
})

print("Qwen QA Status:")
print(qa_result["qa_status"])

print("\nQwen QA Report:")
print(qa_result["qa_report"])


print("\n===== DETERMINISTIC VALIDATOR =====\n")

validator_result = validate_linkedin_content(
    linkedin_content
)

print("Validator Status:")
print(validator_result["status"])

print("\nValidator Issues:")

if validator_result["issues"]:
    for issue in validator_result["issues"]:
        print(f"- {issue}")
else:
    print("NONE")


print("\n===== COMBINED DECISION =====\n")

if (
    qa_result["qa_status"] == "APPROVED"
    and validator_result["status"] == "PASS"
):
    final_status = "APPROVED"
else:
    final_status = "NEEDS_REVISION"


print(f"Final Status: {final_status}")