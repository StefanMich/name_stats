import os

DB = 'names.db.dev'

try:
    from settings_override import *  # noqa
except ImportError:
    pass

if 'db_path' in os.environ:
    DB = os.environ['db_path']
