new_map_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "image_path": {"type": "string", "minLength": 1},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["title", "image_path", "timestamp"],
    "additionalProperties": False
}
