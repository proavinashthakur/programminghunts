from django.shortcuts import render
from . models import Category, Tags, Posts, PostTags, PrivacyPolicy
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from subscriber.models import Visitor
from django.db.models import CharField, Value


def location(request):
    return render(request, 'blog/location.html')

def index(request):
    posts = Posts.objects.filter(published=True).order_by('-updated')[:4]
    categories = Category.objects.filter(featured=True)
    most_recent = Posts.objects.filter(published=True).order_by('-created')[:2]
    return render(request, 'blog/base.html', {"posts":posts, "categories":categories, "most_recent":most_recent})

def single(request, slug):
    if request.user.is_authenticated:
        post = Posts.objects.get(slug=slug)
    else:
        post = Posts.objects.get(slug=slug, published=True)
    
    tags = PostTags.objects.filter(post=post.pk)
    categories = Category.objects.filter(featured=True)
    try:
        prev = Posts.objects.get(id=post.prev)
    except:
        prev = None
    try:
        nxt = Posts.objects.get(id=post.nxt)
    except:
        nxt = None
    return render(request, 'blog/post.html', {"post":post, "tags":tags, 'base_url':settings.BASE_URL,
        "categories":categories, "prev":prev, "nxt":nxt})


def category_wise_posts(request, slug):
    category = Category.objects.filter(slug=slug)[0]
    category_id = category.id
    title = category.title
    tags_ids = Tags.objects.filter(category = category_id).values_list("id", flat=True)
    posts_id = PostTags.objects.filter(tag__in=tags_ids).values_list('post', flat=True)
    posts = Posts.objects.filter(id__in=posts_id, published=True).order_by('-created')
    categories = Category.objects.filter(featured=True)
    
    return render(request, 'blog/category_wise.html', {"posts":posts, "categories":categories,
        "title":title})

def privacy_policy(request):
    post = PrivacyPolicy.objects.all().annotate(title=Value('Privacy Policy - ProgrammingHunts', output_field=CharField()))[0]
    # post.annotate("title"="PrivacyPolicy")
    categories = Category.objects.filter(featured=True)
    return render(request, 'blog/privacy_policy.html', {"post":post, "categories":categories})  


def handler404(request, *args, **argv):
    posts = Posts.objects.filter(published=True).order_by('-updated')[:4]
    categories = Category.objects.filter(featured=True)
    response = render(request, 'blog/error.html', {"posts":posts, "categories":categories})                    
    response.status_code = 500
    return response


def handler500(request, *args, **argv):
    posts = Posts.objects.filter(published=True).order_by('-updated')[:4]
    categories = Category.objects.filter(featured=True)
    response = render(request, 'blog/error.html', {"posts":posts, "categories":categories})                    
    response.status_code = 500
    return response