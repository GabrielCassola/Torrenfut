from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email') 
    search_fields = ('first_name', 'last_name', 'email')  