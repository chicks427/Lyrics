from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

my_url = 'https://genius.com/artists/Kanye-west'
req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

web_byte = urlopen(req).read()
page_html = web_byte.decode('utf-8')

page_soup = soup(page_html, "html.parser") # Parses the html.

albums = page_soup.findAll("a", {"class": "vertical_album_card"})

print(albums[0])