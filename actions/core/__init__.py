import enum
import os
import sys

from actions.core.command import issue_command, issue
from actions.core.file_command import issue_command as issue_file_command
from actions.core.utils import to_command_value


@enum.unique
class ExitStatus(enum.IntEnum):
    """Portable definitions for the standard POSIX exit codes."""

    success = 0
    """Indicates successful program completion."""

    failure = 1
    """Indicates unsuccessful program completion in a general sense."""


def export_variable(name: str, val):
    converted_val = to_command_value(val)
    os.environ.setdefault(name, converted_val)

    file_path = os.environ.get('GITHUB_ENV') or ''
    if file_path:
        delimiter = '_GitHubActionsFileCommandDelimeter_'
        command_value = f'{name}<<{delimiter}{os.linesep}{converted_val}{os.linesep}{delimiter}'
        issue_file_command('ENV', command_value)
    else:
        issue_command('set-env', dict(name=name), converted_val)


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
    issue_command('set-output', dict(name=name), value)


def set_command_echo(enabled: bool):
    issue('echo', 'on' if enabled else 'off')


def set_failed(message: str):
    error(message)
    sys.exit(1)


def is_debug() -> bool:
    return os.environ.get('RUNNER_DEBUG') == '1'


def debug(message: str):
    issue_command('debug', {}, message)


def error(message: str):
    issue('error', message)


def warning(message: str):
    issue('warning', message)


def info(message: str):
    sys.stdout.write(message + os.linesep)


def start_group(name: str):
    issue('group', name)


def end_group():
    issue('endgroup')


async def group(name: str, fn):
    start_group(name)
    try:
        result = await fn()
    finally:
        end_group()
    return result


def save_state(name: str, value):
    issue_command('save-state', dict(name=name), value)


def get_state(name: str) -> str:
    return os.environ.get(f'STATE_{name}') or ''
