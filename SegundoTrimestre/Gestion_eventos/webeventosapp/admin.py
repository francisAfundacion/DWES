from django.contrib import admin
from .models import UsuarioPersonalizado
from .models import Evento
from .models import Reserva
from .models import Comentario

# Configuración personalizada de la administración del modelo Evento.
class EventoAdmin (admin.ModelAdmin):
    """
        Clase para configurar la apariencia y funcionalidad del modelo Evento
        en la interfaz de administración de Django.
        Se personaliza la lista de eventos que se muestran, los campos de búsqueda
        y los filtros disponibles para facilitar la gestión de eventos.

        Atributos:
        - list_display: Define los campos que se mostrarán en la vista de lista para cada objeto Evento.
        - search_fields: Define los campos que se usarán para buscar eventos en el panel de administración.
        - list_filter: Permite agregar filtros para refinar la visualización de los eventos.
        """

    list_display = ('nombre', 'descripcion', 'fecha', 'usuario')
    search_fields = ('nombre', 'fecha')
    list_filter = ('fecha' ,)

# Registro del modelo Evento con la configuración personalizada en la clase EventoAdmin
admin.site.register(Evento,EventoAdmin)

"""
    Registro de los modelos: 
    - UsuarioPersonalizado .
    - Reserva.
    - Comentario.
        -Emplea configuración predeterminada que usa django en el panel de adminstración.
"""
admin.site.register(UsuarioPersonalizado)
admin.site.register(Reserva)
admin.site.register(Comentario)




