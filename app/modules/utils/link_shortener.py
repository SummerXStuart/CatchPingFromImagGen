import pyshorteners
shortener = pyshorteners.Shortener()

def shorten(long_url):
    short_url = shortener.tinyurl.short(long_url)
    return short_url
