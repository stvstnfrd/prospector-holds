"""
Perform searches against the catalog
"""
from html.parser import HTMLParser


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
            if key == 'id' and value.startswith('searchPageLink_'):
                # Mark the tag as a pagination link, but wait until we
                # find an href.
                is_pagination = True
            elif key == 'href':
                if value.find('/iii/encore/record/') == 0:
                    self.links.add(value)
                    # We can stop once we know it's a link to a record.
                    return
                elif value.find('/iii/encore/search/') == 0:
                    # If it looks like a search link, we have to be sure
                    # it's actually a pagination link beore we can return.
                    search_link = value
        if is_pagination and search_link:
            self.next = search_link
