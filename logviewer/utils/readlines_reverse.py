import os

from ..settings import LOG_VIEWER_PATTERNS


def readlines_reverse(qfile, exclude=''):
    """
    """
    reversed_patterns = [pattern[::-1] for pattern in LOG_VIEWER_PATTERNS]

    qfile.seek(0, os.SEEK_END)
    position = qfile.tell()
    line = ''

    while position >= 0:
        qfile.seek(position)
        next_char = qfile.read(1)

        if next_char == '\n' and line:
            if any([line.endswith(p) for p in reversed_patterns]):
                if exclude in line[::-1]:
                    line = ''
                else:
                    yield line[::-1]
                    line = ''
        else:
            line += next_char
        position -= 1

    yield line[::-1]
