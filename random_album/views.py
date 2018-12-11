from django.shortcuts import render
from django.utils.html import strip_tags

import re
import traceback
from requests import get
from bs4 import BeautifulSoup

from .models import Album


def index(request):
	#get_1990s_albums()
	
	urls = [
		'https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-1960s/',
		'https://pitchfork.com/features/lists-and-guides/5932-top-100-albums-of-the-1970s/',
		'https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-1980s/',
		'https://pitchfork.com/features/lists-and-guides/7710-the-top-200-albums-of-the-2000s-20-1/',
	]

	Album.objects.all().delete()

	# for url in urls:
	# 	album_dict = get_album_dict(url)
	# 	save_albums(album_dict)

	albums_1990s = get_1990s_albums()
	#save_albums(albums_1990s)

	return render(request, 'random_album/index.html', {})

def get_album_dict(base_url):
	# TODO: 
	# make these functions load into the database
	# turn these into management commands - class based
	# implement a different database
	albums = {}

	for x in range(1,11):
		if x == 1:
			url = base_url
		else:
			url = f'{base_url}?page={x}'

		response = get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		contents = soup.findAll('div', {'class': 'list-blurb blurb-container container-fluid'})

		for album in contents:
			rank = album.div.find('div', class_ = 'rank').text
			artist = album.a.text
			album_title = album.h2.text
			year = album.h3.text
			blurb = album.find('div', class_ = 'contents').p.text

			# One album doesn't have a rank for some reason ugh
			if not rank:
				rank = sorted(albums.keys())[0] - 1

			try:
				albums[int(rank)] = {
					'rank': int(rank),
					'artist': artist,
					'album': album_title,
					'year': int(year),
					'blurb': blurb
				}
			except:
				print(traceback.format_exc())

	return albums


def save_albums(album_dict):
	for album in album_dict.values():
		try:
			Album.objects.create(
				rank=album['rank'],
				album=album['album'],
				artist=album['artist'],
				year=album['year'],
				blurb=album['blurb']
				)
			print(f'saved {album["year"]} {album["album"]} - {album["artist"]}')
		except Exception as exc:
			print(album)
			print(exc)



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
				if len(label_and_year) == 3: #there's an ampersand messing stuff up
					label = f'{label_and_year[0]} {label_and_year[1]}'
					year = label_and_year[2]
					label_and_year = [label, year]
				label = label_and_year[0].replace("[", "") 
				year = label_and_year[1].replace("]", "")
			else:
				label = None
				year = None


			if rank and artist and album and year:
				try:
					albums[int(rank)] = {
					'rank': int(rank),
					'artist': artist,
					'album': album,
					'year': int(year)
					}
				except:
					print(f'ERROR***')
					print(label_year_search)
					print(label_and_year)
	return albums



