from django.contrib import admin
from .models import UsuarioPersonalizado
from .models import Evento
from .models import Reserva
from .models import Comentario

class EventoAdmin (admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha', 'usuario')
    search_fields = ('nombre', 'fecha')
    list_filter = ('fecha' ,)

admin.site.register(Evento,EventoAdmin)
admin.site.register(UsuarioPersonalizado)
admin.site.register(Reserva)
admin.site.register(Comentario)



# Register your models here.
