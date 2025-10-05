# agents/dev_agent.py

from core.agent_base import BaseAgent

class DeveloperAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="DeveloperAgent",
                         role="Software Developer")

    def run(self, task: str):
        self.log(f"Developing for subtask: {task}")
        prompt = f"You are a senior developer. Implement the following task step clearly:\n{task}\nReturn only clean, working code or direct output."
        result = self.think(prompt)
        self.log("Development complete.")
        return result
