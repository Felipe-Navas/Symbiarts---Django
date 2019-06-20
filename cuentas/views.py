from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import FormRegistro


def signup(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('symbiarts_app:lista_obras')
    else:
        form = FormRegistro()
    return render(request, 'signup.html', {'form': form})
