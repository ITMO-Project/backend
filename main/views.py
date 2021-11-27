from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def indexRender(request):
    print(request.user.id)
    if int(request.user.id or 0) > 0:
        return render(request, 'main/index_user.html')
    return render(request, 'main/index.html')

def indexUserRender(request):
    if int(request.user.id or 0) > 0:
        return render(request, 'main/index_user.html')
    return render(request, 'main/index.html')

