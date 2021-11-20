import os
import sys

from actions_toolkit.utils import to_command_value


def issue_command(command: str, properties: dict, message):
    """
    Commands

    Command Format:
        ::name key=value,key=value::message

    Examples:
        ::warning::This is the message
        ::set-env name=MY_VAR::some value
    """
    cmd = Command(command, properties, message)
    sys.stdout.write(str(cmd) + os.linesep)


def issue(name: str, message: str = ''):
    issue_command(name, {}, message)


CMD_STRING = '::'


class Command:
    command: str
    message: str
    properties: dict

    def __init__(self, command: str, properties: dict, message: str):
        self.command = command or 'missing.command'
        self.properties = properties
        self.message = message

    def __str__(self):
        cmd_str = CMD_STRING + self.command
        if self.properties and len(self.properties) > 0:
            cmd_str += ' '
            first = True
            for k, v in self.properties.items():
                if v:
                    if first:
                        first = False
                    else:
                        cmd_str += ','
                    cmd_str += f'{k}={escape_property(v)}'
        cmd_str += f'{CMD_STRING}{escape_data(self.message)}'
        return cmd_str


def escape_data(s) -> str:
    return to_command_value(s).replace('%', '%25') \
        .replace('\r', '%0D').replace('\n', '%0A')


def escape_property(s) -> str:
    return to_command_value(s).replace('%', '%25').replace('\r', '%0D') \
        .replace('\n', '%0A').replace(':', '%3A').replace(',', '%2C')
