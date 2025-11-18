# from django.shortcuts import render , redirect , get_object_or_404
# from django.db import transaction, models
# from django.contrib.auth.decorators import login_required
# from .models import Produtos , Movimentacao
# from .forms import MovimentacaoForm

# @login_required
# def lista_produtos(request):
#     produtos = Produtos.objects.all().order_by('nome')

#     produtos_em_alerta = Produtos.objects.filter(
#         estoque_atual__lte=models.F('estoque_min')
#     )

#     context = {
#         'produtos': produtos,
#         'produtos_em_alerta': produtos_em_alerta,
#     }
#     return render(request, 'estoque/lista.html', context)


# @login_required
# def registrar_movimentacao(request, produto_id):
#     produto = get_object_or_404(Produtos, pk=produto_id)

#     if request.method == 'POST':
#         form = MovimentacaoForm(request.POST)
#         if form.is_valid():
#             movimentacao = form.save(commit=False)
#             movimentacao.produto = produto
#             movimentacao.responsavel = request.user 

#             quantidade = movimentacao.quantidade
#             tipo = movimentacao.tipo_operacao

#             with transaction.atomic():
#                 if tipo == 'ENTRADA':
#                     produto.estoque_atual += quantidade
#                 elif tipo == 'SAIDA':
#                     if produto.estoque_atual < quantidade:
#                         return render(request, 'estoque/registrar_movimentacao.html', {
#                             'form': form,
#                             'produto': produto,
#                             'erro': 'Estoque insuficiente para esta saída'
#                         })
#                     produto.estoque_atual -= quantidade

#                 produto.save()
#                 movimentacao.save()

#             return redirect('lista_produtos')

#     else:
#         form = MovimentacaoForm()

#     return render(request, 'estoque/registrar_movimentacao.html', {
#         'form': form,
#         'produto': produto
#     })


# @login_required
# def historico_movimentacoes(request, produto_id):
#     produto = get_object_or_404(Produtos, pk=produto_id)
#     movimentacoes = Movimentacao.objects.filter(
#         produto=produto
#     ).order_by('-data_movimentacao')

#     context = {
#         'produto': produto,
#         'movimentacoes': movimentacoes,
#     }
#     return render(request, 'estoque/historico_movimentacoes.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Produtos, Movimentacao
from .forms import ProdutoForm, MovimentacaoForm

@login_required
def dashboard(request):
    """Página inicial com resumo do estoque"""
    produtos = Produtos.objects.all()
    produtos_em_alerta = [p for p in produtos if p.estoque_atual <= p.estoque_min]
    total_produtos = produtos.count()
    
    context = {
        'total_produtos': total_produtos,
        'produtos_em_alerta': produtos_em_alerta,
        'quantidade_alertas': len(produtos_em_alerta),
    }
    return render(request, 'estoque/dashboard.html', context)

@login_required
def lista_produtos(request):
    """Lista todos os produtos"""
    produtos = Produtos.objects.all().order_by('nome')
    produtos_em_alerta = [p for p in produtos if p.estoque_atual <= p.estoque_min]

    context = {
        'produtos': produtos,
        'produtos_em_alerta': produtos_em_alerta,
    }
    return render(request, 'estoque/lista.html', context)

@login_required
def cadastrar_produto(request):
    """Cadastrar novo produto"""
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()

    return render(request, 'estoque/cadastrar_produto.html', {'form': form})

@login_required
def editar_produto(request, produto_id):
    """Editar um produto existente"""
    produto = get_object_or_404(Produtos, pk=produto_id)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'estoque/editar_produto.html', {'form': form, 'produto': produto})

@login_required
def deletar_produto(request, produto_id):
    """Deletar um produto"""
    produto = get_object_or_404(Produtos, pk=produto_id)

    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto deletado com sucesso!')
        return redirect('lista_produtos')

    return render(request, 'estoque/deletar_produto.html', {'produto': produto})

@login_required
def registrar_movimentacao(request, produto_id):
    """Registrar entrada ou saída de um produto"""
    produto = get_object_or_404(Produtos, pk=produto_id)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.produto = produto
            movimentacao.responsavel = request.user

            quantidade = movimentacao.quantidade
            tipo = movimentacao.tipo_operacao

            # Validar estoque antes de fazer a saída
            if tipo == 'SAIDA' and produto.estoque_atual < quantidade:
                messages.error(request, f'Estoque insuficiente! Disponível: {produto.estoque_atual}')
                return render(request, 'estoque/registrar_movimentacao.html', {'form': form, 'produto': produto})

            # Atualizar estoque de forma segura
            with transaction.atomic():
                if tipo == 'ENTRADA':
                    produto.estoque_atual += quantidade
                elif tipo == 'SAIDA':
                    produto.estoque_atual -= quantidade

                produto.save()
                movimentacao.save()

            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('lista_produtos')
    else:
        form = MovimentacaoForm()

    return render(request, 'estoque/registrar_movimentacao.html', {'form': form, 'produto': produto})

@login_required
def historico_movimentacoes(request, produto_id):
    """Ver histórico de movimentações de um produto"""
    produto = get_object_or_404(Produtos, pk=produto_id)
    movimentacoes = Movimentacao.objects.filter(produto=produto).order_by('-data_movimentacao')

    context = {
        'produto': produto,
        'movimentacoes': movimentacoes,
    }
    return render(request, 'estoque/historico_movimentacoes.html', context)
