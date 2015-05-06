from bs4 import BeautifulSoup
from urllib2 import urlopen

def make_soup(url):
    """Downloads the contents of the url and soupifies it"""
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def puncify(s):
    """Replaces unicode characters with the appropriate ASCII punctuation"""
    return s.replace(u'\u201c', '"').replace(u'\u201d', '"').replace(u'\u2019', "'")