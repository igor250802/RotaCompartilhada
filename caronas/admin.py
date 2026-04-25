from django.contrib import admin
from .models import Usuario, Veiculo, Viagem, Parada, Reserva

admin.site.register(Usuario)
admin.site.register(Veiculo)
admin.site.register(Viagem)
admin.site.register(Parada)
admin.site.register(Reserva)