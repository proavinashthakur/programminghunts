from django.contrib.sitemaps import Sitemap
from .models import Posts
 
 
class PostSitemap(Sitemap): 
    def items(self):
        return Posts.objects.filter(published=True)
 
    def lastmod(self, obj):
        return obj.updated