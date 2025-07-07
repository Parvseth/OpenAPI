import os
import subprocess
from logger import logger

def create_directories():
    for d in ["models", "schemas", "routes", "tests", "templates", "logs"]:
        os.makedirs(d, exist_ok=True)
        logger.info(f"Ensured {d}/ exists")

def run_generators():
    for s in [
        "generate_enums.py", "generate_sqlalchemy.py", "generate_pydantic.py",
        "generate_routes.py", "create_tables.py", "generate_tests.py", "generate_main.py"
    ]:
        result = subprocess.run(["python", s])
        if result.returncode != 0:
            logger.error(f"{s} failed")
            exit(1)
    logger.info("✅ Pipeline generation complete.")

if __name__ == "__main__":
    create_directories()
    run_generators()
