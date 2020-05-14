from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from admin_panel.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from blog.models import Category, Tags, Posts, PostTags
from django.contrib.sites.models import Site
from .serializers import CategorySerializer, TagSerializer, PostTagSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from blog.forms import PostForm
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            messages.success(request, "Logged In Successfully.")
            login(request, user)
            return redirect('/pro/')
        messages.error(request, "Sorry, Wrong Credentials.")
        return render(request, 'admin_panel/login.html', {})
    return render(request, 'admin_panel/login.html', {})


def signout(request):
    logout(request)
    return redirect('/pro/')

# profile
@login_required(login_url="/login")
def profile(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        avatar = request.FILES.get('avatar')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        if avatar:
            user.avatar = avatar
        user.save()
        messages.success(request, "Profile Updated")
        return redirect('profile')
    return render(request, 'admin_panel/profile.html', {})


@login_required(login_url="/pro/login")
def change_password(request):
    user_id = int(request.user.id)
    if request.method == "POST":
        current_pass = request.POST.get('password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        user = User.objects.get(id=user_id)
        user_pass = user.password
        correct_pass = check_password(current_pass, user_pass)
        if correct_pass:
            if new_pass != confirm_pass:
                messages.error(request, "New password and Confirm Password does not matched")
                return redirect('profile')
            if len(confirm_pass)<8:
                messages.error(request, "Password length must be greater of equals to 8 characters")
                return redirect('/')
            try:
                user.set_password(confirm_pass)
                user.save()
                messages.success(request, "Password changed, please login again")
                logout(request)
                return redirect('/pro/')
            except:
                messages.error(request, "Something went wrong")
                return redirect('profile')
        messages.error(request, "Sorry, you have entered wrong password.")
        return redirect('profile')
    else:
        messages.error(request, "Wrong request")
        return redirect('profile')    




from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# index/dashboard page when user is logged in
@login_required(login_url="/pro/login")
def dashboard(request):
    # total_shipments = Shipments.objects.count()
    # customers = Shipments.objects.values('email').distinct().count()
    return render(request, 'admin_panel/base.html', {})

# all posts listing
@login_required(login_url="/pro/login")
def posts_listing(request):
    posts = Posts.objects.all()
    return render(request, 'admin_panel/posts_table.html', {"posts":posts})

# index/dashboard page when user is logged in
@login_required(login_url="/pro/login")
def write_blog_post(request):
    # total_shipments = Shipments.objects.count()
    # customers = Shipments.objects.values('email').distinct().count()
    form = PostForm()
    return render(request, 'admin_panel/write_blog_post.html', {"form":form})

# index/dashboard page when user is logged in
@login_required(login_url="/pro/login")
def category_tags(request):
    # total_shipments = Shipments.objects.count()
    # customers = Shipments.objects.values('email').distinct().count()
    categories = Category.objects.all()
    categories_tags = list()
    for category in categories:
        data=dict()
        data['title']=category.title
        data['id']=category.id
        data['thumbnail']=category.thumbnail
        data['featured']=category.featured
        tags = Tags.objects.filter(category=category.id)
        tag_data=list()
        for tag in tags:
            tag_dict = dict()
            tag_dict['id'] = tag.id
            tag_dict['title'] = tag.title
            tag_dict['thumbnail'] = tag.thumbnail
            tag_data.append(tag_dict)
        data['tags']=tag_data
        data['tag_length'] = len(tags)
        categories_tags.append(data)

    return render(request, 'admin_panel/category_tags.html', {"categories":categories,
                                                    "categories_tags":categories_tags, "base_url":settings.BASE_URL})


# index/dashboard page when user is logged in
@login_required(login_url="/pro/login")
def add_category(request):
    title = request.POST.get('title')
    thumbnail = request.FILES.get('thumbnail')
    try:
        messages.success(request, "Category created")
        Category.objects.create(title=title, thumbnail=thumbnail)
        return redirect("category-and-tags")
    except:
        messages.error(request, "Failed to create new category")
        return redirect("category-and-tags")

@api_view(['GET',])
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category)
        return Response({"status":True, "data":serializer.data})
    except:
        return Response({"status":Fals, "msg":"No data found"})

@api_view(['GET',])
def get_tag(request, id):
    try:
        tag = Tags.objects.get(id=id)
        serializer = TagSerializer(tag)
        return Response({"status":True, "data":serializer.data})
    except:
        return Response({"status":False, "msg":"No data found"})

# index/dashboard page when user is logged in
@login_required(login_url="/pro/login")
def add_tag(request):
    category_id = request.POST.get('category')
    title = request.POST.get('title')
    thumbnail = request.FILES.get('thumbnail')
    try:
        category = Category.objects.get(id=category_id)
        Tags.objects.create(category=category, title=title, thumbnail=thumbnail)
        messages.success(request, "Tag created")
        return redirect("category-and-tags")
    except:
        messages.error(request, "Failed to create new tag")
        return redirect("category-and-tags")

@login_required(login_url="/pro/login")
def update_category(request):
    try:
        category_id = request.POST.get('cat_id')
        title = request.POST.get('title')
        thumbnail = request.FILES.get('thumbnail')
        category = Category.objects.get(id=category_id)
        category.title = title
        if thumbnail:
            category.thumbnail = thumbnail
        category.save()
        messages.success(request, "Category updated")
        return redirect("category-and-tags")
    except:
        return redirect("category-and-tags")

@login_required(login_url="/pro/login")
def update_tag(request):
    try:
        tag_id = request.POST.get('tag_id')
        title = request.POST.get('title')
        thumbnail = request.FILES.get('tag-thumbnail')
        tag = Tags.objects.get(id=tag_id)
        tag.title = title
        if thumbnail:
            tag.thumbnail = thumbnail
        tag.save()
        messages.success(request, "Tag updated")
        return redirect("category-and-tags")
    except:
        return redirect("category-and-tags")


@login_required(login_url="/pro/login")
def delete_category(request, id):
    try:
        tag = Category.objects.get(id=id).delete()
        messages.success(request, "Category deleted")
        return redirect("category-and-tags")
    except:
        messages.error(request, "Unable to delete Category")
        return redirect("category-and-tags")

@login_required(login_url="/pro/login")
def delete_tag(request, id):
    try:
        tag = Tags.objects.get(id=id).delete()
        messages.success(request, "Tag deleted")
        return redirect("category-and-tags")
    except:
        messages.error(request, "Unable to delete tag")
        return redirect("category-and-tags")


@api_view(['GET',])
def get_all_tags(request):
    try:
        tags = Tags.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response({"status":True, "data":serializer.data})
    except:
        return Response({"status":False, "msg":"No data found"})


@login_required(login_url="/pro/login")
def add_post(request):
    # try:
    data = request.POST
    title = data.get("title")
    slug = data.get("slug")
    meta_desc = data.get("meta-desc")
    meta_keywords = data.get("meta-keywords")
    thumbnail = request.FILES.get('thumbnail')
    blog_post = data.get("content")
    post = Posts.objects.create(title=title, slug=slug, meta_desc=meta_desc, 
        meta_keywords=meta_keywords, thumbnail=thumbnail, post=blog_post)
    tags = data.getlist("tags[]")
    for item in tags:
        tag = Tags.objects.get(id=item)
        post_tag = PostTags.objects.create(tag=tag, post=post)
        # post_tag.tag = tag.pk
        # post_tag.post = post.pk
        # post_tag.save()
    messages.success(request, "Post saved")
    return redirect("all-posts")
    # except:
    #     messages.error(request, "Unable to save post")
    #     return redirect("all-posts")

@api_view(['GET',])
def get_tag(request, id):
    try:
        tag = Tags.objects.get(id=id)
        serializer = TagSerializer(tag)
        return Response({"status":True, "data":serializer.data})
    except:
        return Response({"status":False, "msg":"No data found"})


@login_required(login_url="/pro/login")
def change_publish_status(request, id):
    try:
        post = Posts.objects.get(id=id)
        status = post.published
        if status == True:
            post.published = False
        elif status == False:
            post.published = True
        post.save()
        return JsonResponse({"status":True, "data":Posts.objects.get(id=id).published})
    except:
        return JsonResponse({"status":False, "data":Posts.objects.get(id=id).published})


@login_required(login_url="/pro/login")
def get_post_data(request, id):
    post = Posts.objects.get(id=id)
    tags = PostTags.objects.filter(post=post.pk)
    tag_list = PostTags.objects.filter(post=id).values_list('tag_id', flat=True)
    print(tag_list)
    if request.method =="POST":
        data = request.POST
        post.title = data.get("title")
        post.slug = data.get("slug")
        post.meta_desc = data.get("meta-desc")
        post.meta_keywords = data.get("meta-keywords")
        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES.get('thumbnail')
        post.post = data.get("content")
        tags_str = data.getlist("tags[]")
        tags = set()
        for item in tags_str:
            tags.add(int(item))

        tag_list = PostTags.objects.filter(post=id).values_list('tag_id', flat=True)
        item_to_remove = set(tag_list)
        for item in tags:
            try:
                if item in tag_list:
                    item_to_remove.remove(item)
                else:
                    tag = Tags.objects.get(id=item)
                    post_tag = PostTags.objects.create(tag=tag, post=post)
                    post_tag.tag = tag.pk
                    post_tag.post = post.pk
                    post_tag.save()
                    item_to_remove.remove(item)
            except:
                pass
        for item in item_to_remove:
            try:
                PostTags.objects.filter(tag=item, post=post.pk)[0].delete()
            except:
                pass
        post.save()
        messages.success(request, "Post saved")
        return redirect("all-posts")
    form = PostForm(initial={'content': post.post})
    return render(request, 'admin_panel/update_post.html', {"form":form, "post":post, "tags":tags, "base_url":settings.BASE_URL})


@login_required(login_url="/pro/login")
def delete_post(request, id):
    post = Posts.objects.get(id=id)
    tags = PostTags.objects.filter(post=post.pk)
    for tag in tags:
        tag.delete()
    post.delete()
    return redirect('all-posts')

@login_required(login_url="/pro/login")
def is_slug_available(request, slug):
    try:
        try:
            is_exists = Posts.objects.get(slug=slug)
            is_exists = True
        except:
            is_exists= False
        if is_exists:
            return JsonResponse({"status":True})
        else:
            return JsonResponse({"status":False})
    except:
        return JsonResponse({"status":False, "msg":"Something went wrong"})

@api_view(['GET',])
def get_post_tags(request, post_id):
    try:
        tags = PostTags.objects.filter(post=post_id)
        tag = list()
        for item in tags:
            tag.append(str(item.tag_id))

        serializer = PostTagSerializer(tags, many=True)
        return Response({"status":True, "data":tag})
    except:
        return Response({"status":False, "msg":"Something went wrong"})

@login_required(login_url="/pro/login")
def change_featured_category_status(request, id):
    try:
        category = Category.objects.get(id=id)
        status = category.featured
        if status == True:
            category.featured = False
        elif status == False:
            category.featured = True
        category.save()
        return JsonResponse({"status":True, "data":Category.objects.get(id=id).featured})
    except:
        return JsonResponse({"status":False, "data":Category.objects.get(id=id).featured})
