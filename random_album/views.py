from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import View

import re
import traceback
import random
from requests import get
from bs4 import BeautifulSoup

from random_album.models import Album
from random_album.forms import RandomAlbumForm

class AlbumListView(View):

	def get(self, request):
		context = {}
		context['album_list'] = Album.objects.all()
		return render(request, 'random_album/album_list.html', context)

class RandomAlbumView(View):

	def get(self, request):
		form = RandomAlbumForm()
		return render(request, 'random_album/random_form.html', {'form': form})

	def post(self, request):
		context = {}
		form = RandomAlbumForm(request.POST)
		if form.is_valid():
			# Filter queryset by chosen decade
			decade = form.cleaned_data['decade']
			if decade == 'any':
				q = Album.objects.all()
			else:
				start_year = int(decade)
				end_year = start_year + 9
				q = Album.objects.filter(year__gte=start_year,
										 year__lte=end_year)

			# Select a random ID from the queryset
			count = q.count()
			random_album = q[random.randint(1, count+1)]
			context['random_album'] = random_album

			return render(request,
				'random_album/random.html',
				{'album': random_album})
		else:
			pass
			#TODO Send to error page


def index(request):
	context = {}

	return render(request, 'random_album/index.html', context)
