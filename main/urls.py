from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.indexRender, name="Index"),
    path("", views.indexUserRender, name="index_user" ),
]
