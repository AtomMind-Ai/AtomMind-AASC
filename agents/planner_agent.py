from core.agent_base import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="PlannerAgent",
                         role="Project Planner")

    def run(self, task: str):
        self.log(f"Planning for task: {task}")
        prompt = f"You are a professional software project planner.\nGoal: {task}\n\nBreak it into numbered, logical subtasks."
        plan = self.think(prompt)
        self.log("Plan generated.")
        return plan

