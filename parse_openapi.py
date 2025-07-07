import yaml
import json

def parse_openapi_yaml(file_path):
    with open(file_path, 'r') as f:
        spec = yaml.safe_load(f)
    return spec

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    spec = parse_openapi_yaml("openapi3.yaml")
    save_json(spec, "openapi3.json")
