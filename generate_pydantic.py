import os
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from schemas_to_model import extract_models
from logger import logger  # ← Logger import

# Load OpenAPI spec
try:
    with open("openapi3.yaml") as f:
        spec = yaml.safe_load(f)
    logger.info("📄 Loaded openapi3.yaml successfully.")
except FileNotFoundError:
    logger.error("❌ openapi3.yaml not found.")
    exit(1)

schemas = spec.get("components", {}).get("schemas", {})
if not schemas:
    logger.warning("⚠️ No schemas found in spec.")
    exit(0)

try:
    models = extract_models(schemas)
    logger.info(f"✅ Extracted {len(models)} models.")
except Exception as e:
    logger.error(f"❌ Error extracting models: {e}")
    exit(1)

# Setup Jinja2
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("pydantic_model.j2")
except TemplateNotFound:
    logger.error("❌ pydantic_model.j2 not found in templates/")
    exit(1)

# Output directory
os.makedirs("schemas", exist_ok=True)

# Generate schema files
for model in models:
    try:
        output = template.render(model=model)
        file_path = f"schemas/{model.name.lower()}.py"
        with open(file_path, "w") as f:
            f.write(output)
        logger.info(f"✅ Generated Pydantic schema: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to generate schema for {model.name}: {e}")
