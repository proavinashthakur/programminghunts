from django.db import models
from django.template.defaultfilters import slugify
from tinymce import HTMLField


class Category(models.Model):
	title = models.CharField(max_length=50)
	thumbnail = models.ImageField(upload_to="category-thumbnail", blank=True, null=True)
	featured = models.BooleanField(default=False)
	slug = models.SlugField(max_length = 250, null = True, blank = True)

	def save(self, *args, **kwargs):
		if not self.id:
		# Newly created object, so set slug
			self.slug = slugify(self.title)
		super(Category, self).save(*args, **kwargs)

class Tags(models.Model):
	category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="category")
	title = models.CharField(max_length=40)
	thumbnail = models.ImageField(upload_to="tags-thumbnail", blank=True, null=True)


class Posts(models.Model):
	title = models.CharField(max_length=60)
	meta_desc = models.CharField(max_length=130)
	meta_keywords = models.CharField(max_length=255)
	post = HTMLField('Content')
	thumbnail = models.ImageField(upload_to="post-thumbnail", blank=True, null=True)
	slug = models.SlugField(max_length = 250, null = True, blank = True)
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add=True)
	published = models.BooleanField(default=False) 

	def get_absolute_url(self):
		return '/'+self.slug


class PostTags(models.Model):
	tag = models.ForeignKey(Tags, on_delete=models.CASCADE, default=None, null=True, related_name="tag")
	post = models.ForeignKey(Posts, on_delete=models.CASCADE, default=None, null=True)

