from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm

# RF01 - Lógica de Cadastro
def cadastrar(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Loga automaticamente após cadastrar (RF02)
            return redirect('home') # Redireciona para a página inicial
    else:
        form = UsuarioCreationForm()
    return render(request, 'caronas/cadastro.html', {'form': form})

# Passo 5 - View da Home (Página Inicial)
# O decorador @login_required garante que apenas usuários autenticados acessem
@login_required
def home(request):
    return render(request, 'caronas/home.html')