from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import os
import re
import json

def get_html(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    page_html = web_byte.decode('utf-8')

    page_soup = soup(page_html, "html.parser") # Parses the html.
    
    return page_soup

def store_lyrics(tracklist):
    tracklist_soup = {}
    for link in album_tracklist:
        tracklist_soup[link] = get_html(link)
        
        song_data = get_tracking_data(tracklist_soup[link])

        file_path = song_data['Primary Artist'] + '/' + song_data['Primary Album'] + '/'
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        filename = tracklist_soup[link].head.title.text.replace(u'\xa0', u' ')
        filename = file_path + filename + '.txt'
        print(filename)
        file_object = open(filename, 'w')
        file_object.write(tracklist_soup[link].p.text)
        file_object.close()

def get_links(link_type, soup):
    link_list = []
    if link_type == "album":
        links = soup.findAll("a", {"class": "vertical_album_card"})
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

artist_soup = get_html('https://genius.com/artists/Kanye-west')
album_links = get_links('album', artist_soup)

for album_link in album_links:
    album_soup = get_html(album_link)
    album_tracklist = get_links('song', album_soup)
    store_lyrics(album_tracklist)