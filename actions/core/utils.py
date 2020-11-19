import json


def to_command_value(input_val) -> str:
    if input_val is None:
        return ''
    if isinstance(input_val, str):
        return str(input_val)
    return json.dumps(input_val)
