from django.shortcuts import render


def encryptionRender(request):
    return render(request, 'encryption/encryption.html')

def encryptionImageRender(request):
    return render(request, 'encryption/encryption_image.html')

def encryptedRender(request):
    return render(request, 'encryption/encrypted.html')