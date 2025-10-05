import os
import json
from datetime import datetime

PROJECT_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "projects")
os.makedirs(PROJECT_DATA_DIR, exist_ok=True)


def _context_path(project_name: str) -> str:
    safe_name = project_name.replace(" ", "_").lower()
    return os.path.join(PROJECT_DATA_DIR, f"{safe_name}_context.json")


def load_context(project_name: str) -> dict:
    """Load project context, or create default if not exists."""
    path = _context_path(project_name)
    if not os.path.exists(path):
        return {"project": project_name, "created": datetime.now().isoformat(), "subtasks": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_context(project_name: str, context: dict):
    """Save project context to file."""
    path = _context_path(project_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)


def init_project_context(project_name: str, fresh_start: bool = False):
    """Initialize project context. If fresh_start=True, clear all previous subtasks."""
    if fresh_start:
        context = {"project": project_name, "created": datetime.now().isoformat(), "subtasks": []}
        save_context(project_name, context)


def append_subtask_result(project_name: str, subtask_text: str, developer_output: str,
                          review_output: str, status: str, discussion: str = ""):
    """Add a subtask result to the project context."""
    context = load_context(project_name)
    context["subtasks"].append({
        "timestamp": datetime.now().isoformat(),
        "subtask": subtask_text,
        "developer_output": developer_output,
        "review_output": review_output,
        "status": status,
        "discussion": discussion
    })
    save_context(project_name, context)


def get_summary_for_agents(project_name: str, upto_subtask_idx: int = None) -> str:
    """
    Generate a concise briefing for agents.

    If upto_subtask_idx is given, only include subtasks before that index
    (completed subtasks) to prevent showing unfinished work.
    """
    context = load_context(project_name)
    summary_lines = [f"Project: {project_name}\n"]
    subtasks = context.get("subtasks", [])

    if upto_subtask_idx is not None:
        subtasks = subtasks[:upto_subtask_idx - 1]  # only include completed before current

    for idx, st in enumerate(subtasks, 1):
        summary_lines.append(f"Subtask {idx}: {st['subtask']}")
        summary_lines.append(f"Status: {st['status']}")
        summary_lines.append(f"Developer Output (short): {st['developer_output'][:200]}...")
        summary_lines.append(f"Review Summary: {st['review_output'][:200]}...")
        if st.get("discussion"):
            summary_lines.append(f"Discussion Notes: {st['discussion'][:200]}...")
        summary_lines.append("-" * 50)

    return "\n".join(summary_lines)

