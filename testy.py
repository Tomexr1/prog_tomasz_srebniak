import requests
import webbrowser
from bs4 import BeautifulSoup


res = requests.get('https://en.wikipedia.org/wiki/Special:Random')
bs4_object = BeautifulSoup(res.text, 'html.parser')
url = bs4_object.select('link[rel="canonical"]')[0].get('href')
title = bs4_object.select('h1')[0].getText()
# print('Czy chcesz przeczytać artykuł o ' + title + '?')
# if input('T/N: ').lower() == 't':
#     webbrowser.open(url)
print(bs4_object.prettify())
