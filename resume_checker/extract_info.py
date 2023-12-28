from pdfminer.high_level import extract_text
from geotext import GeoText

def extract(url):
    text = extract_text(url)
    return text

def plain_text(text):
    return text

def extract_city(text):
    places = GeoText(plain_text(text))
    print(places.cities)



url = 'test.pdf'
a = extract(url)
b = plain_text(a)
