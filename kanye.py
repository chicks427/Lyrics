from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

def get_html(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

	web_byte = urlopen(req).read()
	page_html = web_byte.decode('utf-8')

	page_soup = soup(page_html, "html.parser") # Parses the html.
	return page_soup

def get_links(link_type, soup):
	link_list = []
	if link_type == "album":
		links = soup.findAll("a", {"class": "vertical_album_card"})
	elif link_type == "song":
		links = soup.findAll("a", {"class": "u-display_block"})
	for link in links:
		link_list.append(link["href"])
	return link_list

Kanye_soup = get_html('https://genius.com/artists/Kanye-west')
Kanye_albums = get_links('album', Kanye_soup)

pablo = get_html(Kanye_albums[0])
kanye_tracklist = get_links('song', pablo)

for song in kanye_tracklist:
	print(song)