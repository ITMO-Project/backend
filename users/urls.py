from django.conf.urls import include, url
from django.urls.conf import path
#from users.views import dashboard
from main.views import indexUserRender
from main.views import indexRender 
from users.views import register

from django.contrib.auth import views as auth_views 

urlpatterns = [
    #url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"accounts/", include("django.contrib.auth.urls")),
    #url(r"TEST/", indexUser, name="indexUser"),
    url(r"register/", register, name="register"),
]

urlpatterns += [
    path(r"User/", indexUserRender, name="index_user"),
    path("", indexRender, name="Index"),      
]



