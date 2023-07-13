from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import escape
from django.core.exceptions import ValidationError
from hashlib import sha256
from .models import Usuario

# Create your views here.
def index(request):
    return redirect("login")

def login(request):
    if "usuario" in request.session:
        return redirect("balanco")
    return render(request, "login.html")

def registrar(request):
    if "usuario" in request.session:
        return redirect("balanco")
    return render(request, "registrar.html")

def perfil(request):
    if not "usuario" in request.session:
        return redirect("login")
    
    usuario = Usuario.objects.filter(id=request.session['usuario']['id'])

    context = {
        "usuario": usuario
    }
    return render(request, "perfil.html", context)

# Controllers
def validar_registro(request):
    if request.method == "POST":
        nome = escape(request.POST.get("nome"))
        email = escape(request.POST.get("email"))
        senha = escape(request.POST.get("senha"))
        senha1 = escape(request.POST.get("senha1"))

        if not senha == senha1:
            messages.add_message(request, messages.ERROR, "As senhas não conferem")
            return redirect("registrar")

        try:
            usuario = Usuario(
                nome=nome,
                email=email,
                senha=senha
            )    
            usuario.save()
            
        except Exception as e:
            messages.error(request, "Erro ao tentar cadastrar usuário", e)
            return redirect("registrar")

        messages.add_message(request, messages.SUCCESS, "Usuário registrado com sucesso")
        return redirect("login")
        
def validar_login(request):
    if request.method == "POST":
        email = escape(request.POST.get("email"))
        senha = escape(request.POST.get("senha"))

        # Autenticação do usuário
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario.objects.filter(email=email).filter(senha_cripto=senha)

        if usuario.exists():
            usuario = usuario.first()
            if usuario.ativo:
                context = {
                    "usuario": usuario.nome,
                    "email": usuario.email,
                    "id": usuario.id
                }
                request.session['usuario'] = context
                messages.success(request, f"Seja bem vindo(a) {context['usuario']}! Você está logado como {context['email']}")
                return redirect("perfil")
            messages.error(request, "Usuário Inativo! Entre em contato com o Administrador")
            return redirect("login")
        messages.error(request, "Credencial inválida!")
    
    return redirect("login")

def atualiza_usuario(request):
    if request.method == "POST":
        twitter = request.POST.get('twitter')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        linkedin = request.POST.get('linkedin')

        print(twitter, facebook, instagram, linkedin)

        usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()

        try:
            usuario.twitter = twitter
            usuario.facebook = facebook
            usuario.instagram = instagram
            usuario.linkedin = linkedin
            usuario.save()

            messages.success(request, "Usuário atualizado com sucesso")
            return redirect("perfil")
        except Exception as e:
            messages.error(request, "Erro ao atualizar usuário")
            return redirect("perfil")
    return redirect("perfil")

def sair(request):
    messages.warning(request, "Você saiu do sistema")
    request.session.flush()
    return redirect("index")