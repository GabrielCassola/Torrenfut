from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ClienteRegistrationForm, EditarPerfilForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente

# View de cadastro de cliente
from django.shortcuts import render, redirect
from .forms import ClienteRegistrationForm
from django.contrib import messages

def cliente_registro(request):
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criar um cliente associado ao usuário
            Cliente.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email')
            )
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('login')  # Redireciona para a página de login
    else:
        form = ClienteRegistrationForm()
    return render(request, 'forms_cadastro.html', {'form': form})


# View de login
def cliente_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')  # Redireciona ao perfil do cliente
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
    return render(request, 'forms_login.html')

def logout_cliente(request):
    logout(request)  # Faz o logout do usuário
    return redirect('login')  # Redireciona para a página de login após o logout

@login_required
def perfil_cliente(request):
    return render(request, 'perfil.html')  # Renderiza um template de perfil


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('perfil')  
    else:
        form = EditarPerfilForm(instance=request.user)
    
    return render(request, 'editar_perfil.html', {'form': form})