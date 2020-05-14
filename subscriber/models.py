from django.db import models

# Create your models here.

class Subscribers(models.Model):
	first_name = models.CharField(max_length=25, null=True)
	last_name = models.CharField(max_length=25, null=True)
	email = models.EmailField()
	is_verified = models.BooleanField(default=False)
	ip = models.CharField(max_length=45, null=True)
	city = models.CharField(max_length=30, null=True)
	country = models.CharField(max_length=30, null=True) 
	otp = models.CharField(max_length=50, null=True)
	created = models.DateTimeField(auto_now_add = True, null=True)



class Visitor(models.Model):
	ip = models.CharField(max_length=45, null=True)
	city = models.CharField(max_length=30, null=True)
	country = models.CharField(max_length=30, null=True) 
	url = models.CharField(max_length=255, null=True	)
	created = models.DateTimeField(auto_now_add = True, null=True)