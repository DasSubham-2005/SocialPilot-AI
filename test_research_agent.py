from app.agents.research_agent import research_agent


result = research_agent.invoke({
    "topic": "AI Agents in modern software development",
    "search_query": "",
    "sources": [],
    "research_summary": "",
})


print("\n===== SOCIALPILOT AI — RESEARCH AGENT =====\n")

print("Search Query:")
print(result["search_query"])

print("\nResearch Summary:")
print(result["research_summary"])

print("\nSources:")
for index, source in enumerate(result["sources"], start=1):
    print(f"\n{index}. {source['title']}")
    print(source["url"])