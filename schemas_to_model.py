from dataclasses import dataclass
from typing import List, Optional, Dict, Any
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
    example: Optional[Any] = None   # ✅ added for automatic example injection

@dataclass
class Model:
    name: str
    fields: List[Field]

@dataclass
class EnumDefinition:
    name: str
    enum_values: List[str]

def extract_models(schemas: dict) -> List[Model]:
    models = []
    for name, schema in schemas.items():
        if schema.get("type") != "object":
            continue

        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])
        fields = []
        primary_field = None

        # Determine primary field
        for fname in properties:
            if fname.lower() == "id" or fname.lower() == f"{name.lower()}id":
                primary_field = fname
                break
        if not primary_field and properties:
            primary_field = list(properties.keys())[0]

        for fname, fdetails in properties.items():
            ftype = fdetails.get("type", "string")
            fmt = fdetails.get("format")
            enum_vals = fdetails.get("enum")
            ref_model = None

            if "$ref" in fdetails:
                # Handle references
                ref_model = fdetails["$ref"].split("/")[-1]
                ftype = ref_model
                sqla_type = "Integer"
                pydantic_type = ref_model
                example = 1  # Default example for FK references
            else:
                enum_class = f"{fname.capitalize()}Enum" if enum_vals else None
                sqla_type = map_openapi_to_sqlalchemy(ftype, fmt, enum_vals, enum_class)
                pydantic_type = map_openapi_to_pydantic(ftype, fmt, enum_vals, enum_class)

                # ✅ Automatic safe example injection
                example = fdetails.get("example")
                if example is None:
                    if ftype == "integer" or ftype == "number":
                        example = 0
                    elif ftype == "boolean":
                        example = False
                    elif ftype == "array":
                        example = []
                    elif ftype == "object":
                        example = {}
                    else:
                        example = "example_value"

            fields.append(Field(
                name=fname,
                type=ftype,
                required=fname in required_fields,
                ref=ref_model,
                sqla_type=sqla_type,
                pydantic_type=pydantic_type,
                enum_values=enum_vals,
                enum_class_name=enum_class if enum_vals else None,
                format=fmt,
                is_primary=fname == primary_field,
                example=example   # ✅ ensures test generation does not fail
            ))
        models.append(Model(name=name, fields=fields))
    return models

def extract_enums(schemas: dict) -> List[EnumDefinition]:
    enums = []
    for name, schema in schemas.items():
        if "enum" in schema:
            enums.append(EnumDefinition(name=name, enum_values=schema["enum"]))
    return enums

@dataclass
class Route:
    path: str
    method: str
    request_schema: Optional[str]
    response_schema: Optional[str]
    tag: Optional[str]

def extract_routes(paths: dict) -> List[Route]:
    routes = []
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue

            request_schema = None
            response_schema = None

            # Request schema detection
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            for media_type, media_content in content.items():
                schema = media_content.get("schema", {})
                if "$ref" in schema:
                    request_schema = schema["$ref"].split("/")[-1]
                elif schema.get("items", {}).get("$ref"):
                    request_schema = schema["items"]["$ref"].split("/")[-1]

            # Response schema detection
            responses = operation.get("responses", {})
            for status_code in ["200", "201", "default"]:
                resp = responses.get(status_code, {})
                content = resp.get("content", {})
                for media_type, media_content in content.items():
                    schema = media_content.get("schema", {})
                    if "$ref" in schema:
                        response_schema = schema["$ref"].split("/")[-1]
                    elif schema.get("items", {}).get("$ref"):
                        response_schema = schema["items"]["$ref"].split("/")[-1]
                    if response_schema:
                        break
                if response_schema:
                    break

            tag = None
            tags = operation.get("tags")
            if tags and isinstance(tags, list):
                tag = tags[0]

            routes.append(Route(
                path=path,
                method=method.upper(),
                request_schema=request_schema,
                response_schema=response_schema,
                tag=tag
            ))
    return routes
