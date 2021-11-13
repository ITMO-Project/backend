from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def indexRender(request):
    return render(request, 'main/index.html')

def indexUserRender(request):
    return render(request, 'main/index_user.html')

