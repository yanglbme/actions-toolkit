import os
from pathlib import Path

from actions_toolkit.utils import to_command_value


def issue_command(command: str, message):
    file_path = os.getenv(f'GITHUB_{command}')
    if not file_path:
        raise Exception(f'Unable to find environment variable '
                        f'for file command {command}')
    if not Path(file_path).exists():
        raise Exception(f'Missing file at path: {file_path}')
    with open(file_path, 'a', encoding='utf8', newline='') as f:
        f.write(f'{to_command_value(message)}{os.linesep}')
