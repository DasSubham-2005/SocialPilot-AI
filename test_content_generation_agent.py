from app.agents.research_agent import research_agent
from app.agents.verification_agent import verification_agent
from app.agents.content_generation_agent import content_generation_agent


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


print("\n===== SOCIALPILOT AI — CONTENT GENERATION =====\n")

print("CONTENT STRATEGY")
print("----------------")
print(content_result["content_strategy"])

print("\n\nFINAL LINKEDIN DRAFT")
print("--------------------")
print(content_result["draft_content"])