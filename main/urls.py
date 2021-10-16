from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexRender, name="index")
]