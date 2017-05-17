"""String utils."""
import re


def split(input_str, spliters=' '):
    """Split string to parts."""
    pattern = '[{}]'.format(spliters)
    return [part for part in re.split(pattern, input_str) if part]
