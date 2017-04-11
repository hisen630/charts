import urlparse
from urllib import urlencode

def url_append_query(base_url, query):
    parts = list(urlparse.urlparse(base_url))
    if isinstance(query, basestring):
        query = urlparse.parse_qsl(query)
    elif isinstance(query, dict):
        query = query.items()
    parts[4] = urlencode(urlparse.parse_qsl(parts[4]) + query)
    return urlparse.urlunparse(parts)
