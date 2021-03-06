from django.db import models

class Album(models.Model):
	rank =  models.IntegerField()
	artist = models.CharField(max_length=500)
	album = models.CharField(max_length=500)
	year = models.IntegerField()
	blurb = models.CharField(max_length=2000)

	def __str__(self):
		return f'{self.album} - {self.artist}'