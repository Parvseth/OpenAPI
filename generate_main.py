import os
import yaml
from jinja2 import Environment, FileSystemLoader
from utils import to_snake_case
from logger import logger

# === Load OpenAPI Spec ===
with open("openapi3.yaml", "r") as f:
    spec = yaml.safe_load(f)
    
schemas = spec.get("components", {}).get("schemas", {})
model_names = list(schemas.keys())

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("main_template.j2")

# === Prepare context for main.py ===
models = [
    {
        "name": name,
        "snake": to_snake_case(name),
        "plural": to_snake_case(name) + "s",
    }
    for name in model_names
]

output = template.render(models=models)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(output)

logger.info("✅ main.py generated successfully.")
