"""programminghunts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pro/', include('admin_panel.urls')),
    path('', include('subscriber.urls')),
    re_path(r'^admin/filebrowser/', site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'blog.views.handler404'
handler500 = 'blog.views.handler500'