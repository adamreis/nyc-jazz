from bs4 import BeautifulSoup
from urllib2 import urlopen

def make_soup(url):
    """Downloads the contents of the url and soupifies it"""
    try:
        html = urlopen(url).read()
    except:
        html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def puncify(s):
    """Replaces unicode characters with the appropriate ASCII punctuation"""
    return s.replace(u'\xa0', u' ').replace(u'\u201c', '"').replace(u'\u201d', '"').replace(u'\u2019', "'").replace(u"&amp;", '&')