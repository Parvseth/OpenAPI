from schemas_to_model import extract_models
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from logger import logger  # <-- Add this line

try:
    with open("openapi3.yaml") as f:
        spec = yaml.safe_load(f)
    logger.info("📄 Loaded openapi3.yaml successfully.")
except FileNotFoundError:
    logger.error("❌ openapi3.yaml not found.")
    exit(1)

schemas = spec.get("components", {}).get("schemas", {})
if not schemas:
    logger.warning("⚠️ No schemas found in OpenAPI spec.")
    exit(0)

try:
    models = extract_models(schemas)
    logger.info("✅ Extracted models from schemas.")
except Exception as e:
    logger.error(f"❌ Error extracting models: {e}")
    exit(1)

# Get enums from fields
enum_classes = []
seen = set()
for model in models:
    for field in model.fields:
        if field.enum_values and field.enum_class not in seen:
            enum_classes.append({
                "name": field.enum_class,
                "values": field.enum_values
            })
            seen.add(field.enum_class)

if not enum_classes:
    logger.info("ℹ️ No enum definitions found.")
    exit(0)

# Render template
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("enum_template.j2")
except TemplateNotFound:
    logger.error("❌ enum_template.j2 not found in templates/")
    exit(1)

try:
    output = template.render(enums=enum_classes)
except Exception as e:
    logger.error(f"❌ Failed to render enum template: {e}")
    exit(1)

# Write to enums.py
try:
    with open("schemas/enums.py", "w") as f:
        f.write(output)
    logger.info("✅ Generated enums → schemas/enums.py")
except Exception as e:
    logger.error(f"❌ Failed to write enums.py: {e}")
    exit(1)
