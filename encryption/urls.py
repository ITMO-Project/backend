from django.urls import path
from . import views

app_name = "encryption"

urlpatterns = [
    path("", views.encryptionRender, name="Encryption"),
    path("image/", views.encryptionImageRender, name="EncryptionImage"),
    path("encrypted/", views.finishEncrypt, name="Encrypted"),
]