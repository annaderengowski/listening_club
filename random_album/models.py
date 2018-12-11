from django.db import models

class Album(models.Model):
	rank =  models.IntegerField()
	artist = models.CharField(max_length=500)
	album = models.CharField(max_length=500)
	year = models.IntegerField()
	blurb = models.CharField(max_length=2000)

	#unique together artist/album?