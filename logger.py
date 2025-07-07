# logger.py
import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

log_file_path = os.path.join("logs", "generation.log")

logger = logging.getLogger("generator")
logger.setLevel(logging.INFO)

# Remove any existing handlers (to prevent duplicates if re-imported)
if logger.hasHandlers():
    logger.handlers.clear()

# Create a file handler that logs to generation.log with UTF-8 encoding
file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Optional: suppress propagation to avoid duplicate logs
logger.propagate = False
