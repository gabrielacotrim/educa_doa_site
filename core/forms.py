from django import forms
from .models import Necessidade
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email']

class NecessidadeForm(forms.ModelForm):
    class Meta:
        model = Necessidade
        fields = ['titulo', 'descricao', 'valor_meta', 'imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class DoacaoForm(forms.Form):
    valor = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)

class LoginForm(forms.Form):
    email_ou_identificador = forms.CharField(max_length=150, label="Email ou CPF/CNPJ")
    senha = forms.CharField(widget=forms.PasswordInput)
