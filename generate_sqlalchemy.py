import os
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from schemas_to_model import extract_models  # returns Model -> List[Field] with .sqla_type info
from logger import logger

# === Load OpenAPI spec ===
try:
    with open("openapi3.yaml", "r") as f:
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
    logger.info(f"✅ Extracted {len(models)} models from spec.")
except Exception as e:
    logger.error(f"❌ Failed to extract models: {e}")
    exit(1)

# === Setup Jinja2 environment ===
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("sqlalchemy_model.j2")
except TemplateNotFound:
    logger.error("❌ sqlalchemy_model.j2 not found in 'templates/' folder.")
    exit(1)

# === Ensure models directory exists ===
os.makedirs("models", exist_ok=True)

# === Render and write each model ===
for model in models:
    try:
        rendered_code = template.render(model=model)
        output_path = os.path.join("models", f"{model.name.lower()}.py")

        with open(output_path, "w") as f:
            f.write(rendered_code)

        logger.info(f"✅ Generated SQLAlchemy model: {model.name} → {output_path}")
    except Exception as e:
        logger.error(f"❌ Failed to generate SQLAlchemy model for {model.name}: {e}")
