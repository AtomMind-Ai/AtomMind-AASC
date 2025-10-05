# agent/review_agent.py

from core.agent_base import BaseAgent

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ReviewAgent",
                         role="Code Reviewer")

    def run(self, task: str):
        self.log("Reviewing generated output.")
        prompt = f"You are a reviewer. Review this output for correctness, structure, and clarity:\n{task}\nGive a brief summary and pass/fail."
        feedback = self.think(prompt)
        self.log("Review completed.")
        return feedback
