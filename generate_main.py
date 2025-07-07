import os
from jinja2 import Environment, FileSystemLoader
from schemas_to_model import extract_models, extract_routes
import yaml
from logger import logger

with open("openapi3.yaml") as f:
    spec = yaml.safe_load(f)

schemas = spec.get("components", {}).get("schemas", {})
paths = spec.get("paths", {})

models = extract_models(schemas)
routes = extract_routes(paths)

# Determine which models have CRUD operations
models_with_crud = []
model_plural_map = {}

for model in models:
    plural_name = model.name.lower() + "s"
    model_plural_map[model.name] = plural_name

models_with_crud_set = set()
for route in routes:
    if route.request_schema:
        models_with_crud_set.add(route.request_schema)
    elif route.response_schema:
        models_with_crud_set.add(route.response_schema)

# Filter models to include only those with CRUD paths
models_with_crud = [model for model in models if model.name in models_with_crud_set]

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("main_template.j2")

output = template.render(models=[
    {
        "name": model.name,
        "snake": model.name.lower(),
        "plural": model_plural_map[model.name]
    }
    for model in models_with_crud
])

with open("main.py", "w", encoding="utf-8") as f:
    f.write(output)

logger.info("✅ Generated main.py with correct imports based on available routes.")
