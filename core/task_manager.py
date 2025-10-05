# core/task_manager.py

import os
from loguru import logger
from agents.planner_agent import PlannerAgent
from core.memory import remember
from core.approval import request_approval
from core.workflow import AsyncWorkflowManager
from core.stores import PROJECT_DATA_DIR, init_project_context

class TaskManager:
    """Manages project planning, execution, and reporting with full context tracking."""

    def __init__(self):
        self.planner = PlannerAgent()
        self.async_workflow = AsyncWorkflowManager()

    def run_project(self, project_name: str, fresh_start: bool = False):
        logger.info(f"🚀 Planning project: {project_name}")

        # Initialize fresh project context if requested
        if fresh_start:
            init_project_context(project_name, fresh_start=True)

        # 1️⃣ Planner generates overall plan
        plan_text = self.planner.run(project_name)
        remember("planner", "latest_plan", plan_text)
        logger.info(f"🧠 Plan created:\n{plan_text}")

        # 2️⃣ Approval check for plan
        if not request_approval("Planner", plan_text):
            logger.warning("❌ Plan not approved. Aborting workflow.")
            return {"status": "aborted", "reason": "plan rejected"}

        # 3️⃣ Split plan into subtasks
        subtasks = [s.strip() for s in plan_text.split("\n") if s.strip()]

        # 4️⃣ Run workflow with project_name to track context
        results = self.async_workflow.start_project(project_name, subtasks)

        # 5️⃣ Summarize results
        summary = {"approved": 0, "rejected": 0, "error": 0}
        for r in results:
            status = r.get("status")
            if status in summary:
                summary[status] += 1
        logger.info(f"📊 Project Summary: {summary}")

        # 6️⃣ Final report path (context JSON)
        report_path = os.path.join(PROJECT_DATA_DIR, f"{project_name.replace(' ', '_').lower()}_context.json")
        logger.info(f"📝 Final project report (context) saved: {report_path}")

        return {"results": results, "summary": summary, "report": report_path}
