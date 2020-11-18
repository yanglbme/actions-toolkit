import json


def to_command_value(input) -> str:
    if not input:
        return ''
    if isinstance(input, str):
        return str(input)
    return json.dumps(input)
