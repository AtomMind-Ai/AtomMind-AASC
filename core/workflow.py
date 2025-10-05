import asyncio
from core.logger import get_logger
from core.agent_manager import AgentManager
from core.approval import request_approval, reviewer_approval_check
from core.stores import append_subtask_result, get_summary_for_agents, init_project_context

logger = get_logger()


class AsyncWorkflowManager:
    """Sequential, context-aware workflow with dynamic discussion between Developer and Reviewer."""

    def __init__(self, fresh_start=False):
        self.manager = AgentManager()
        self.manager.load_all_agents()
        self.fresh_start = fresh_start

    async def run_subtask(self, project_name, subtask_idx, subtask_text):
        developer = self.manager.create_agent("DeveloperAgent")
        reviewer = self.manager.create_agent("ReviewAgent")

        if not developer or not reviewer:
            logger.error(f"[Subtask {subtask_idx}] Agent not found.")
            append_subtask_result(project_name, subtask_text, "", "", "error", discussion="Agent missing")
            return {"subtask": subtask_text, "status": "error"}

        # Gather briefing / reminders from previous subtasks
        briefing = get_summary_for_agents(project_name, upto_subtask_idx=subtask_idx)
        briefing_prompt = f"📋 Project briefing before subtask {subtask_idx}:\n{briefing}\n\nSubtask: {subtask_text}"

        try:
            # Developer works on subtask
            developer_input = f"{briefing_prompt}\n\nDevelop this subtask clearly and efficiently."
            developer_output = await asyncio.to_thread(developer.run, developer_input)
            append_subtask_result(project_name, subtask_text, developer_output, "", "in_progress", discussion="")

            # Developer approval
            if not request_approval("Developer", subtask_text):
                append_subtask_result(project_name, subtask_text, developer_output, "", "rejected", discussion="Developer output rejected")
                return {"subtask": subtask_text, "result": developer_output, "status": "rejected"}

            # Reviewer reviews developer output
            review_input = f"{briefing_prompt}\n\nDeveloper output:\n{developer_output}\n\nReview this output carefully."
            review_output = await asyncio.to_thread(reviewer.run, review_input)

            # Reviewer-based approval logic
            status = "approved" if reviewer_approval_check(review_output) else "Need Human Review"
            print(f"[STATUS] {status.upper()} {'✅' if status=='approved' else '❌'}")

            # Developer responds to reviewer feedback if rejected
            developer_response = ""
            if status == "rejected":
                developer_response_input = f"Reviewer said:\n{review_output}\nPlease respond and improve the subtask output."
                developer_response = await asyncio.to_thread(developer.run, developer_response_input)
                # Optionally, you could re-run reviewer check for developer's response here

            # Compose discussion log
            discussion_notes = "\n\n".join([
                f"Developer initial output:\n{developer_output}",
                f"Reviewer feedback:\n{review_output}",
                f"Developer response:\n{developer_response}" if developer_response else ""
            ]).strip()

            # Save final context
            append_subtask_result(
                project_name,
                subtask_text,
                developer_output,
                review_output,
                status,
                discussion_notes
            )

            return {
                "subtask": subtask_text,
                "result": developer_output,
                "review": review_output,
                "developer_response": developer_response,
                "status": status,
                "discussion": discussion_notes
            }

        except Exception as e:
            logger.exception(f"[Subtask {subtask_idx}] Error: {e}")
            append_subtask_result(project_name, subtask_text, "", "", "error", discussion=str(e))
            return {"subtask": subtask_text, "error": str(e), "status": "error"}

    async def run_project(self, project_name, subtasks):
        """Run all subtasks sequentially for proper reminders and discussion context."""
        logger.info(f"🚀 Running project sequentially: {project_name}")

        if self.fresh_start:
            init_project_context(project_name, fresh_start=True)

        results = []
        for idx, subtask in enumerate(subtasks, 1):
            result = await self.run_subtask(project_name, idx, subtask)
            results.append(result)

        logger.info("✅ All subtasks processed in order.")
        return results

    def start_project(self, project_name, subtasks):
        return asyncio.run(self.run_project(project_name, subtasks))

