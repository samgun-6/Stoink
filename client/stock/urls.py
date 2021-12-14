from django.conf.urls import url
from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    url(r'^stock/$', views.stock, name='stock'),
    path('predict', views.predict, name='predict'),
]
