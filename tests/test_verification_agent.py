from app.agents.research_agent import research_agent
from app.agents.verification_agent import verification_agent


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


print("\n===== SOCIALPILOT AI — VERIFICATION AGENT =====\n")

print(f"Sources analyzed: {verification_result['source_count']}")

print("\nVerification Report:")
print(verification_result["verified_facts"])