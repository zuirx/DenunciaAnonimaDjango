from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Denuncia
from .forms import DenunciaForm
import socket


def denuncia(request):

    denuncias = Denuncia.objects.all()

    if request.method == 'POST':
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.user_ip = request.META.get('REMOTE_ADDR', None)
            denuncia.save()
            return redirect('denuncia')
    else:
        form = DenunciaForm()

    return render(request, 'denuncia/base.html', {
        'denuncias' : denuncias,
        'form': form
    })
