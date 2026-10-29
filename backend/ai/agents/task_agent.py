class TaskAgent:
    """
    Task creation & basic task operations.
    """

    def run(self, text: str, goals: list):
        clean = (
            text.lower()
                .replace("add", "")
                .replace("create", "")
                .replace("task", "")
                .replace("goal", "")
                .strip()
        )

        if not clean:
            clean = "New Task"

        new_goal = {
            "id": len(goals) + 1,
            "title": clean,
            "completed": False,
            "priority": "medium",
            "deadline": None,
            "streak": 0,
        }

        goals.append(new_goal)

        return {
            "message": f"📝 Added task: **{clean}**",
            "task": new_goal,
            "action": "task_created"
        }
