from django.db import models

# Create your models here.
from usuarios.models import Usuario

# Create your models here.
class TipoChoices(models.IntegerChoices):
    ENTRADA = 1, "Entrada"
    SAIDA = 2, "Saída"

class Categoria(models.Model):
    categoria = models.CharField("Categoria", max_length=32, blank=False)
    tipo = models.IntegerField("Tipo", choices=TipoChoices.choices, blank=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Categoria"
    
    def __str__(self):
        return self.categoria