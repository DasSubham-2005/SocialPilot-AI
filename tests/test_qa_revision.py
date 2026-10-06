from app.agents.qa_agent import qa_agent
from app.agents.revision_agent import revision_agent


topic = "AI Agents in modern software development"

verified_facts = """
AI agents are increasingly being used to plan tasks, make decisions,
orchestrate tools, and support software development workflows.

Agentic systems can assist with activities such as coding, testing,
documentation, and security-related workflows.

Human oversight, access controls, audit trails, and review processes
are important considerations when deploying autonomous AI systems.

The role of software engineers is evolving as AI-assisted and
agent-based development workflows become more capable.
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

linkedin_content = """The future of software development is changing rapidly because AI agents can now manage complex workflows.

AI agents are increasingly helping with coding, testing, documentation, and security checks. This can reduce manual context switching and support hybrid human-AI collaboration.

AI agents are already replacing most software engineers across the industry.

Autonomy without control creates risks, so organizations need appropriate access controls, audit trails, and human review.

What changes are you seeing in software development?

SoftwareEngineering #AIAgents #DevOps"""


print("\n===== SOCIALPILOT AI — CACHED QA / REVISION TEST =====\n")

print("Initial LinkedIn Post")
print("--------------------")
print(linkedin_content)

print("\n===== QA CHECK 1 =====\n")

qa_result = qa_agent.invoke({
    "topic": topic,
    "verified_facts": verified_facts,
    "sources": sources,
    "linkedin_content": linkedin_content,
    "qa_report": "",
    "qa_status": "",
})

print("QA Status:")
print(qa_result["qa_status"])

print("\nQA Report:")
print(qa_result["qa_report"])


if qa_result["qa_status"] == "NEEDS_REVISION":

    print("\n===== REVISION AGENT =====\n")

    revision_result = revision_agent.invoke({
        "topic": topic,
        "linkedin_content": linkedin_content,
        "verified_facts": verified_facts,
        "sources": sources,
        "qa_report": qa_result["qa_report"],
        "revised_content": "",
    })

    revised_content = revision_result["revised_content"]

    print("Revised LinkedIn Post")
    print("--------------------")
    print(revised_content)

    print("\n===== QA CHECK 2 =====\n")

    final_qa_result = qa_agent.invoke({
        "topic": topic,
        "verified_facts": verified_facts,
        "sources": sources,
        "linkedin_content": revised_content,
        "qa_report": "",
        "qa_status": "",
    })

    print("Final QA Status:")
    print(final_qa_result["qa_status"])

    print("\nFinal QA Report:")
    print(final_qa_result["qa_report"])

    if final_qa_result["qa_status"] == "APPROVED":
        print("\n===== FINAL APPROVED CONTENT =====\n")
        print(revised_content)
        print("\nWorkflow completed successfully.")

    else:
        print("\nContent still requires revision.")

else:
    print("\n===== CONTENT ALREADY APPROVED =====\n")
    print(linkedin_content)
    print("\nNo revision required.")