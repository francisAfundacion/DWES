from django.contrib import admin
from .models import UsuarioPersonalizado
from .models import Evento
from .models import Reserva
from .models import Comentario

admin.site.register(UsuarioPersonalizado)
admin.site.register(Evento)
admin.site.register(Reserva)
admin.site.register(Comentario)


# Register your models here.
