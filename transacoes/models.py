from django.db import models
from usuarios.models import Usuario, Base
from categorias.models import Categoria

class TipoEscolha(models.IntegerChoices):
    OPCAO_1 = 1, 'Opção 1'
    OPCAO_2 = 2, 'Opção 2'

class Transacao(Base):
    tipo = models.IntegerField(choices=TipoEscolha.choices)
    descricao = models.CharField("Descrição", max_length=128, blank=False)
    valor = models.DecimalField("Valor", blank=False, decimal_places=2, max_digits=10)
    data = models.DateField("Data", blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    comentario = models.TextField("Comentário", max_length=256)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
    
    def __str__(self):
        return self.descricao
        