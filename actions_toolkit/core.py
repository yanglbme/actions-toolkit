import enum
import os
import sys
from typing import List, Union

from actions_toolkit.command import issue_command, issue
from actions_toolkit.file_command import issue_command as issue_file_command
from actions_toolkit.oidc_utils import OidcClient
from actions_toolkit.utils import to_command_value, to_command_properties, AnnotationProperties


class InputOptions:
    """Interface for getInput options"""

    def __init__(self, required: bool = False, trim_whitespace: bool = True):
        """Optional. Whether the input is required. If required and not present, will throw. Defaults to false"""
        self.required = required

        """Optional. Whether leading/trailing whitespace will be trimmed for the input. Defaults to true"""
        self.trim_whitespace = trim_whitespace


@enum.unique
class ExitCode(enum.IntEnum):
    """The code to exit an action"""

    """A code indicating that the action was successful"""
    success = 0

    """A code indicating that the action was a failure"""
    failure = 1


# -----------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------

def export_variable(name: str, val):
    """
    Sets env variable for this action and future actions_toolkit in the job
    :param name: the name of the variable to set
    :param val: the value of the variable. Non-string values will be converted to a string via json.dumps
    :return: void
    """
    converted_val = to_command_value(val)
    os.environ[name] = converted_val

    file_path = os.getenv('GITHUB_ENV')
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
    Prepends inputPath to the PATH (for this action and future actions_toolkit)
    :param input_path: value of the path
    :return: void
    """
    file_path = os.getenv('GITHUB_PATH')
    if file_path:
        issue_file_command('PATH', input_path)
    else:
        issue_command('add-path', {}, input_path)
    os.environ['PATH'] = f'{input_path}{os.pathsep}{os.getenv("PATH")}'


def get_input(name: str, **options) -> str:
    """
    Gets the value of an input.
    Unless trimWhitespace is set to false in InputOptions, the value is also trimmed.
    Returns an empty string if the value is not defined.
    """
    options = InputOptions(**options)
    name = name.replace(' ', '_').upper()
    val = os.getenv(f'INPUT_{name}', '')
    if options.required and not val:
        raise Exception(f'Input required and not supplied: {name}')
    if not options.trim_whitespace:
        return val
    return val.strip()


def get_multiline_input(name: str, **options) -> List[str]:
    """
    Gets the values of an multiline input.  Each value is also trimmed.
    """
    return list(filter(lambda x: x != '', get_input(name, **options).split("\n")))


def get_boolean_input(name: str, **options) -> bool:
    """
    Gets the input value of the boolean type in the YAML 1.2 "core schema" specification.
    Support boolean input list: `true | True | TRUE | false | False | FALSE` .
    The return value is also in boolean type.
    ref: https://yaml.org/spec/1.2/spec.html#id2804923
    """
    true_value = ['true', 'True', 'TRUE']
    false_value = ['false', 'False', 'FALSE']
    val = get_input(name, **options)
    if val in true_value:
        return True
    if val in false_value:
        return False
    raise TypeError(f'Input does not meet YAML 1.2 "Core Schema" specification: {name}\n'
                    f'Support boolean input list: `true | True | TRUE | false | False | FALSE`')


def set_output(name: str, value):
    """
    Sets the value of an output.
    :param name: name of the output to set
    :param value: value to store. Non-string values will be converted to a string via json.dumps
    :return: void
    """
    sys.stdout.write(os.linesep)
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

def set_failed(message: Union[str, Exception]):
    """
    Sets the action status to failed.
    When the action exits it will be with an exit code of 1
    :param message: add error issue message
    :return: void
    """
    error(message)
    sys.exit(ExitCode.failure.value)


def is_debug() -> bool:
    """Gets whether Actions Step Debug is on or not"""
    return os.getenv('RUNNER_DEBUG') == '1'


def debug(message: str):
    """
    Writes debug message to user log
    :param message: debug message
    :return: void
    """
    issue_command('debug', {}, message)


def error(message: Union[str, Exception], **properties):
    """
    Adds an error issue
    :param message: error issue message. Errors will be converted to string via str()
    """
    properties = AnnotationProperties(**properties) if properties else properties
    if isinstance(message, Exception):
        message = f'Error: {str(message)}'
    issue_command('error', to_command_properties(properties), message)


def warning(message: Union[str, Exception], **properties):
    """
    Adds a warning issue
    :param message: warning issue message. Errors will be converted to string via str()
    """
    properties = AnnotationProperties(**properties) if properties else properties
    if isinstance(message, Exception):
        message = f'Error: {str(message)}'
    issue_command('warning', to_command_properties(properties), message)


def notice(message: Union[str, Exception], **properties):
    """
    Adds a notice issue
    :param message: notice issue message. Errors will be converted to string via str()
    """
    properties = AnnotationProperties(**properties) if properties else properties
    if isinstance(message, Exception):
        message = f'Error: {str(message)}'
    issue_command('notice', to_command_properties(properties), message)


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
    return os.getenv(f'STATE_{name}', '')


def get_id_token(aud: str = None) -> str:
    id_token = OidcClient.get_id_token(aud)
    set_secret(id_token)
    return id_token
