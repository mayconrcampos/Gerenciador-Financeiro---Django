from django.shortcuts import render, redirect
from .models import Categoria, Usuario, TipoChoices
from django.contrib import messages


# Create your views here.
def inserir_categorias(request):
    if not "usuario" in request.session:
        return redirect("login")
    return render(request, "inserir_categorias.html")

def listar_categorias(request):
    if not "usuario" in request.session:
        return redirect("login")
    
    usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()    
    categorias = Categoria.objects.filter(usuario=usuario)
    if not categorias.exists():
        messages.error(request, "Não há nenhuma categoria cadastrada.")
        return render(request, "listar_categorias.html")

    context = {
        "categorias": categorias
    }
    return render(request, "listar_categorias.html", context)

# Controllers
def deletar_categoria(request, id):
    if request.method == 'GET':
        try:
            categoria = Categoria.objects.filter(id=id).first()
            categoria.delete()

            messages.success(request, "Categoria excluída com sucesso")
            return redirect("listar_categorias")
            
        except Exception as e:
            messages.error(request, "Erro ao excluir categoria")
            return redirect("listar_categorias")

    return redirect("listar_categorias")

def insere_categoria(request):
    if request.method == "POST":
        categoria = request.POST.get("categoria")
        tipo = request.POST.get("tipo")
        id_usuario = request.session["usuario"]['id']

        if len(categoria) == 0:
            messages.error(request, "Campo 'Categoria' deve ser preenchido")
            return redirect("inserir_categorias")

        try:
            usuario = Usuario.objects.filter(id=id_usuario).first()
            categoria = Categoria(
                tipo=TipoChoices.ENTRADA if tipo == '1' else TipoChoices.SAIDA,
                categoria=categoria,
                usuario=usuario              
            )
            categoria.save()
            messages.success(request, "Categoria inserida com sucesso")
            return redirect("listar_categorias")
        except Exception as e:
            messages.error(request, "Erro ao inserir categoria", e)

        return redirect("inserir_categorias")

def edita_categoria(request):
    if request.method == "POST":
        id = request.POST.get("id")
        cat = request.POST.get("categoria")
        tipo = request.POST.get("tipo")
        if len(cat) == 0:
            messages.error(request, "Campo 'Categoria' deve ser preenchido")
            return redirect("listar_categorias")

        try:
            categoria = Categoria.objects.filter(id=id).first()
            categoria.tipo = TipoChoices.ENTRADA if tipo == "1" else TipoChoices.SAIDA
            categoria.categoria = cat
            categoria.save()
            
            messages.success(request, "Categoria Atualizada com sucesso")
            return redirect("listar_categorias")
        except Exception as e:
            
            messages.error(request, "Erro ao Atualizar categoria", e)
        
        return redirect("listar_categorias")