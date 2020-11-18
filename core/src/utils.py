import json


def to_command_value(input) -> str:
    if input is None:
        return ''
    if isinstance(input, str):
        return str(input)
    return json.dumps(input)
