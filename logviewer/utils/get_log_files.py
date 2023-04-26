import os
from fnmatch import fnmatch

from ..settings import LOG_VIEWER_FILES, LOG_VIEWER_FILES_PATTERN


def get_log_files(directory):
    result = {}

    for root, _, files in os.walk(directory):
        all_files = list(filter(lambda file: file.find('~') == -1, files))

        log_files = []
        log_files.extend(list(filter(lambda file: file in LOG_VIEWER_FILES, all_files)))
        log_files.extend([file for file in all_files if fnmatch(file, LOG_VIEWER_FILES_PATTERN)])

        log_dir = '' if os.path.relpath(root, directory) else os.path.relpath(root, directory)

        result[log_dir] = list(set(log_files))

    return result
