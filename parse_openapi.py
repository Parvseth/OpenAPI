import yaml
from openapi_spec_validator import validate_spec

# Load the OpenAPI YAML file
with open("openapi3.yaml", "r") as f:
    spec = yaml.safe_load(f)

# Print top-level keys to understand the structure
print("Top-level keys in OpenAPI spec:")
print(spec.keys())

# Print the available API paths
print("\nAvailable endpoints (paths):")
for path in spec['paths']:
    print(path)

# Print methods available under each path
print("\nHTTP methods per path:")
for path, methods in spec['paths'].items():
    print(f"{path}: {list(methods.keys())}")

# Print the schemas (data models)
print("\nComponent Schemas:")
for schema_name, schema_body in spec['components']['schemas'].items():
    print(f"{schema_name}: {schema_body['type']} with properties {schema_body.get('properties', {})}")


def safe_validate(spec):
    try:
        validate_spec(spec)
        print("✅ Spec is valid!")
    except Exception as e:
        print(f"❌ Spec is invalid: {type(e).__name__}: {e}")
safe_validate(spec)

