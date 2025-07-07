from dataclasses import dataclass
from typing import Optional, Dict, List
import yaml

@dataclass
class Route:
    path: str
    method: str
    operation_id: Optional[str]
    request_schema: Optional[str] = None  # Schema name
    response_schemas: Dict[str, str] = None  # status_code -> schema name


def resolve_ref(ref: str) -> str:
    """Extract the model name from a $ref like '#/components/schemas/User'"""
    return ref.split("/")[-1]


def extract_routes(spec: dict) -> List[Route]:
    routes = []

    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, operation in methods.items():
            operation_id = operation.get("operationId")

            # Request schema
            request_schema = None
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            app_json = content.get("application/json", {})
            schema = app_json.get("schema")

            if schema:
                if "$ref" in schema:
                    request_schema = resolve_ref(schema["$ref"])
                elif "type" in schema:
                    request_schema = schema.get("type")  # fallback to type

            # Response schemas
            response_schemas = {}
            responses = operation.get("responses", {})
            for status_code, resp in responses.items():
                content = resp.get("content", {})
                app_json = content.get("application/json", {})
                schema = app_json.get("schema")
                if schema and "$ref" in schema:
                    response_schemas[status_code] = resolve_ref(schema["$ref"])

            routes.append(Route(
                path=path,
                method=method.upper(),
                operation_id=operation_id,
                request_schema=request_schema,
                response_schemas=response_schemas
            ))

    return routes

with open("openapi3.yaml", "r") as f:
    spec = yaml.safe_load(f)

routes = extract_routes(spec)

for route in routes:
    print(f"\n🔹 Route: {route.method} {route.path}")
    print(f"  Operation ID: {route.operation_id}")
    print(f"  Request Schema: {route.request_schema}")
    print(f"  Response Schemas: {route.response_schemas}")
