from collections import defaultdict
from schemas_to_model import extract_routes  # Make sure this returns List[Route]
import yaml

with open("openapi3.yaml", "r") as f:
    spec = yaml.safe_load(f)
# After you've loaded your OpenAPI spec
routes = extract_routes(spec["paths"])

# This will hold model → set of methods
model_method_map = defaultdict(set)

for route in routes:
    if route.request_schema:
        model_method_map[route.request_schema].add(route.method)
    elif route.response_schema:
        model_method_map[route.response_schema].add(route.method)

# Convert sets to lists
model_methods = {model: list(methods) for model, methods in model_method_map.items()}

# Optional: Print result
from pprint import pprint
pprint(model_methods)
