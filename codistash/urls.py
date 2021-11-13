from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('main.urls')),
    path("encryption/", include('encryption.urls')),
    path("decryption/", include('decryption.urls')),
    path("", include('users.urls')),
]
