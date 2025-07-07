# transferring functions : OpenAPI types to SQLAlchemy types
# and for OpenAPI types to python types

from typing import Optional , List
from sqlalchemy import JSON  # add this at the top

def map_openapi_to_python(oapi_type: str, fmt: Optional[str] = None) -> str:
    if oapi_type == "string":
        if fmt == "date":
            return "datetime.date"
        elif fmt == "date-time":
            return "datetime.datetime"
        else:
            return "str"
    elif oapi_type == "integer":
        return "int"
    elif oapi_type == "number":
        return "float"
    elif oapi_type == "boolean":
        return "bool"
    elif oapi_type == "array":
        return "List"  # You'll handle `items` separately
    elif oapi_type == "object":
        return "dict"  # fallback
    return "Any"



def map_openapi_to_sqlalchemy(type_, format=None, enum_values=None, enum_class=None, items_type=None):
    if enum_values:
        return f"Enum({enum_class})"
    
    mapping = {
        "integer": "Integer",
        "string": "String",
        "boolean": "Boolean",
        "number": "Float",
        "date": "Date",
        "date-time": "DateTime"
    }

    if type_ == "array":
        # Use JSON for better compatibility across DBs
        return "JSON"

    return mapping.get(type_, "String")



def map_openapi_to_pydantic(type_, format=None, enum_values=None, enum_class=None):
    if enum_values:
        return enum_class
    mapping = {
        "integer": "int",
        "string": "str",
        "boolean": "bool",
        "number": "float",
        "date": "date",
        "date-time": "datetime"
    }
    return mapping.get(type_, "str")
