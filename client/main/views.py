from django.shortcuts import render


def home(request):
    return render(request, 'static/templates/home.html')
