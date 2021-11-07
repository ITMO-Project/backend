from django.urls import path
from . import views

app_name = "decryption"

urlpatterns = [
    path("", views.decryptionRender, name="Decryption"),
    path("decrypted/", views.decryptedRender, name="Decrypted"),
    path("save/", views.saveToClientRender, name="Save")
]