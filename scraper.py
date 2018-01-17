import requests
import re
import csv

from bs4 import BeautifulSoup

data = []
pages = ['http://www.bimba.co.za/zavijah/satanic-faith']

for pg in pages:
    page = requests.get(pg)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    list(html.children)
    body = list(html.children)[3]
    list(body.children)

    title_section = list(body.children)[5]
    # print(title_section.prettify())

    #regex for album
    album = re.compile("feat_label")

    # Find next sibling
    # def album_for_song(tag):
    #     test = tag.find_all('label', album)
    #     return test

    find_album_name = title_section.find('label', album)
    title = body.find('h1', class_='page-header')

    # Find the artist wrapped with <label> tag Artist
    find_artist_string = title_section.find(string=re.compile("Artist"))
    # Find the artist wrapped with <label> tag Album
    find_album_string = title_section.find(string=re.compile("Album"))
    # Find the artist wrapped with <label> tag Album
    find_featured_string = title_section.find(string=re.compile("Featuring"))

    # print the featured string

    # If find_featured_string is empty return empty string
    if not find_featured_string:
        featured = ""
        # find the featured tag
        # check if it's wrapped in an a tag
    elif find_featured_string.find_parent("p").find_all('a'):

        # if the string does not contain an <a>
        # tag then find the string without a wrapper
        featured = find_featured_string.find_parent("p").find_all('a')[0].get_text()

    else:
        featured = find_featured_string.find_parent("p").get_text('',strip=True)

    # If find_featured_string is empty return empty string
    if not find_artist_string:
        artist = ""

    elif find_artist_string.find_parent("p").find_all('a'):
        # find the artist tag
        # check if it's wrapped in an a tag
        # if the string does not contain an <a>
        # tag then find the string without a wrapper
        artist = find_artist_string.find_parent("p").find_all('a')[0].get_text()
    else:
        # for section_artist in title_section.find_all('label'):
        #     textest = section_artist.next_sibling
        #     print(textest)
        artist = find_artist_string.find_parent("p").get_text('',strip=True)

    # If find_featured_string is empty return empty string
    if not find_album_string:
        album = ""
    # print the album string
    elif find_album_string.find_parent("p").find_all('a'):
        # find the artist tag
        # check if it's wrapped in an a tag
        # if the string does not contain an <a>
        # tag then find the string without a wrapper
        album = find_album_string.find_parent("p").find_all('a')[0].get_text()
    else:
        album = find_album_string.find_parent("p").get_text('',strip=True)

    lyrics_body = body.find(property="content:encoded")
    title = title.get_text() + " Lyrics"
    lyrics = lyrics_body.prettify()

    # Print all the fields for the page
    data.append((title, artist, featured, album, lyrics))

    # open a csv file with append, so old data will not be erased
with open('index.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    # The for loop
    for title, artist, featured, album, lyrics in data:
        writer.writerow([title, artist, featured, album, lyrics])


