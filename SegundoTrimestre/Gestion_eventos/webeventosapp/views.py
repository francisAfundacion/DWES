from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento, UsuarioPersonalizado, Reserva
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

@csrf_exempt
def eliminar_evento(request, id):
    print(id)
    data = json.loads(request.body)
    print(data)
    tipo_usuario = data["tipo_usuario"]
    print("VOY A IMPRIMIR TIPOUSUARIO")
    print(tipo_usuario)
    if tipo_usuario  == "organizador" and request == "DELETE":
        evento_eliminar = Evento.objects.get(id = id)
        evento_eliminar.delete()
    return JsonResponse({"mensaje": "Producto eliiminado"})


#reservas
def listar_reservas(request):
    diccionario_usuario = json.loads(request.body)
    autenticado = diccionario_usuario.get("autenticado",False)
    if autenticado:
        print(diccionario_usuario)
        print(diccionario_usuario["usuario"])
        objeto_usuario = UsuarioPersonalizado.objects.get(username = diccionario_usuario["usuario"])
        print(objeto_usuario)
        print("visualizo objeto evento")
        print(objeto_usuario.tipo)
        #objeto_evento = Evento.objects.filter(usuario = objeto_usuario)
        #objeto_evento = Evento.objects.select_related('usuario').filter(usuario = objeto_usuario)
        #print(objeto_evento)
        lista_diccionario_reservas = []
        #consulta_reservas = Reserva.objects.filter(usuario = objeto_usuario)
        consulta_reservas = Reserva.objects.select_related('usuario').filter(usuario = objeto_usuario)
        print("visual reservas")
        print(consulta_reservas)
        #for
        print("antes del bucle for")
        for sql_reserva in consulta_reservas:
            print("entro bucle llenado lista reservas")
            diccionario_reserva = {}
            diccionario_reserva["estado"] = sql_reserva.estado
            diccionario_reserva["entradas_reservadas"] = sql_reserva.entradas_reservadas
            diccionario_reserva["usuario"] = objeto_usuario.username
            diccionario_reserva["evento"] = sql_reserva.evento.nombre
            print("diccionario_reserva")
            print(diccionario_reserva)
            lista_diccionario_reservas.append(diccionario_reserva)
            print("LISTA DESPUES DE ESTAR LLENA")
            print(lista_diccionario_reservas)
    return JsonResponse(lista_diccionario_reservas, safe=False)

@csrf_exempt
def crear_reserva(request):

    """
       Vista para crear una nueva reserva para un evento.

       Esta vista permite a un usuario crear una reserva para un evento específico.

       Parámetros del cuerpo de la solicitud (JSON):
       - usuario: Nombre del usuario que está realizando la reserva.
       - evento: Nombre del evento para el cual se está realizando la reserva.
       - estado: Estado de la reserva.
       - entradas_reservadas: Número de entradas reservadas.

       Respuesta:
       - Si la reserva se crea correctamente, devuelve el ID de la reserva y el nombre del evento.
       - Si el usuario o el evento no existen, devuelve un error.
       """

    if request.method == "POST":
        diccionario_nueva_reserva = json.loads(request.body)
        nombre_usuario = diccionario_nueva_reserva["usuario"]
        nombre_evento = diccionario_nueva_reserva["evento"]
        try:
            # Verificar si el usuario existe
            objeto_usuario = UsuarioPersonalizado.objects.get(username__iexact = nombre_usuario)
        except UsuarioPersonalizado.DoesNotExist:
            return JsonResponse({"mensaje": "El username introducido no se asocia con ninguno que esté guardado en nuestra base de datos."}, status = 404)
        try:
            # Verificar si el evento existe
            objeto_evento = Evento.objects.get(nombre__iexact = nombre_evento)
            nueva_reserva = Reserva.objects.create(
                estado=diccionario_nueva_reserva["estado"],
                usuario=objeto_usuario,
                evento=objeto_evento,
                entradas_reservadas=diccionario_nueva_reserva["entradas_reservadas"]
            )
            return JsonResponse({"id": nueva_reserva.id, "nombre": nueva_reserva.evento.nombre, "mensaje": "Se ha creado la reserva correctamente."}, status = 201)
        # Si el evento no existe
        except Evento.DoesNotExist:
            return JsonResponse({ "mensaje": "El nombre del evento introducido no se asocia con ninguno que esté guardado en nuestra base de datos."}, status = 404)

