from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import os
import re


def get_html(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    page_html = web_byte.decode('utf-8')

    page_soup = soup(page_html, "html.parser") # Parses the html.
    
    return page_soup

def store_lyrics(tracklist):
    tracklist_soup = {}
    for link in tracklist:
        print(link)
        try:
            tracklist_soup[link] = get_html(link)

            song_data = get_tracking_data(tracklist_soup[link])

            file_path = "datasets/lyrics/" + song_data['Primary Artist'] + '/' + song_data['Primary Album'] + '/'

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            filename = file_path + song_data['Title'] + '.txt'
            print(filename)
            file_object = open(filename, 'w')
            file_object.write(tracklist_soup[link].p.text)
            file_object.close()
        except:
            print("Cannot find the above link")

def get_links(link_type, soup):
    link_list = []
    if link_type == "album":
        try:
            all_albums_button = soup.findAll("a", {"class": "full_width_button"})
            all_albums_soup = get_html("https://genius.com" + all_albums_button[1]['href'])
            links = all_albums_soup.findAll("a", {"class": "album_link"})
            for album in links:
                link_list.append('https://genius.com' + album['href'])
        except IndexError: # Happens when artist has <7 total albums
            if link_type == "album":
                links = soup.findAll("a", {"class": "vertical_album_card"})
            for link in links:
                link_list.append(link["href"])
    elif link_type == "song":
        links = soup.findAll("a", {"class": "u-display_block"})
        for link in links:
            link_list.append(link["href"])
    return link_list

def get_tracking_data(soup):
    pattern = re.compile(r"var TRACKING_DATA = {.*?};$", re.MULTILINE | re.DOTALL)
    script = soup.find("script", text=pattern)
    tracking_data = pattern.search(script.text).group(0)[21:-2].split(',')
    tracking_data_dict = {}

    for item in tracking_data:
        split = item.split(":")
        tracking_data_dict[split[0].replace('"', '')] = split[1].replace('"', '')
        
    return tracking_data_dict

artist_links = ['https://genius.com/artists/Eminem',
               'https://genius.com/artists/Kendrick-lamar',
               'https://genius.com/artists/Kanye-west',
               'https://genius.com/artists/Dead-prez']

for artist in artist_links:
    artist_soup = get_html(artist)
    album_links = get_links('album', artist_soup)
    for album_link in album_links:
        album_soup = get_html(album_link)
        album_tracklist = get_links('song', album_soup)
        store_lyrics(album_tracklist)

sdgaf_lyrics = []
filename = "datasets/lyrics/Eminem/The Slim Shady LP/Still Don’t Give a Fuck.txt"
file = open(filename,'r')
for line in file:
    if line[0] not in ['[', '\n']:
        sdgaf_lyrics.append(line.replace("\n", ""))
file.close()