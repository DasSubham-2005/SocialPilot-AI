from app.agents.research_agent import research_agent
from app.agents.verification_agent import verification_agent
from app.agents.content_generation_agent import content_generation_agent
from app.agents.linkedin_adapter import linkedin_adapter
from app.agents.qa_agent import qa_agent
from app.agents.revision_agent import revision_agent


topic = "AI Agents in modern software development"

MAX_REVISION_LOOPS = 3


research_result = research_agent.invoke({
    "topic": topic,
    "search_query": "",
    "sources": [],
    "research_summary": "",
})


verification_result = verification_agent.invoke({
    "topic": topic,
    "sources": research_result["sources"],
    "research_summary": research_result["research_summary"],
    "verified_facts": "",
    "source_count": 0,
})


content_result = content_generation_agent.invoke({
    "topic": topic,
    "research_summary": research_result["research_summary"],
    "verified_facts": verification_result["verified_facts"],
    "sources": research_result["sources"],
    "content_strategy": "",
    "draft_content": "",
})


linkedin_result = linkedin_adapter.invoke({
    "topic": topic,
    "draft_content": content_result["draft_content"],
    "linkedin_content": "",
})


current_content = linkedin_result["linkedin_content"]


print("\n===== SOCIALPILOT AI — QA / REVISION LOOP =====\n")

print("Initial LinkedIn Post")
print("--------------------")
print(current_content)


for loop_number in range(MAX_REVISION_LOOPS + 1):

    qa_result = qa_agent.invoke({
        "topic": topic,
        "verified_facts": verification_result["verified_facts"],
        "sources": research_result["sources"],
        "linkedin_content": current_content,
        "qa_report": "",
        "qa_status": "",
    })

    print(f"\n===== QA CHECK {loop_number + 1} =====\n")

    print("QA Status:")
    print(qa_result["qa_status"])

    print("\nQA Report:")
    print(qa_result["qa_report"])


    if qa_result["qa_status"] == "APPROVED":

        print("\n===== FINAL APPROVED CONTENT =====\n")
        print(current_content)

        print("\nWorkflow completed successfully.")
        break


    if loop_number >= MAX_REVISION_LOOPS:
        print("\nMaximum revision limit reached.")
        print("Content still requires revision.")
        break


    print(
        f"\nRevision required. "
        f"Starting Revision Agent — Loop {loop_number + 1}..."
    )


    revision_result = revision_agent.invoke({
        "topic": topic,
        "linkedin_content": current_content,
        "verified_facts": verification_result["verified_facts"],
        "sources": research_result["sources"],
        "qa_report": qa_result["qa_report"],
        "revised_content": "",
    })


    current_content = revision_result["revised_content"]


    print("\n===== REVISED CONTENT =====\n")
    print(current_content)