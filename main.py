"""JSON Schema Validator - Validate JSON data against schemas."""

def validate(data, schema, path="root"):
    errors = []
    t = schema.get("type")
    if t:
        type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict, "null": type(None)}
        if not isinstance(data, type_map.get(t, object)):
            errors.append(f"{path}: expected {t}, got {type(data).__name__}")
            return errors
    if t == "object":
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                errors.append(f"{path}: missing required field '{key}'")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in data:
                errors.extend(validate(data[key], sub, f"{path}.{key}"))
    if t == "array":
        items = schema.get("items")
        if items:
            for i, item in enumerate(data):
                errors.extend(validate(item, items, f"{path}[{i}]"))
    if t == "string":
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: string too short (min {schema['minLength']})")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: string too long (max {schema['maxLength']})")
    if t in ("integer", "number"):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: value {data} < minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: value {data} > maximum {schema['maximum']}")
    return errors

if __name__ == "__main__":
    schema = {
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string", "minLength": 2},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "email": {"type": "string"},
        }
    }
    tests = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "B", "age": -5},
        {"age": 25},
    ]
    for t in tests:
        errs = validate(t, schema)
        status = "✅ Valid" if not errs else "❌ Invalid"
        print(f"{status}: {t}")
        for e in errs:
            print(f"   - {e}")
