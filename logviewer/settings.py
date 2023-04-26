# LOG_VIEWER_FILES = getattr(settings, 'LOG_VIEWER_FILES', [])
'''
LOG_VIEWER_FILES = getattr(settings, 'LOG_VIEWER_FILES', [])
LOG_VIEWER_FILES_PATTERN = getattr(settings, 'LOG_VIEWER_FILES_PATTERN', '*.log*')
LOG_VIEWER_FILES_DIR = getattr(settings, 'LOG_VIEWER_FILES_DIR', 'logs/')
LOG_VIEWER_PAGE_LENGTH = getattr(settings, 'LOG_VIEWER_PAGE_LENGTH', 25)
LOG_VIEWER_MAX_READ_LINES = getattr(settings, 'LOG_VIEWER_MAX_READ_LINES', 1000)
LOG_VIEWER_FILE_LIST_TITLE = getattr(settings, 'LOG_VIEWER_FILE_LIST_TITLE', None)
LOG_VIEWER_FILE_LIST_STYLES = getattr(settings, 'LOG_VIEWER_FILE_LIST_STYLES', None)
LOG_VIEWER_PATTERNS = getattr(settings, 'LOG_VIEWER_PATTERNS', ['[INFO]', '[DEBUG]', '[WARNING]',
                                                                '[ERROR]', '[CRITICAL]'])
'''
LOG_VIEWER_FILES = ['debug', ]
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = 'logs/'
LOG_VIEWER_PAGE_LENGTH = 100       # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']

# Optionally you can set the next variables in order to customize the admin:
LOG_VIEWER_FILE_LIST_TITLE = "Logs de sistema"
LOG_VIEWER_FILE_LIST_STYLES = "/static/css/my-custom.css"
