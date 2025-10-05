import os
from core.memory import list_memory, recall
from core.logger import get_logger

logger = get_logger()

class ReporterAgent:
    """Generate a full project report in Markdown style."""

    def __init__(self):
        self.name = "ReporterAgent"

    def run(self, goal: str):
        report_lines = [f"# Project Report: {goal}\n"]

        # 1️⃣ Show project structure
        report_lines.append("## Project Structure\n```\n")
        for root, dirs, files in os.walk("agents"):
            for d in dirs:
                report_lines.append(os.path.join(root, d))
            for f in files:
                report_lines.append(os.path.join(root, f))
        for root, dirs, files in os.walk("core"):
            for d in dirs:
                report_lines.append(os.path.join(root, d))
            for f in files:
                report_lines.append(os.path.join(root, f))
        for root, dirs, files in os.walk("config"):
            for f in files:
                report_lines.append(os.path.join(root, f))
        report_lines.append("```\n")

        # 2️⃣ Show developer outputs
        report_lines.append("## DeveloperAgent Outputs\n")
        dev_entries = list_memory("developer")
        if not dev_entries:
            report_lines.append("No developer outputs found.\n")
        else:
            for entry in dev_entries:
                key = entry.split(" — ")[1]
                code = recall("developer", key)
                report_lines.append(f"### Subtask: {key}\n```python\n{code}\n```\n")

        # 3️⃣ Show ReviewAgent feedback
        report_lines.append("## ReviewAgent Feedback\n")
        review_entries = list_memory("reviewer")
        if not review_entries:
            report_lines.append("No review outputs found.\n")
        else:
            for entry in review_entries:
                key = entry.split(" — ")[1]
                feedback = recall("reviewer", key)
                report_lines.append(f"### Review: {key}\n   \n{feedback}\n   \n")

        # 4️⃣ Status summary
        report_lines.append("## Summary\n")
        report_lines.append(f"- Total subtasks: {len(dev_entries)}\n")
        report_lines.append(f"- Total reviews: {len(review_entries)}\n")
        report_lines.append("- Human attention needed if any review shows rejection.\n")

        report = "\n".join(report_lines)
        return report

    def save_report(self, goal: str, filename="project_report.md"):
        report = self.run(goal)
        os.makedirs("reports", exist_ok=True)
        path = os.path.join("reports", filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Project report saved to {path}")
        return path

