"""
Perform searches against the catalog
"""
from html.parser import HTMLParser
import requests
from urllib.parse import quote

from ..settings import SETTINGS


class Search:
    """
    Perform a search and fetch all paginated entries
    """

    @classmethod
    def query_title(cls, search_title):
        """
        Search the catalogue for items by title
        """
        page_number = 0
        # TODO: Make format configurable
        search_format = 'blu-ray'
        url = "{protocol}://{domain}{path}{page}?{params}".format(
            protocol=SETTINGS['SEARCH_PROTOCOL'],
            domain=SETTINGS['SEARCH_DOMAIN'],
            path=SETTINGS['SEARCH_PATH_SEARCH'],
            page="C__S{query}__P{page_number}__0rightresult__U".format(
                query=quote(
                    # TODO: I think title is incorrectly escaped;
                    #       see multi-word title terms.
                    "t:({title}) f:g ({format})".format(
                        title=search_title,
                        format=search_format,
                    )
                ),
                page_number=page_number,
            ),
            params='lang=eng&suite=def',
        )
        urls = set()
        while True:
            if url in urls:
                break
            urls.add(url)
            r = requests.get(url)
            parser = SearchResultParser()
            parser.feed(r.text)
            if len(parser.links) == 0:
                break
            for link in parser.links:
                yield link
            if not parser.next:
                break
            url = "{protocol}://{domain}/{path}".format(
                protocol=SETTINGS['SEARCH_PROTOCOL'],
                domain=SETTINGS['SEARCH_DOMAIN'],
                path=parser.next,
            )
            # Fail-safe: Stop, eventually, to avoid hammering servers if
            # we mistakenly get caught in a loop.
            # TODO: Remove this and/or make it configurable
            page_number += 1
            if page_number > 10:
                break


class SearchResultParser(HTMLParser):
    """
    An HTML parser to handle search results from the catalog
    """

    def __init__(self, *args, **kwargs):
        """
        This class is mostly a simple wrapper around the base HTMLParser.

        When we parse a document, we're looking for two kinds of links:
        - links to search results
        - a link to the next page of paginated results
        """
        self.links = set()
        self.next = ''
        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        """
        Parse tags, looking for links to search results
        or the "next" page if pagination
        """
        # Ignore all tags except anchors
        if tag != 'a':
            return
        is_pagination = False
        search_link = ''
        for (key, value) in attrs:
            if key == 'id' and value.startswith(SETTINGS['SEARCH_PAGINATE_ID_PREFIX']):
                # Mark the tag as a pagination link, but wait until we
                # find an href.
                is_pagination = True
            elif key == 'href':
                if value.find(SETTINGS['SEARCH_PATH_RECORD']) == 0:
                    self.links.add(value)
                    # We can stop once we know it's a link to a record.
                    return
                elif value.find(SETTINGS['SEARCH_PATH_SEARCH']) == 0:
                    # If it looks like a search link, we have to be sure
                    # it's actually a pagination link beore we can return.
                    search_link = value
        if is_pagination and search_link:
            self.next = search_link
