from django.urls import path
from .views import inserir_categorias, listar_categorias, deletar_categoria, insere_categoria, edita_categoria

urlpatterns = [
    path("inserir/categorias/", inserir_categorias, name="inserir_categorias"),
    path("insere/categoria/", insere_categoria, name="insere_categoria"),
    path("edita/categoria/", edita_categoria, name="edita_categoria"),
    path("listar/categorias/", listar_categorias, name="listar_categorias"),
    path("deletar/categoria/<int:id>", deletar_categoria, name="deletar_categoria")
]