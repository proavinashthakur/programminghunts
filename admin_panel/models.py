from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.sites.models import Site


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar')


class Advertisement(models.Model):
	title = models.CharField(max_length=130)
	code = models.TextField()
	type = models.CharField(max_length=20)
	publish = models.BooleanField(default=True)