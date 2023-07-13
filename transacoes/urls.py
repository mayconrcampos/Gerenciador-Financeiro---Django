from django.urls import path
from .views import transacoes, entradas, saidas, balanco, insere_transacao, edita_transacao, deleta_transacao

urlpatterns = [
    path("transacoes/", transacoes, name="transacoes"),
    path("transacoes/entradas/", entradas, name="entradas"),
    path("transacoes/saidas/", saidas, name="saidas"),
    path("transacoes/balanco/", balanco, name="balanco"),
    path("insere/transacao/", insere_transacao, name="insere_transacao"),
    path("edita/transacao/", edita_transacao, name="edita_transacao"),
    path("deleta/transacao/", deleta_transacao, name="deleta_transacao"),
]