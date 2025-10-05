# core/approval.py

import logging
import os
import yaml
import re

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "settings.yaml")

def _load_auto_approve() -> bool:
    """Load auto-approval mode from config. Defaults to True if config missing."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
            return config.get('approval', {}).get('mode', True)
    except FileNotFoundError:
        return True

AUTO_APPROVE = _load_auto_approve()


def request_approval(agent_name: str, task_desc: str) -> bool:
    """
    General approval request.
    Returns True if approved, False if rejected.
    """
    if AUTO_APPROVE:
        logging.info(f"[{agent_name}] Auto-approved task: {task_desc}")
        return True
    else:
        print(f"\n[{agent_name}] Task requires approval:\n{task_desc}")
        choice = input("Approve? (y/n): ").strip().lower()
        approved = choice == "y"
        logging.info(f"[{agent_name}] Manual approval: {approved}")
        return approved


def reviewer_approval_check(review_output: str) -> bool:
    """
    Analyze the reviewer's output to decide if the subtask passes or fails.
    Returns True if approved, False if rejected.
    """
    # Simple keywords that indicate failure
    failure_keywords = [
        r'\bfail\b',
        r'\berror\b',
        r'\berrors\b',
        r'\bissue\b',
        r'\bissues\b',
        r'\baction required\b',
        r'\bincorrect\b',
        r'\bcritical issue\b',
    ]
    
    review_lower = review_output.lower()
    
    for kw in failure_keywords:
        if re.search(kw, review_lower):
            logging.info(f"[Reviewer Approval] Detected failure keyword '{kw}' in review. Subtask rejected.")
            return False
    
    logging.info("[Reviewer Approval] No failure detected. Subtask approved.")
    return True
