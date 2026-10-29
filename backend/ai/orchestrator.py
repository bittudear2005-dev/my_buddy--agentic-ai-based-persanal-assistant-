from ai.llm import llm
from ai.agents.task_agent import TaskAgent
from ai.agents.analytics_agent import AnalyticsAgent
from ai.agents.query_agent import QueryAgent

class Orchestrator:
    """
    Brain of the entire AI system:
    - Classifies intent
    - Routes to correct agent
    - Falls back to LLM
    """

    def __init__(self):
        self.task_agent = TaskAgent()
        self.analytics_agent = AnalyticsAgent()
        self.query_agent = QueryAgent()

    def classify(self, text: str) -> str:
        text = text.lower()

        if any(w in text for w in ["add", "create", "new task"]):
            return "task"

        if any(w in text for w in ["progress", "stats", "status", "how am i"]):
            return "analytics"

        if any(w in text for w in ["what", "show", "find", "search"]):
            return "query"

        return "general"

    def handle(self, text: str, goals: list):
        intent = self.classify(text)

        if intent == "task":
            return self.task_agent.run(text, goals)

        if intent == "analytics":
            return self.analytics_agent.run(goals)

        if intent == "query":
            return self.query_agent.run(text)

        # LLM fallback for normal chat
        reply = llm.generate(
            f"You are a productivity assistant. "
            f"Respond concisely.\nUser: {text}\nAssistant:"
        )

        return {
            "message": reply,
            "action": "llm_fallback"
        }

orchestrator = Orchestrator()
