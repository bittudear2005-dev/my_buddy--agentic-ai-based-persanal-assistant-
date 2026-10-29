from ai.rag import search

class QueryAgent:
    """
    Uses RAG to answer questions using user’s stored tasks & data.
    """

    def run(self, text: str):
        results = search(text)
        docs = results.get("documents", [[]])[0]

        if not docs:
            return {
                "message": "I didn’t find anything related in your knowledge base.",
                "results": [],
                "action": "rag_no_results"
            }

        formatted = "\n".join([f"- {d}" for d in docs])

        return {
            "message": f"🔍 Here's what I found:\n{formatted}",
            "results": docs,
            "action": "rag_search"
        }