@csrf_exempt
def actualizar_reserva(request, id):

    """
     Vista para actualizar una reserva existente.

     Permite a un organizador actualizar los detalles de una reserva, como el estado de la reserva y el número de entradas.

     Parámetros del cuerpo de la solicitud (JSON):
     - estado: Nuevo estado de la reserva.
     - entradas_reservadas: Nuevo número de entradas reservadas.
     - usuario: Nombre del usuario que realizó la reserva.
     - evento: Nombre del evento para el cual se hizo la reserva.

     Respuesta:
     - Si la reserva se actualiza correctamente, devuelve el ID y el nombre del evento.
     - Si no se encuentra la reserva, el usuario o el evento, devuelve un error.
     """

    if request.method in ["PUT","PATCH"]:
        campos_modif_reserva = json.loads(request.body)
        try:
            # Verificar si la reserva con el id especificado existe
            reserva_modif = Reserva.objects.get(id = id)
        except Reserva.DoesNotExist:
            return JsonResponse({ "mensaje": "¡Error! No existe el id de la reserva que se desea modificar."},status = 404)

        reserva_modif.estado = campos_modif_reserva.get("estado", reserva_modif.estado)
        reserva_modif.entradas_reservadas = campos_modif_reserva.get("entradas_reservadas", reserva_modif.entradas_reservadas)
        nombre_usuario = campos_modif_reserva.get("usuario", reserva_modif.usuario.username)
        nombre_evento = campos_modif_reserva.get("evento", reserva_modif.evento.nombre)
        try:
            # Verificar si el usuario existe
            objeto_usuario = UsuarioPersonalizado.objects.get(username__iexact = nombre_usuario)
        except UsuarioPersonalizado.DoesNotExist:
            return  JsonResponse({"mensaje": "¡Error! No se pudo efectuar la modificación debido a que el nombre de usuario introducido no está registrado."}, status = 404)
        try:
            # Verificar si el evento existe
            objeto_evento = Evento.objects.get(nombre__iexact = nombre_evento)
        except Evento.DoesNotExist:
            return JsonResponse({"mensaje": "¡Error! No se pudo efectuar la modificación debido a que el nombre del evento introducido no está registrado."}, status = 404)
        reserva_modif.usuario = objeto_usuario
        reserva_modif.evento = objeto_evento
        reserva_modif.save()
        return JsonResponse({"id": reserva_modif.id, "evento": reserva_modif.evento.nombre, "mensaje": "Reserva actualizada con éxito."})

    @csrf_exempt
    def eliminar_reserva(request, id):

        """
           Vista para cancelar una reserva existente.

           Permite a un participante cancelar su reserva especificando el ID de la reserva.

           Parámetros de la solicitud (URL):
           - tipo_usuario: Tipo de usuario que realiza la solicitud (debe ser 'participante').

           Respuesta:
           - Si la reserva se elimina correctamente, devuelve el mensaje de éxito.
           - Si no se encuentra la reserva o el tipo de usuario es incorrecto, devuelve un error.
           """

        tipo_usuario = request.GET.get("tipo_usuario")
        if request.method == "DELETE" and tipo_usuario == "participante":
            try:
                reserva_eliminar = Reserva.objects.get(id=id)
                info_reserva = {
                    "id": reserva_eliminar.id,
                    "evento": reserva_eliminar.evento.nombre
                }
                reserva_eliminar.delete()
                return JsonResponse({"mensaje": "Evento eliminado con éxito.", "info_reserva": info_reserva})
            except Reserva.DoesNotExist:
                return JsonResponse({"mensaje": "¡Error! No existe el id de la reserva que se desea eliminar."},
                                    status=404)
        else:
            return JsonResponse(
                {"mensaje": "¡Error! El tipo de usuario no es participante. No podrá eliminar reservas."}, status=403)

