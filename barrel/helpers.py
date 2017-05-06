try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_urls_from_file(fname):
    with open(fname) as f:
        content = f.readlines()
    # remove the whitespaces
    return [x.strip() for x in content]


def get_domain_from_url(url):
    parsed_uri = urlparse(url)
    return parsed_uri.netloc