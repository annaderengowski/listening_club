from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class User(AbstractBaseUser, PermissionsMixin):
	pass

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(email, password, **kwargs)


class Album(models.Model):
	rank =  models.IntegerField()
	artist = models.CharField(max_length=500)
	album = models.CharField(max_length=500)
	year = models.IntegerField()
	blurb = models.CharField(max_length=2000)

	def __str__(self):
		return f'{self.album} - {self.artist}'
