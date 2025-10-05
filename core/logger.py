from loguru import logger
import os

log_dir = "data/logs"
os.makedirs(log_dir, exist_ok=True)
logger.add(f"{log_dir}/system.log", rotation="5 MB")

def get_logger():
    return logger
