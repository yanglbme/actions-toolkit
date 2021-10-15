import json
from typing import Optional


class AnnotationProperties:
    def __init__(self, title: Optional[str], file: Optional[str],
                 start_line: Optional[int], end_line: Optional[int],
                 start_column: Optional[int], end_column: Optional[int]):
        self.title = title
        self.file = file
        self.start_line = start_line
        self.end_line = end_line
        self.start_column = start_column
        self.end_column = end_column


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
