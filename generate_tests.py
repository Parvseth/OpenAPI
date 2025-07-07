import os
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from schemas_to_model import extract_models
from logger import logger

# Optional: Simple pluralizer for fallback
def pluralize(word):
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    elif word.endswith(("s", "sh", "ch", "x", "z")):
        return word + "es"
    else:
        return word + "s"

# === Load OpenAPI Spec ===
try:
    with open("openapi3.yaml", "r") as f:
        spec = yaml.safe_load(f)
    logger.info("✅ Loaded openapi3.yaml successfully.")
except FileNotFoundError:
    logger.error("❌ openapi3.yaml not found.")
    exit(1)

schemas = spec.get("components", {}).get("schemas", {})
if not schemas:
    logger.warning("⚠️ No schemas found in OpenAPI spec.")
    exit(0)

# === Extract Models ===
try:
    models = extract_models(schemas)
    for model in models:
        model.plural = pluralize(model.name.lower())  # ✅ Add plural name
    logger.info(f"✅ Extracted {len(models)} models.")
except Exception as e:
    logger.error(f"❌ Error extracting models: {e}")
    exit(1)

# === Jinja2 Template Setup ===
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("test_template.j2")
except TemplateNotFound:
    logger.error("❌ Template 'test_template.j2' not found in templates/")
    exit(1)

# === Output Directory Setup ===
os.makedirs("tests", exist_ok=True)

# === Generate Test Files ===
for model in models:
    try:
        output = template.render(model=model)
        file_path = f"tests/test_{model.name.lower()}.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)
        logger.info(f"✅ Generated test file: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to generate test for {model.name}: {e}")
