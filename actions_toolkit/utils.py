import json
import os
from typing import List


class AnnotationProperties:
    def __init__(self, title: str = None, file: str = None,
                 start_line: int = None, end_line: int = None,
                 start_column: int = None, end_column: int = None):
        # A title for the annotation.
        self.title = title

        # The path of the file for which the annotation should be created.
        self.file = file

        # The start line for the annotation.
        self.start_line = start_line

        # The end line for the annotation. Defaults to `start_line` when `start_line` is provided.
        self.end_line = end_line

        # The start column for the annotation. Cannot be sent when `start_line` and `end_line` are different values.
        self.start_column = start_column

        # The start column for the annotation. Cannot be sent when `start_line` and `end_line` are different values.
        # Defaults to `start_column` when `start_column` is provided.
        self.end_column = end_column


class OctokitOptions:
    def __init__(self, auth_strategy=None, auth=None, user_agent: str = None,
                 previews: List[str] = None, base_url: str = None, log=None,
                 request=None, time_zone: str = None):
        self.auth_strategy = auth_strategy
        self.auth = auth
        self.user_agent = user_agent
        self.previews = previews
        self.base_url = base_url
        self.log = log
        self.request = request
        self.time_zone = time_zone


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


def to_command_properties(annotation_properties: AnnotationProperties) -> dict:
    if not annotation_properties:
        return {}
    return {
        'title': annotation_properties.title,
        'file': annotation_properties.file,
        'line': annotation_properties.start_line,
        'endLine': annotation_properties.end_line,
        'col': annotation_properties.start_column,
        'endColumn': annotation_properties.end_column
    }


def get_api_base_url() -> str:
    return os.getenv('GITHUB_API_URL', 'https://api.github.com')


def get_auth_string(token: str, **options) -> str:
    options = OctokitOptions(**options)
    if not token and not options.auth:
        raise Exception('Parameter token or opts.auth is required')
    return options.auth if isinstance(options.auth, str) else f'token {token}'
