from django.urls import path, include
from django.conf.urls import url
from . import views
#from django.contrib.auth.views import PasswordChangeView

app_name = "main"

urlpatterns = [
    path("", views.indexRender, name="Index"),
    path("", views.indexUserRender, name="index_user" ),
]
