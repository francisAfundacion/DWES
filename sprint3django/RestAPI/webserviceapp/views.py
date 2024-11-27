from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse

from .models import Tlibros,Tcomentarios, Tusuarios

import json

from datetime import datetime





  
"""
    Vista que consulta todos los libros de la base de datos y los devuelve en formato JSON.

    Argumentos:
        request: solicitud HTTP recibido.

    Returns:
        JsonResponse: Respuesta en formato JSON que contiene una lista de todos los libros.
""" 
def devolver_libros(request):
    consulta_libros = Tlibros.objects.all()
    conjunto_libros = []

    for fila_libro_sql in consulta_libros:
       diccionario_lib_com = {}
       diccionario_lib_com['id'] = fila_libro_sql.id
       diccionario_lib_com['nombre'] = fila_libro_sql.nombre
       diccionario_lib_com['url_imagen'] = fila_libro_sql.url_imagen
       diccionario_lib_com['autor'] = fila_libro_sql.autor
       diccionario_lib_com['precio'] = fila_libro_sql.precio
       conjunto_libros.append(diccionario_lib_com) 

    return JsonResponse(conjunto_libros, safe=False)

"""
    Vista que consulta  un libro con un id especificado en  la base de datos y lo devuelve en formato JSON.

    Argumentos:
        request: solicitud HTTP recibido.
        id_libro:peti: id del libro de la petición GET.

    Returns:
        JsonResponse: Respuesta en formato JSON que contiene tod la información relativa a un libro.
""" 
def devolver_libro_id (request , id_libro_peti):
    consulta_libros = Tlibros.objects.get(id = id_libro_peti) 
    consulta_comentarios = consulta_libros.tcomentarios_set.all()
    lista_comentarios = []

    for fila_comentario_sql in consulta_comentarios:
       diccionario_lib_com = {}
       diccionario_lib_com['id'] = fila_comentario_sql.libro.id
       diccionario_lib_com['fecha'] = str(fila_comentario_sql.fecha or "Sin fecha")
       diccionario_lib_com['comentario'] = fila_comentario_sql.comentario + ": " + diccionario_lib_com['fecha']
       diccionario_lib_com['usuario'] = fila_comentario_sql.usuario.id
       lista_comentarios.append(diccionario_lib_com)
       print("prueba visual campo libro =>")
       print (consulta_libros.autor)
    resultado = {
        'id': consulta_libros.id,
        'nombre': consulta_libros.nombre,
        'url_imagen': consulta_libros.url_imagen ,
        'autor': consulta_libros.autor,
        'precio': consulta_libros.precio,
        'comentarios': lista_comentarios,
    }
    print("vsual resultado campo")
    print(consulta_libros.autor)
    return JsonResponse(resultado, safe=False)


"""
    Vista que consulta  un libro con un id especificado en  la base de datos y lo devuelve en formato JSON.

    Argumentos:
        request: solicitud HTTP recibido.
        id_libro_peti: id del libro en el que se va a a efectúar la inserción de un comentario.

    Returns:
        JsonResponse: Respuesta en formato JSON que contiene tod la información relativa a un libro.
""" 
@csrf_exempt
def guardar_comentario(request, id_libro_peti):
    if request.method != 'POST':
        mensaje = "Solo se admite peticiones de tipo POST, para la inserción del comentario"
    else:
        mensaje="ok"
        json_comentario_insertar = json.loads(request.body)
        comentario = Tcomentarios()
        comentario.comentario = json_comentario_insertar['nuevo_comentario']
        comentario.libro = Tlibros.objects.get(id = id_libro_peti)
        comentario.fecha = datetime.now()
        comentario.save()
        return JsonResponse ({"status": mensaje})



    
       
