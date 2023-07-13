from django.shortcuts import render, redirect
import re
from usuarios.models import Usuario
from categorias.models import Categoria, TipoChoices
from django.contrib import messages
from .models import Transacao, TipoEscolha
from datetime import datetime

# Services
def validar_valor_monetario(valor: str):
    try:
        valor = valor.replace(".", "")
        numero = float(valor.replace('R$', '').replace(',', '.').strip())
        if numero >= 0 and round(numero, 2) == numero:
            return numero
        else:
            return False
    except ValueError:
        return False


# Create your views here.
def transacoes(request):
    if not "usuario" in request.session:
        return redirect("index")
    usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()
    entradas = Categoria.objects.filter(tipo=TipoChoices.ENTRADA).filter(usuario=usuario)
    saidas = Categoria.objects.filter(tipo=TipoChoices.SAIDA).filter(usuario=usuario)

    context = {
        "entradas": entradas,
        "saidas": saidas
    }

    return render(request, "transacoes.html", context)

def entradas(request):
    if not "usuario" in request.session:
        return redirect("index")
    usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()
    entradas = Transacao.objects.filter(usuario=usuario).filter(tipo=TipoChoices.ENTRADA)
    categorias_entradas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.ENTRADA)
    categorias_saidas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.SAIDA)

    total = 0
    subtotal = []
    for entrada in entradas:
        total += entrada.valor
        subtotal.append(total)
    
    minha_lista = zip(entradas, subtotal)
    context = {
        "entradas": minha_lista,
        "total": total,
        "categorias_entradas": categorias_entradas,
        "categorias_saidas": categorias_saidas
    }
    return render(request, "entradas.html", context) 

def saidas(request):
    if not "usuario" in request.session:
        return redirect("index")
    usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()
    saidas = Transacao.objects.filter(usuario=usuario).filter(tipo=TipoChoices.SAIDA)
    categorias_entradas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.ENTRADA)
    categorias_saidas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.SAIDA)

    total = 0
    subtotal = []
    for saida in saidas:
        total += saida.valor
        subtotal.append(total)
    
    minha_lista = zip(saidas, subtotal)
    context = {
        "saidas": minha_lista,
        "total": total,
        "categorias_entradas": categorias_entradas,
        "categorias_saidas": categorias_saidas
    }
    return render(request, "saidas.html", context)

def balanco(request):
    if not "usuario" in request.session:
        return redirect("index")
    usuario = Usuario.objects.filter(id=request.session['usuario']['id']).first()
    balancos = Transacao.objects.filter(usuario=usuario)
    categorias_entradas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.ENTRADA)
    categorias_saidas = Categoria.objects.filter(usuario=usuario).filter(tipo=TipoChoices.SAIDA)


    if balancos.exists():
        total = 0
        subtotal = []
        for i in balancos:
            if i.tipo == 1:
                total += i.valor
            else:
                total -= i.valor
            
            subtotal.append(total)
        
        lista = zip(balancos, subtotal)

        context = {
            "transacoes": lista,
            "total": total,
            "categorias_entradas": categorias_entradas,
            "categorias_saidas": categorias_saidas

        }
        return render(request, "balanco.html", context)
    messages.error(request, "Não existem transações cadastradas")
    return render(request, "balanco.html", {"transacoes": []})

def insere_transacao(request):
    if not "usuario" in request.session:
        return redirect("index")
    
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        data = request.POST.get("data")
        id_categoria = request.POST.get("categoria")
        comentario = request.POST.get("comentario")
        comentario = str(comentario).strip()

        if not descricao:
            messages.error(request, "Campo 'Descrição' não pode estar vazio")
            return redirect("transacoes")
        
        if not validar_valor_monetario(valor):
            messages.error(request, "Valor monetário inválido.")
            return redirect("transacoes")
        
        valor = validar_valor_monetario(valor)
        categoria = Categoria.objects.filter(id=id_categoria).first()
        usuario = Usuario.objects.filter(id=request.session["usuario"]['id']).first()
        
        try:
            transacao = Transacao(
                tipo=TipoChoices.ENTRADA if tipo == "1" else TipoChoices.SAIDA,
                descricao=descricao,
                valor=valor,
                data=data,
                categoria=categoria,
                comentario=comentario,
                usuario=usuario
            )
            transacao.save()
            messages.success(request, "Transação cadastrada com sucesso")
            if tipo == '1':
                return redirect("entradas")
            return redirect("saidas")
            
        except Exception as e:
            messages.error(request, f"Erro ao inserir transação! {e}")
            return redirect("transacoes")

def edita_transacao(request):
    if not "usuario" in request.session:
        return redirect("index")
    
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        data = request.POST.get("data")
        comentario = request.POST.get("comentario")
        id_categoria = request.POST.get("categoria")
        id_transacao = request.POST.get("id_transacao")
        comentario = str(comentario).strip()

        if not descricao:
            messages.error(request, "Campo 'Descrição' não pode estar vazio")
            if tipo == "1":
                return redirect("entradas")
            return redirect("saidas")
        
        if not validar_valor_monetario(valor):
            messages.error(request, "Valor monetário inválido.")
            if tipo == "1":
                return redirect("entradas")
            return redirect("saidas")
        
        valor = validar_valor_monetario(valor)
        categoria = Categoria.objects.filter(id=id_categoria).first()
        # usuario = Usuario.objects.filter(id=request.session["usuario"]['id']).first()
        transacao = Transacao.objects.filter(id=id_transacao).first()
        try:
            transacao.tipo = TipoChoices.ENTRADA if tipo == "1" else TipoChoices.SAIDA
            transacao.descricao = descricao
            transacao.valor = valor
            transacao.data = data
            transacao.comentario = comentario
            transacao.categoria = categoria
            transacao.save()

            messages.success(request, "Transação atualizada com sucesso")
            

        except Exception as e:
            messages.error(request, "Erro ao atualizar transação")
                     
        
        if tipo == "1":
            return redirect("entradas")
        return redirect("saidas")

def deleta_transacao(request):
    if not "usuario" in request.session:
        return redirect("index")
    
    if request.method == "GET":
        id_transacao = request.GET.get("id_transacao")
        tipo = request.GET.get("tipo")
        
        transacao = Transacao.objects.filter(id=id_transacao)

        if transacao.exists():
            try:
                transacao = transacao.first()
                transacao.delete()

                messages.success(request, "Transação excluida com sucesso")
                
            except Exception as e:
                messages.error(request, "Erro ao excluir transação")

        print(request)
        if request.path == "/transacoes/balanco":
            return redirect("balanco")
        if tipo == "1":
            return redirect("entradas")
        return redirect("saidas")