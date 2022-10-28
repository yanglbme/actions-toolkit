import os
from pathlib import Path
from uuid import uuid4

from actions_toolkit.utils import to_command_value


def issue_file_command(command: str, message):
    file_path = os.getenv(f'GITHUB_{command}')
    if not file_path:
        raise Exception(f'Unable to find environment variable '
                        f'for file command {command}')
    if not Path(file_path).exists():
        raise Exception(f'Missing file at path: {file_path}')
    with open(file_path, 'a', encoding='utf8', newline='') as f:
        f.write(f'{to_command_value(message)}{os.linesep}')


def prepare_key_value_message(key: str, value) -> str:
    delimiter = f'ghadelimiter_{uuid4()}'
    converted_value = to_command_value(value)

    # These should realistically never happen, but just in case someone finds a
    # way to exploit uuid generation let's not allow keys or values that contain
    # the delimiter.
    if delimiter in key:
        raise Exception(f'Unexpected input: name should not contain the delimiter "{delimiter}"')
    if delimiter in converted_value:
        raise Exception(f'Unexpected input: value should not contain the delimiter "{delimiter}"')
    return f'{key}<<{delimiter}{os.linesep}{converted_value}{os.linesep}{delimiter}'
