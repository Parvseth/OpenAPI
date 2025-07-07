from jinja2 import Environment, FileSystemLoader
from utils import load_yaml, extract_models
from logger import logger

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("route_template.j2")

def main():
    spec = load_yaml("openapi3.yaml")
    schemas = spec.get("components", {}).get("schemas", {})
    models = extract_models(schemas)
    for model in models:
        code = template.render(model=model, methods=["POST", "GET", "PUT", "DELETE"])
        with open(f"routes/{model.name.lower()}.py", "w") as f:
            f.write(code)
        logger.info(f"Generated routes/{model.name.lower()}.py")

if __name__ == "__main__":
    main()
