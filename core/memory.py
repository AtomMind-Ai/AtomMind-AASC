import os
import json
from datetime import datetime

MEMORY_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "memory")
GENERAL_MEMORY_FILE = os.path.join(MEMORY_DIR, "general_memory.json")

def _ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def _memory_path(agent_name: str) -> str:
    return os.path.join(MEMORY_DIR, f"{agent_name.lower()}_memory.json")

def load_memory(agent_name: str = None) -> dict:
    """Load memory for a specific agent or general memory if agent_name is None."""
    _ensure_dir()
    path = _memory_path(agent_name) if agent_name else GENERAL_MEMORY_FILE
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return {
            "agent": agent_name or "general",
            "created": datetime.now().isoformat(),
            "entries": []
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory_data: dict, agent_name: str = None):
    """Save memory to file for specific agent or general memory if agent_name is None."""
    _ensure_dir()
    path = _memory_path(agent_name) if agent_name else GENERAL_MEMORY_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=2, ensure_ascii=False)

def remember(agent_name: str, key: str, value: str, general: bool = False):
    """Save a memory entry. If general=True, store in shared memory for all agents."""
    mem = load_memory(None if general else agent_name)
    mem["entries"].append({
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "key": key,
        "value": value
    })
    save_memory(mem, None if general else agent_name)

def recall(agent_name: str, key: str, general: bool = False):
    """Retrieve latest value for key from agent memory or general memory if general=True."""
    mem = load_memory(None if general else agent_name)
    for entry in reversed(mem.get("entries", [])):
        if entry["key"] == key:
            return entry["value"]
    return None

def list_memory(agent_name: str = None):
    """List all memory entries for specific agent or general memory if agent_name=None."""
    mem = load_memory(agent_name)
    return [f"{e['timestamp']} — {e.get('agent','general')} — {e['key']}" for e in mem.get("entries", [])]

def clear_memory(agent_name: str = None):
    """Clear memory for agent or general memory."""
    mem = {"agent": agent_name or "general", "created": datetime.now().isoformat(), "entries": []}
    save_memory(mem, agent_name)

