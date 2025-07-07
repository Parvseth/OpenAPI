# import logging
# import os

# os.makedirs("logs", exist_ok=True)
# log_file_path = os.path.join("logs", "generation.log")

# logger = logging.getLogger("generator")
# logger.setLevel(logging.INFO)

# if logger.hasHandlers():
#     logger.handlers.clear()

# file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
# formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.propagate = False

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
