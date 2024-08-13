import json
import pkgutil


SCHEMA_JSON = json.loads(pkgutil.get_data(
    __name__,
    'schema.json'
))
