from django import forms

DECADE_CHOICES = [
	('any', 'any decade'),
	('1960', 'the 1960s'),
	('1970', 'the 1970s'),
	('1980', 'the 1980s'),
	('1990', 'the 1990s'),
	('2000', 'the 2000s'),
	]

class RandomAlbumForm(forms.Form):
	decade = forms.ChoiceField(choices=DECADE_CHOICES)