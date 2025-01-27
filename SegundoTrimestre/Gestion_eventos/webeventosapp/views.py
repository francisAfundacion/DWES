from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento, UsuarioPersonalizado
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from datetime import datetime
import json

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

@csrf_exempt
def crear_evento(request):
    diccionario_nuevo_evento = json.loads(request.body)
    print(diccionario_nuevo_evento)
    ##query_param_organizador = request.POST.get("tipo_usuario", "")
    tipo_usuario = diccionario_nuevo_evento['tipo_usuario']
    print("LLEGO A VISUALIZAR TIPO_USUARIO")
    print(tipo_usuario)
    if request.method == "POST" and tipo_usuario == "organizador":
        nombre_usuario_post = diccionario_nuevo_evento["usuario"]
        print(nombre_usuario_post)
        #consulta_usuario_post = UsuarioPersonalizado.objects.filter(username = nombre_usuario_post), me da query set y no una instancia del modelo
        consulta_usuario_post = UsuarioPersonalizado.objects.get(username = nombre_usuario_post)
        print("VISUALIZO CONSULTA USUARIO")
        print(consulta_usuario_post)
        Evento.objects.create (
        nombre =diccionario_nuevo_evento["nombre"],
        descripcion = diccionario_nuevo_evento["descripcion"],
        fecha = diccionario_nuevo_evento["fecha"],
        hora = diccionario_nuevo_evento["hora"],
        max_asistencias = diccionario_nuevo_evento["max_asistencias"],
        usuario = consulta_usuario_post,
        url_img = diccionario_nuevo_evento["url_img"]
        )
    return JsonResponse({"nombre": diccionario_nuevo_evento["nombre"], "mensaje": "Evento guardado correctamente."})

@csrf_exempt
def actualizar_evento(request, id):
    if request.method  in ["PUT", "PATCH"]:
        print(id)
        print (request.method)
        campos_modif_evento = json.loads(request.body)
        print(campos_modif_evento)
        tipo_usuario = campos_modif_evento["tipo_usuario"]
        print(tipo_usuario)
        if tipo_usuario == "organizador":
            nombre_usuario = campos_modif_evento.get("usuario", "")
            print(nombre_usuario)
            evento = Evento.objects.get(id = id)
            evento.nombre = campos_modif_evento.get("nombre", evento.nombre)
            evento.descripcion = campos_modif_evento.get("descripcion", evento.descripcion)
            evento.fecha =  campos_modif_evento.get("fecha", evento.fecha)
            evento.hora = campos_modif_evento.get("hora", evento.hora)
            evento.max_asistencias = campos_modif_evento.get("max_asistencias", evento.max_asistencias)
            if nombre_usuario == "":
                consulta_usuario = UsuarioPersonalizado.objects.get(username=nombre_usuario)
                print(consulta_usuario)
                evento.usuario = campos_modif_evento.get("usuario",consulta_usuario)
            evento.url_img = campos_modif_evento.get("url_img",evento.url_img)
            evento.save()
    return JsonResponse({"mensaje": "Producto actualizado"})








#GET: Listar todos los eventos disponibles (filtros opcionales por título o fecha, ordenados y paginados con un límite de 5 elementos por página).
#POST: Crear un evento (solo organizadores).
#PUT/PATCH: Actualizar un evento (solo organizadores).
#DELETE: Eliminar un evento (solo organizadores).
