from collections import defaultdict
import json
from os import getenv
from os import path
from os import makedirs
import pkgutil

from .models.errors import MissingSettingsKeyError


SCHEMA_JSON = json.loads(pkgutil.get_data(
    __name__,
    'schema.json'
))
_APP_NAME = '-'.join(__name__.split('.')[0].split('_'))
_HOME = getenv('HOME', '/root')
_XDG_CACHE_DEFAULT = path.join(_HOME, '.cache')
_XDG_CACHE = getenv('XDG_CACHE_HOME', _XDG_CACHE_DEFAULT)
_XDG_CONFIG_DEFAULT = path.join(_HOME, '.config')
_XDG_CONFIG = getenv('XDG_CONFIG_HOME', _XDG_CONFIG_DEFAULT)
_CACHE = path.join(_XDG_CACHE, _APP_NAME)
_CONFIG = path.join(_XDG_CONFIG, _APP_NAME)
_APP_DIRECTORIES = (_CACHE, _CONFIG)
_CONFIG_JSON = path.join(_CONFIG, 'config.json')


def _default():
    MissingSettingsKeyError._default(_CONFIG_JSON)


try:
    with open(_CONFIG_JSON) as stream:
        SETTINGS = json.load(stream)
except FileNotFoundError:
    SETTINGS = {}
SETTINGS = defaultdict(_default, SETTINGS)


def make_directories():
    for directory in _APP_DIRECTORIES:
        # TODO: Handle other exceptions
        makedirs(directory, exist_ok=True)
