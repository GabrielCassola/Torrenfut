from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("cpf", "nome", "email")

admin.site.register(Cliente, ClienteAdmin)
