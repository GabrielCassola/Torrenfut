from django.shortcuts import render, redirect
from .forms import PersonForm
from django.contrib import messages

def cliente_cadastro(request):
    template_name = 'forms_cadastro.html'
    form = PersonForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return render(request, template_name, {'form': form})
        
    context = {'form': form}
    return render(request, template_name, context)