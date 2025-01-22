from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#CRUD de eventos
def listar_eventos(request):
    ##limite = int(request)
    eventos = Evento.objects.all()
    lista_json_eventos = []
    for evento in eventos:
        json_evento = {}
        json_evento['nombre'] = evento.nombre
        json_evento['descripcion'] = evento.descripcion
        json_evento['fecha'] = evento.fecha
        json_evento['hora'] = evento.hora
        json_evento['max_asistencias'] = evento.max_asistencias
        json_evento['usuario'] = evento.usuario
        json_evento['url_img'] = evento.url_img
        lista_json_eventos.append(json_evento)
        print (lista_json_eventos)
    return JsonResponse(lista_json_eventos, safe=False)




#GET: Listar todos los eventos disponibles (filtros opcionales por título o fecha, ordenados y paginados con un límite de 5 elementos por página).
#POST: Crear un evento (solo organizadores).
#PUT/PATCH: Actualizar un evento (solo organizadores).
#DELETE: Eliminar un evento (solo organizadores).
