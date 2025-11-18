
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Produtos(models.Model):
    nome = models.CharField(max_length=60)
    tamanho = models.TextField(max_length=60)
    material = models.TextField(max_length=50)
    peso = models.FloatField()
    estoque_atual = models.IntegerField(default=0)
    estoque_min = models.IntegerField(default=10)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA','entrada'),
        ('SAIDA','saida')
    ]

    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    tipo_operacao = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)

    def __str__ (self):
        return f"{self.tipo_operacao} de {self.quantidade} de {self.produto.nome}"