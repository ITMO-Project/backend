from django.shortcuts import render


def decryptionRender(request):
    return render(request, 'decryption/decryption.html')

def decryptedRender(request):
    return render(request, 'decryption/decrypted.html')
