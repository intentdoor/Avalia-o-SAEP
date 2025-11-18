from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/<int:produto_id>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:produto_id>/deletar/', views.deletar_produto, name='deletar_produto'),
    path('produtos/<int:produto_id>/movimentar/', views.registrar_movimentacao, name='registrar_movimentacao'),
    path('produtos/<int:produto_id>/historico/', views.historico_movimentacoes, name='historico_movimentacoes'),
]