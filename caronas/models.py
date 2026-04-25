from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Tabela de Usuários (RF01, RF02)
# Extendemos o AbstractUser para ganhar as funcionalidades de login do Django
class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Definimos o email como campo de login principal se desejar, 
    # mas por padrão o Django usa o 'username'.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return self.nome

# 2. Tabela de Veículos (Complemento ao RF03)
class Veiculo(models.Model):
    id_proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='veiculos')
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} ({self.placa})"

# 3. Tabela de Viagens (RF03)
class Viagem(models.Model):
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Em Curso', 'Em Curso'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ]

    id_motorista = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='viagens_dirigidas')
    id_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    vagas_totais = models.IntegerField()
    status_viagem = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Aberta')

    def __str__(self):
        return f"Viagem {self.id} - {self.data_hora}"

# 4. Tabela de Paradas (Itinerário)
class Parada(models.Model):
    id_viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='paradas')
    cidade = models.CharField(max_length=100)
    ordem_parada = models.IntegerField() # Ex: 1=Muzambinho, 2=Guaxupé

    class Meta:
        ordering = ['ordem_parada']

    def __str__(self):
        return f"{self.ordem_parada}º - {self.cidade}"

# 5. Tabela de Reservas (RF04, RF06, RF07)
class Reserva(models.Model):
    STATUS_RESERVA = [
        ('Pendente', 'Pendente'),
        ('Aceita', 'Aceita'),
        ('Recusada', 'Recusada'),
    ]

    id_viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='reservas')
    id_passageiro = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='minhas_reservas')
    id_parada_embarque = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name='embarques')
    id_parada_desembarque = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name='desembarques')
    quantidade_bagagem = models.IntegerField(default=0)
    status_solicitacao = models.CharField(max_length=10, choices=STATUS_RESERVA, default='Pendente')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva {self.id} - Passageiro: {self.id_passageiro.nome}"