from django import forms
from .models import Produtos , Movimentacao

class ProdutoForm(forms.ModelForm ):
    class Meta:
        model = Produtos
        fields = ['nome', 'estoque_atual', 'estoque_min', 'peso', 'material']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 22 centimetros'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'estoque_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Em kg (opcional)', 'step': '0.01'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Aço, Plástico'}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['tipo_operacao', 'quantidade']
        widgets = {
            'tipo_operacao': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }
