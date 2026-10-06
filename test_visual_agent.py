from app.agents.research_agent import research_agent
from app.agents.verification_agent import verification_agent
from app.agents.content_generation_agent import content_generation_agent
from app.agents.linkedin_adapter import linkedin_adapter
from app.agents.qa_agent import qa_agent
from app.agents.human_approval import human_approval_agent
from app.agents.visual_agent import visual_agent


topic = "AI Agents in modern software development"


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


qa_result = qa_agent.invoke({
    "topic": topic,
    "verified_facts": verification_result["verified_facts"],
    "sources": research_result["sources"],
    "linkedin_content": linkedin_result["linkedin_content"],
    "qa_report": "",
    "qa_status": "",
})


if qa_result["qa_status"] != "APPROVED":
    print("\n===== SOCIALPILOT AI — VISUAL AGENT =====\n")
    print("Visual generation blocked.")
    print("QA Status:", qa_result["qa_status"])
    print("\nReason:")
    print(qa_result["qa_report"])
    raise SystemExit


approval_result = human_approval_agent.invoke({
    "linkedin_content": linkedin_result["linkedin_content"],
    "qa_status": qa_result["qa_status"],
    "qa_report": qa_result["qa_report"],
    "human_decision": "APPROVE",
    "approval_status": "",
    "approval_message": "",
})


if approval_result["approval_status"] != "APPROVED":
    print("\nVisual generation blocked by human approval.")
    raise SystemExit


visual_result = visual_agent.invoke({
    "topic": topic,
    "linkedin_content": linkedin_result["linkedin_content"],
    "verified_facts": verification_result["verified_facts"],
    "visual_brief": "",
})


print("\n===== SOCIALPILOT AI — VISUAL AGENT =====\n")

print("Visual Brief:")
print(visual_result["visual_brief"])