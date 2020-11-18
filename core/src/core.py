import os

from command import issue_command, issue
from file_command import issue_command as issue_file_command
from utils import to_command_value


def export_variable(name: str, val):
    converted_val = to_command_value(val)
    os.environ.setdefault(name, converted_val)

    file_path = os.environ.get('GITHUB_ENV') or ''
    if file_path:
        delimiter = '_GitHubActionsFileCommandDelimeter_'
        command_value = f'{name}<<{delimiter}{os.linesep}{converted_val}{os.linesep}{delimiter}'
        issue_file_command('ENV', command_value)
    else:
        issue_command('set-env', {name: None}, converted_val)


def set_secret(secret: str):
    issue_command('add-mask', {}, secret)


def add_path(input_path: str):
    file_path = os.environ.get('GITHUB_PATH') or ''
    if file_path:
        issue_file_command('PATH', input_path)
    else:
        issue_command('add-path', {}, input_path)
    os.environ.setdefault('PATH', f'{input_path}{os.pathsep}{os.environ.get("PATH")}')


def get_input(name: str, required: bool = True) -> str:
    name = f'INPUT_{name.replace(" ", "_").upper()}'
    val = os.environ.get(name) or ''
    if required and not val:
        raise Exception(f'Input required and not supplied: {name}')
    return val.strip()


def set_output(name: str, value):
    issue_command('set-output', {name: None}, value)


def set_command_echo(enabled: bool):
    issue('echo', 'on' if enabled else 'off')


def set_failed(message: str):
    pass
