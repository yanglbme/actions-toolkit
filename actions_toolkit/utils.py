import json


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
