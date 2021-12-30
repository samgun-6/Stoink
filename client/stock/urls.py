from django.conf.urls import url
from . import views
from django.urls import path
from django.conf.urls import *

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    url(r'^stock/$', views.stock, name='stock'),
    path('predict', views.predict, name='predict'),
    path('testFunc', views.testFunc, name='testFunc'),
    path('allstocks', views.allstocks, name='allstocks'),
    #path('setModel', views.setModel, name='setModel'),
    #path('getModel', views.getModel, name='getModel'),

]
