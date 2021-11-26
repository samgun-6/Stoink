from django.http import HttpResponse


def stock(request):
    return HttpResponse("Hello, world. You're at the stocks index.")
