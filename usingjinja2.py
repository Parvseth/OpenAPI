from jinja2 import Environment, FileSystemLoader
from schemas_to_model import extract_models, Model
import yaml

# Load spec
with open("openapi3.yaml") as f:
    spec = yaml.safe_load(f)

models = extract_models(spec["components"]["schemas"])

# Setup Jinja
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("model_template.j2")

# Render each model
for model in models:
    output = template.render(model=model)
    with open(f"{model.name.lower()}.py", "w") as f:
        f.write(output)
