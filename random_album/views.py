from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import View

import re
import traceback
from requests import get
from bs4 import BeautifulSoup

from random_album.models import Album

class AlbumListView(View):

	def get(self, request):
		template_name = 'album_list.html'
		context = {}
		context['album_list'] = Album.objects.all()
		return render(request, 'random_album/album_list.html', context)


def index(request):
	context = {}

	return render(request, 'random_album/index.html', context)

