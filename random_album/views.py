from django.shortcuts import render
from django.utils.html import strip_tags

import re
import traceback
from requests import get
from bs4 import BeautifulSoup

from .models import Album


def index(request):
	#TODO:
	# implement a different database
	# unit tests
	# generate a random album
	# class-based views
	# get blurbs for 90s albums
	context = {}

	return render(request, 'random_album/index.html', context)

	