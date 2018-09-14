from django.shortcuts import render
from django.utils.html import strip_tags

import re
from requests import get
from bs4 import BeautifulSoup

def index(request):
	#get_1990s_albums()
	
	urls = [
		'https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-1960s/',
		'https://pitchfork.com/features/lists-and-guides/5932-top-100-albums-of-the-1970s/',
		'https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-1980s/',
		'https://pitchfork.com/features/lists-and-guides/7710-the-top-200-albums-of-the-2000s-20-1/',
	]

	get_album_dict()

	return render(request, 'random_album/index.html', {})

def get_album_dict():
	url = 'https://pitchfork.com/features/lists-and-guides/7710-the-top-200-albums-of-the-2000s-20-1/'
	response = get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	contents = soup.findAll('div', {'class': 'list-blurb blurb-container container-fluid'})

	albums = {}

	for album in contents:
		#album.h3.find('span', class_ = 'lister-item-year text-muted unbold')
		rank = album.div.find('div', class_ = 'rank').text
		artist = album.a.text
		album_title = album.h2.text
		year = album.h3.text
		blurb = album.find('div', class_ = 'contents').p.text

		albums[rank] = {
			'artist': artist,
			'album': album_title,
			'year': year,
			'blurb': blurb
		}

	print(albums)
	#print(contents[0].li.text)

def get_1990s_albums():
	url = 'https://pitchfork.com/features/lists-and-guides/5923-top-100-albums-of-the-1990s/'

	rank_list = []
	artist_list = []
	album_list = []
	label_list = []
	year_list = []
	blurb_list = []

	albums = {}

	rank_pattern = r"\d{3}:"
	artist_pattern = r": \w.*<br/>"
	album_pattern = r"<em>.+</em><br"
	label_year_pattern = r"\[.+; \d{4}\]"

	for page in range(1,11):
		# Get response for the right page
		if page == 1:
			response = get(url)
		else:
			response = get(f'{url}?page={page}')
		soup = BeautifulSoup(response.text, 'html.parser')
		contents = soup.find_all('p')

		for p in contents:
			rank_search = re.search(rank_pattern, str(p))
			if rank_search:
				rank = rank_search.group(0)[0:3]
			else:
				rank = None 

			artist_search = re.search(artist_pattern, str(p))
			if artist_search:
				artist = artist_search.group(0).replace(": ", "").replace("<br/>", "")
			else:
				artist = None

			album_search = re.search(album_pattern, str(p))
			if album_search:
				album = strip_tags(album_search.group(0).replace("<br", ""))
			else:
				album = None

			label_year_search = re.search(label_year_pattern, str(p))
			if label_year_search:
				label_and_year = label_year_search.group(0).split("; ")
				label = label_and_year[0].replace("[", "") 
				year = label_and_year[1].replace("]", "")
			else:
				label = None
				year = None

			if rank and artist and album and label and year:
				albums[rank] = {
					'artist': artist,
					'album': album,
					'label': label,
					'year': year
					}
	print(albums)



