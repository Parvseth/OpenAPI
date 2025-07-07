def extract_enums(schemas):
    enums = []
    for name, schema in schemas.items():
        if "enum" in schema:
            enums.append({"name": name, "values": schema["enum"]})
    return enums

def extract_models(schemas):
    models = []
    for name, schema in schemas.items():
        if schema.get("type") == "object":
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            fields = []
            for pname, pdetails in properties.items():
                ptype = pdetails.get("type", "string")
                fields.append({
                    "name": pname,
                    "type": ptype,
                    "required": pname in required
                })
            models.append({"name": name, "fields": fields})
    return models
