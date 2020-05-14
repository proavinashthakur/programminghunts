from django.urls import path
from . import views
urlpatterns = [
    path('subscriber-api', views.subscribe, name="subscriber-api"),
    path('activate/<str:token>', views.verify_email, name="verify-email"),

]

