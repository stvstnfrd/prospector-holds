"""
Raise and handle custom exceptions
"""


class MissingSettingsKeyError(KeyError):
    """
    A custom version of KeyError when
    we're missing a settings key
    """

    @classmethod
    def _default(cls, config_json):
        """
        The default handler when accessing
        a missing key from the SETTINGS dict

        Since the settings are used to access external resources,
        we can't provide sensible defaults.
        There are currently some use-cases for this library that don't
        rely on those settings; we don't need to panic/raise if the file
        doesn't exist and we don't need it.

        But when we try to use these settings and they aren't set,
        we need to bail/panic.

        The error message includes an example of the required
        configuration fields to ease remediation for end-users.
        """
        example = {
            'SEARCH_PROTOCOL': 'https',
            'SEARCH_DOMAIN': 'example.com',
            'SEARCH_PATH_SEARCH': '/path/to/search/',
            'SEARCH_PATH_RECORD': '/path/to/record/',
            'SEARCH_PAGINATE_ID_PREFIX': 'pagination_link_',
            'SEARCH_RECORD_MARC_DATA_QUERY_STRING': {
                'marc_data': 'yes',
            },
        }
        example = str(example)
        example = '"'.join(example.split("'"))
        message = "Config file required at '{path}', like: \n\t{example}".format(
            path=config_json,
            example=example,
        )
        raise cls(message)
