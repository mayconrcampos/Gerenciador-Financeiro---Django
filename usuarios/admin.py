from django.contrib import admin
from .models import Usuario

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # readonly_fields = ("nome", "email", "senha_cripto", "imagem", "facebook", "twitter", "instagram", "linkedin")
    list_display = ("nome", "email", "ativo")