import os
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from schemas_to_model import extract_models, extract_routes
from logger import logger  # ← Central logging

# Load OpenAPI spec
try:
    with open("openapi3.yaml", "r") as f:
        spec = yaml.safe_load(f)
    logger.info("📄 Loaded openapi3.yaml successfully.")
except FileNotFoundError:
    logger.error("❌ openapi3.yaml not found.")
    exit(1)

schemas = spec.get("components", {}).get("schemas", {})
paths = spec.get("paths", {})
if not schemas or not paths:
    logger.warning("⚠️ No schemas or paths found in the spec.")
    exit(0)

try:
    models = extract_models(schemas)
    routes = extract_routes(paths)
    logger.info(f"✅ Extracted {len(models)} models and {len(routes)} routes.")
except Exception as e:
    logger.error(f"❌ Error during model/route extraction: {e}")
    exit(1)

# Setup Jinja2 environment
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("route_template.j2")
except TemplateNotFound:
    logger.error("❌ route_template.j2 not found in templates/")
    exit(1)

# Ensure output dir exists
os.makedirs("routes", exist_ok=True)

# Group HTTP methods per model
model_routes = {}
for route in routes:
    if route.request_schema:
        model_routes.setdefault(route.request_schema, set()).add(route.method)
    elif route.response_schema:
        model_routes.setdefault(route.response_schema, set()).add(route.method)

# Generate route files
for model in models:
    methods = model_routes.get(model.name)
    if not methods:
        logger.info(f"ℹ️ Skipped {model.name}: no associated routes.")
        continue

    try:
        output = template.render(model=model, methods=sorted(methods))
        filename = f"routes/{model.name.lower()}.py"
        with open(filename, "w") as f:
            f.write(output)
        logger.info(f"✅ Generated route: {filename}")
    except Exception as e:
        logger.error(f"❌ Failed to generate route for {model.name}: {e}")
