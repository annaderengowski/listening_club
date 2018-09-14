from django.shortcuts import render
from django.utils.html import strip_tags

import re
from requests import get
from bs4 import BeautifulSoup

def index(request):
	#get_1990s_albums()
	

	return render(request, 'random_album/index.html', {})


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



