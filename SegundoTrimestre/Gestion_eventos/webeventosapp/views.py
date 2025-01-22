from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.
#CRUD de eventos

def listar_eventos(request):
    ##limite = int(request)
    #eventos = Evento.objects.all()
    query_param_nombre = request.GET.get("nombre","")
    query_param_fecha = request.GET.get("fecha","")
    orden = request.GET.get("orden", "fecha")
    limite_pag = int(request.GET.get("limite", 5))
    n_pagina = int(request.GET.get("pagina", 1))

    if query_param_nombre != "":
        eventos = Evento.objects.filter(nombre__icontains= query_param_nombre).order_by(orden)
    else:
        if query_param_fecha != "":
            eventos = Evento.objects.filter(fecha__exact = query_param_fecha).order_by(orden)
        else:
            eventos = Evento.objects.all().order_by(orden)

    paginator = Paginator(eventos, limite_pag)  # Dividir productos en páginas de tamaño `limite`
    try:
        eventos_pagina = paginator.page(n_pagina)  # Obtener los productos de la página actual
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)  # Manejar errores de paginación

    lista_json_eventos = []
    for evento in eventos_pagina:
        json_evento = {}
        json_evento['nombre'] = evento.nombre
        json_evento['descripcion'] = evento.descripcion
        json_evento['fecha'] = evento.fecha
        json_evento['hora'] = evento.hora
        json_evento['max_asistencias'] = evento.max_asistencias
        json_evento['usuario'] = evento.usuario.username
        json_evento['url_img'] = evento.url_img
        lista_json_eventos.append(json_evento)

    data = {
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": n_pagina,
        "next": n_pagina + 1 if eventos_pagina.has_next() else None,
        "previous": n_pagina -1 if eventos_pagina.has_previous() else None,
        "results":  lista_json_eventos
    }

    return JsonResponse(data, safe=False)




#GET: Listar todos los eventos disponibles (filtros opcionales por título o fecha, ordenados y paginados con un límite de 5 elementos por página).
#POST: Crear un evento (solo organizadores).
#PUT/PATCH: Actualizar un evento (solo organizadores).
#DELETE: Eliminar un evento (solo organizadores).
