import yaml
from jinja2 import Environment, FileSystemLoader
from utils import load_yaml
from logger import logger

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("enum_template.j2")

def main():
    spec = load_yaml("openapi3.yaml")
    schemas = spec.get("components", {}).get("schemas", {})
    enums = []
    for name, schema in schemas.items():
        if "enum" in schema:
            enums.append({"name": name, "values": schema["enum"]})
    if not enums:
        logger.info("No enums found in the spec.")
        return
    output = template.render(enums=enums)
    with open("schemas/enums.py", "w") as f:
        f.write(output)
    logger.info("Generated schemas/enums.py")

if __name__ == "__main__":
    main()
