from dataclasses import dataclass
from typing import List, Optional, Dict
import yaml
from type_mapper import map_openapi_to_sqlalchemy, map_openapi_to_pydantic


@dataclass
class Field:
    name: str
    type: str
    required: bool = False
    ref: Optional[str] = None
    sqla_type: Optional[str] = None
    pydantic_type: Optional[str] = None
    enum_values: Optional[List[str]] = None
    enum_class_name: Optional[str] = None
    format: Optional[str] = None
    is_primary: bool = False
    enum_class: Optional[str] = None


@dataclass
class Model:
    name: str
    fields: List[Field]


@dataclass
class Route:
    path: str
    method: str
    request_schema: Optional[str] = None
    response_schema: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None


@dataclass
class EnumDefinition:
    name: str
    enum_values: List[str]


# --- Extract Schemas to Models ---
def extract_models(schemas: dict) -> List[Model]:
    models = []

    for model_name, schema in schemas.items():
        if schema.get("type") != "object":
            continue

        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        fields = []

        # --- Infer primary key ---
        primary_field = None
        for fname in properties:
            if fname.lower() in {"id", f"{model_name.lower()}id", f"{model_name.lower()}_id"}:
                primary_field = fname
                break
        if not primary_field and properties:
            primary_field = next(iter(properties))

        for field_name, field_schema in properties.items():
            openapi_type = field_schema.get("type", "any")
            openapi_format = field_schema.get("format")
            enum_values = field_schema.get("enum")

            enum_class_name = f"{field_name.capitalize()}Enum" if enum_values else None
            enum_class = f"{field_name[0].upper()}{field_name[1:]}Enum" if enum_values else None

            if openapi_type == "array":
                item_type = field_schema.get("items", {}).get("type", "string")
                field_type = f"List[{item_type}]"
                sqla_type = map_openapi_to_sqlalchemy(openapi_type, format=openapi_format, items_type=item_type)
                pydantic_type = f"List[{map_openapi_to_pydantic(item_type)}]"
                ref_model = None
            elif "$ref" in field_schema:
                ref_model = field_schema["$ref"].split("/")[-1]
                field_type = ref_model
                sqla_type = "Integer"
                pydantic_type = ref_model
            else:
                ref_model = None
                field_type = openapi_type
                sqla_type = map_openapi_to_sqlalchemy(
                    openapi_type,
                    openapi_format,
                    enum_values,
                    enum_class=enum_class
                )
                pydantic_type = map_openapi_to_pydantic(
                    openapi_type,
                    openapi_format,
                    enum_values,
                    enum_class=enum_class
                )

            is_required = field_name in required_fields
            is_primary = field_name == primary_field

            fields.append(Field(
                name=field_name,
                type=field_type,
                required=is_required,
                ref=ref_model,
                sqla_type=sqla_type,
                pydantic_type=pydantic_type,
                enum_values=enum_values,
                enum_class_name=enum_class_name,
                format=openapi_format,
                is_primary=is_primary,
                enum_class=enum_class_name
            ))

        models.append(Model(name=model_name, fields=fields))

    return models


# --- Extract Paths to Routes ---
def extract_routes(paths: dict) -> List[Route]:
    routes = []

    for path, methods in paths.items():
        for method, details in methods.items():
            request_schema = None
            response_schema = None

            # Extract summary and description
            summary = details.get("summary")
            description = details.get("description")

            # Extract request schema
            if "requestBody" in details:
                content = details["requestBody"].get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    if "$ref" in schema:
                        request_schema = schema["$ref"].split("/")[-1]

            # Extract response schema
            responses = details.get("responses", {})
            for code in ["200", "201"]:
                if code in responses:
                    content = responses[code].get("content", {})
                    if "application/json" in content:
                        schema = content["application/json"].get("schema", {})
                        if "$ref" in schema:
                            response_schema = schema["$ref"].split("/")[-1]
                    break

            # Add route object
            routes.append(Route(
                path=path,
                method=method.upper(),
                request_schema=request_schema,
                response_schema=response_schema,
                summary=summary,
                description=description
            ))

    return routes


def extract_tags(routes: List[Route]) -> List[str]:
    tags = set()
    for route in routes:
        if route.request_schema:
            tags.add(route.request_schema.lower())
        elif route.response_schema:
            tags.add(route.response_schema.lower())
    return sorted(tags)


# --- Full Spec Wrapper ---
def get_final_data_model(spec: dict) -> Dict:
    schemas = spec["components"]["schemas"]
    return {
        "models": extract_models(schemas),
        "routes": extract_routes(spec["paths"])
    }


def extract_enums(schemas: dict) -> List[EnumDefinition]:
    enums = []
    for name, schema in schemas.items():
        if "enum" in schema:
            enums.append(EnumDefinition(name=name, enum_values=schema["enum"]))
    return enums


# --- Debugging ---
if __name__ == "__main__":
    from pprint import pprint

    with open("openapi3.yaml", "r") as f:
        spec = yaml.safe_load(f)

    final_data_model = get_final_data_model(spec)

    for model in final_data_model["models"]:
        print(f"\nModel: {model.name}")
        for field in model.fields:
            ref_info = f" → {field.ref}" if field.ref else ""
            enum_info = f" enum({field.enum_class_name})" if field.enum_class_name else ""
            required = "required" if field.required else "optional"
            print(f"  - {field.name} ({field.type}) {required}{ref_info}{enum_info}")

    print("\nRoutes:")
    for route in final_data_model["routes"]:
        print(f"  {route.method} {route.path} (Request: {route.request_schema}, Response: {route.response_schema})")
