from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import View

import re
import traceback
import random
from requests import get
from bs4 import BeautifulSoup

from random_album.models import Album

class AlbumListView(View):

	def get(self, request):
		context = {}
		context['album_list'] = Album.objects.all()
		return render(request, 'random_album/album_list.html', context)

class RandomAlbumView(View):

	def get(self, request):
		context = {}
		q = Album.objects.all()
		count = q.count()
		random_album = q[random.randint(1, count+1)]
		context['random_album'] = random_album
		return render(request, 'random_album/random.html', context)

	def post(self, request):
		pass


def index(request):
	context = {}

	return render(request, 'random_album/index.html', context)

