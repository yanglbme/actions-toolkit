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


# -----------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------

def export_variable(name: str, val):
    """
    Sets env variable for this action and future actions in the job
    :param name: the name of the variable to set
    :param val: the value of the variable. Non-string values will be converted to a string via json.dumps
    :return: void
    """
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
    """
    Registers a secret which will get masked from logs
    :param secret: value of the secret
    :return: void
    """
    issue_command('add-mask', {}, secret)


def add_path(input_path: str):
    """
    Prepends inputPath to the PATH (for this action and future actions)
    :param input_path: value of the path
    :return: void
    """
    file_path = os.environ.get('GITHUB_PATH') or ''
    if file_path:
        issue_file_command('PATH', input_path)
    else:
        issue_command('add-path', {}, input_path)
    os.environ.setdefault('PATH', f'{input_path}{os.pathsep}{os.environ.get("PATH")}')


def get_input(name: str, required: bool = True) -> str:
    """
    Gets the value of an input. The value is also trimmed.
    :param name: name of the input to get
    :param required: if required or not
    :return: string
    """
    name = f'INPUT_{name.replace(" ", "_").upper()}'
    val = os.environ.get(name) or ''
    if required and not val:
        raise Exception(f'Input required and not supplied: {name}')
    return val.strip()


def set_output(name: str, value):
    """
    Sets the value of an output.
    :param name: name of the output to set
    :param value: value to store. Non-string values will be converted to a string via json.dumps
    :return: void
    """
    issue_command('set-output', dict(name=name), value)


def set_command_echo(enabled: bool):
    """
    Enables or disables the echoing of commands into stdout for the rest of the step.
    Echoing is disabled by default if ACTIONS_STEP_DEBUG is not set.
    """
    issue('echo', 'on' if enabled else 'off')


# -----------------------------------------------------------------------
# Results
# -----------------------------------------------------------------------

def set_failed(message: str):
    """
    Sets the action status to failed.
    When the action exits it will be with an exit code of 1
    :param message: add error issue message
    :return: void
    """
    error(message)
    sys.exit(1)


def is_debug() -> bool:
    """Gets whether Actions Step Debug is on or not"""
    return os.environ.get('RUNNER_DEBUG') == '1'


def debug(message: str):
    """
    Writes debug message to user log
    :param message: debug message
    :return: void
    """
    issue_command('debug', {}, message)


def error(message: str):
    """
    Adds an error issue
    :param message: error issue message. Errors will be converted to string via str()
    :return: void
    """
    issue('error', message)


def warning(message: str):
    """
    Adds an warning issue
    :param message: warning issue message. Errors will be converted to string via str()
    :return: void
    """
    issue('warning', message)


def info(message: str):
    """
    Writes info to log with console.log.
    :param message: info message
    :return: void
    """
    sys.stdout.write(message + os.linesep)


def start_group(name: str):
    """
    Begin an output group.

    Output until the next `groupEnd` will be foldable in this group
    :param name: The name of the output group
    :return: void
    """
    issue('group', name)


def end_group():
    """End an output group."""
    issue('endgroup')


async def group(name: str, fn):
    """
    Wrap an asynchronous function call in a group.

    Returns the same type as the function itself.
    :param name: The name of the group
    :param fn: The function to wrap in the group
    """
    start_group(name)
    try:
        result = await fn()
    finally:
        end_group()
    return result


# -----------------------------------------------------------------------
# Wrapper action state
# -----------------------------------------------------------------------

def save_state(name: str, value):
    """
    Saves state for current action, the state can only be retrieved by this action's post job execution.
    :param name: name of the state to store
    :param value: value to store. Non-string values will be converted to a string via json.dumps
    :return: void
    """
    issue_command('save-state', dict(name=name), value)


def get_state(name: str) -> str:
    """
    Gets the value of an state set by this action's main execution.
    :param name: name of the state to get
    :return: string
    """
    return os.environ.get(f'STATE_{name}') or ''
