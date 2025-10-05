import importlib
import pkgutil
from typing import Any, Dict, Optional, Type

from core.logger import get_logger

logger = get_logger()


class AgentManager:
    """Load and manage available Agent classes."""

    def __init__(self) -> None:
        self.agents: Dict[str, Type[Any]] = {}

    def register_agent(self, name: str, agent_class: Type[Any]) -> None:
        """Register an agent class under a name."""
        self.agents[name] = agent_class
        logger.info(f'Registered agent: {name}')

    def load_all_agents(self) -> None:
        """Auto-import all modules in the `agents` package and register Agent classes.

        Any class whose name ends with "Agent" will be registered.
        """
        try:
            import agents  # local package with agent modules
        except ImportError:
            logger.exception("Failed to import 'agents' package.")
            return

        for _, module_name, _ in pkgutil.iter_modules(agents.__path__):
            try:
                module = importlib.import_module(f"agents.{module_name}")
            except Exception:
                logger.exception(f"Failed to import agents.{module_name}")
                continue

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr.__name__.endswith("Agent"):
                    self.register_agent(attr.__name__, attr)

    def create_agent(self, name: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        """Instantiate a registered agent by name. Returns None if not found."""
        agent_class = self.agents.get(name)
        if agent_class is None:
            logger.error(f"Agent {name} not found.")
            return None
        return agent_class(*args, **kwargs)
