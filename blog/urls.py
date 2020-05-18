from django.urls import path
from django.conf.urls import url
from . import views
from .sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
	path('', views.index, name="index"),
	path('tutorial/<str:slug>', views.single, name="single-post"),
	path('category/<str:slug>', views.category_wise_posts, name="category-wise"),
	path('privacy-policy', views.privacy_policy, name="privacy-policy"),
]