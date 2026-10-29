class AnalyticsAgent:
    """
    Computes user productivity stats.
    """

    def run(self, goals: list):
        total = len(goals)
        completed = len([g for g in goals if g["completed"]])
        percent = int((completed / total) * 100) if total else 0

        return {
            "message": (
                f"📊 Progress: {completed}/{total} tasks "
                f"({percent}%) completed."
            ),
            "stats": {
                "total": total,
                "completed": completed,
                "completion_rate": percent
            },
            "action": "analytics_report"
        }
