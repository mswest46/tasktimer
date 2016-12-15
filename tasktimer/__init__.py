# __init__.py

import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path = ""):
    return os.path.join(_ROOT, 'data', path)

__version__ = '1.0.0'

