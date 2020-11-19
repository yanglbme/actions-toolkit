import json


def to_command_value(input_val) -> str:
    """
    Sanitizes an input into a string so it can be passed into issueCommand safely
    :param input_val: input to sanitize into a string
    :return: string
    """
    if input_val is None:
        return ''
    if isinstance(input_val, str):
        return str(input_val)
    return json.dumps(input_val)
