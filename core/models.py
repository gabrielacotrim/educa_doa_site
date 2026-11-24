from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    is_doador = models.BooleanField(default=False)
    is_escola = models.BooleanField(default=False)

class Doador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

class Escola(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cnpj = models.CharField(max_length=18, unique=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    nome_escola = models.CharField(max_length=200)

    def __str__(self):
        return self.nome_escola

class Necessidade(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='necessidades')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_arrecadado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    imagem = models.ImageField(upload_to='necessidades/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    @property
    def percentual_arrecadado(self):
        if self.valor_meta > 0:
            return min(int((self.valor_arrecadado / self.valor_meta) * 100), 100)
        return 0

class Doacao(models.Model):
    doador = models.ForeignKey(Doador, on_delete=models.SET_NULL, null=True, related_name='doacoes')
    necessidade = models.ForeignKey(Necessidade, on_delete=models.CASCADE, related_name='doacoes')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_doacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.doador} doou R${self.valor} para {self.necessidade}'

