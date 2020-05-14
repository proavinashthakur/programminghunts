from django.shortcuts import render
from . models import Category, Tags, Posts, PostTags
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.gis.geoip2 import GeoIP2
from subscriber.models import Visitor


def index(request):
    try:
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        Visitor.objects.create(ip=ip, city=city['city'], country=city['country_name'], url=request.path)
    except:
        pass
    posts = Posts.objects.filter(published=True).order_by('-created')[:4]
    categories = Category.objects.filter(featured=True)
    return render(request, 'blog/base.html', {"posts":posts, "categories":categories})

def single(request, slug):
    try:
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        Visitor.objects.create(ip=ip, city=city['city'], country=city['country_name'], url=request.path)
    except:
        pass
    post = Posts.objects.get(slug=slug)
    tags = PostTags.objects.filter(post=post.pk)
    categories = Category.objects.filter(featured=True)

    return render(request, 'blog/post.html', {"post":post, "tags":tags, 'base_url':settings.BASE_URL,
        "categories":categories})


def category_wise_posts(request, slug):
    try:
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
        Visitor.objects.create(ip=ip, city=city['city'], country=city['country_name'], url=request.path)
    except:
        pass
    category = Category.objects.filter(slug=slug)[0]
    category_id = category.id
    title = category.title
    tags_ids = Tags.objects.filter(category = category_id).values_list("id", flat=True)
    posts_id = PostTags.objects.filter(tag__in=tags_ids).values_list('post', flat=True)
    posts = Posts.objects.filter(id__in=posts_id, published=True).order_by('-created')
    categories = Category.objects.filter(featured=True)
    
    return render(request, 'blog/category_wise.html', {"posts":posts, "categories":categories,
        "title":title})


def handler404(request, *args, **argv):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html', {})                    
    response.status_code = 500
    return response