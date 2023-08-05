DB = 'names.db.dev'

try:
    from settings_override import *  # noqa
except ImportError:
    pass
