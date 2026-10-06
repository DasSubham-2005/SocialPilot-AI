from app.agents.content_agent import content_agent


result = content_agent.invoke({
    "topic": "AI Agents in modern software development",
    "content_plan": ""
})


print("\n===== SOCIALPILOT AI =====\n")
print(result["content_plan"])