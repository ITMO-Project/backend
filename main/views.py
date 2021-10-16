from django.shortcuts import render


def indexRender(request):
    return render(request, 'main/index.html')
