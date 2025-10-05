from abc import ABC, abstractmethod
from core.logger import get_logger
from core.llm_client import call_llm

logger = get_logger()

class BaseAgent(ABC):
    def __init__(self, name, role, memory=None):
        self.name = name
        self.role = role
        self.memory = memory

    @abstractmethod
    def run(self, task: str):
        pass

    def log(self, msg: str):
        logger.info(f"[{self.name}] {msg}")

    def think(self, task: str) -> str:
        """Reason or generate plan using LLM."""
        prompt = f"{self.role} Agent Task:\n{task}\n\nRespond concisely."
        return call_llm(prompt)
