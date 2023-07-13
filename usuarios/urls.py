from django.urls import path
from .views import index, login, registrar, perfil, validar_registro, validar_login, sair, atualiza_usuario

urlpatterns = [
    path("", index, name="index"),
    path("auth/login/", login, name="login"),
    path("auth/registrar/", registrar, name="registrar"),
    path("usuario/perfil/", perfil, name="perfil"),
    path("registra/usuario/", validar_registro, name="validar_registro"),
    path("login/usuario/", validar_login, name="validar_login"),
    path("atualiza/usuario", atualiza_usuario, name="atualiza_usuario"),
    path("sair/usuario/", sair, name="sair")
]