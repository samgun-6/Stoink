from django.http import HttpResponse
from django.shortcuts import render
from main.models import Main



#def stock(request):
  # return HttpResponse("You're at the stocks index.")

def stock(request):
    return render(request, 'front/stock.html')
