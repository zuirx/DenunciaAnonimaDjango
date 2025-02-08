from django.urls import path
from . import views

urlpatterns = [
    path('', views.denuncia, name='denuncia'),
]