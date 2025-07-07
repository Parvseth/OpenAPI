def map_openapi_to_sqlalchemy(ftype, fmt=None, enum_vals=None, enum_class=None):
    mapping = {
        "integer": "Integer",
        "number": "Float",
        "string": "String",
        "boolean": "Boolean",
        "array": "ARRAY",
        "object": "JSON"
    }
    if enum_class:
        return f"Enum({enum_class})"
    return mapping.get(ftype, "String")

def map_openapi_to_pydantic(ftype, fmt=None, enum_vals=None, enum_class=None):
    mapping = {
        "integer": "int",
        "number": "float",
        "string": "str",
        "boolean": "bool",
        "array": "List",
        "object": "dict"
    }
    if enum_class:
        return enum_class
    return mapping.get(ftype, "str")
