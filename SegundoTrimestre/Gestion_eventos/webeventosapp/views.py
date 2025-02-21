from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento, UsuarioPersonalizado, Reserva, Comentario
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from django.shortcuts import render

class  esOrganizador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.tipo == "organizador"

class  esParticipante(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.tipo == "participante"

class listar_eventosAPIView(APIView):
   # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista eventos que presenta filtros opcionales por nombre del evento o fecha, ordenación acorde a  los campos nombrados y número de página y límite de registros en cada una de estas..",
        manual_parameters=[
            openapi.Parameter('nombre', openapi.IN_QUERY, description="Filtrar por nombre del evento",type=openapi.TYPE_STRING),
            openapi.Parameter('fecha', openapi.IN_QUERY, description="Filtrar por fecha (YYYY-MM-DD)",type=openapi.TYPE_STRING),
            openapi.Parameter('pagina', openapi.IN_QUERY, description="Número de página",type=openapi.TYPE_INTEGER),
            openapi.Parameter('limite', openapi.IN_QUERY, description="Límite de registros de cada página.",type=openapi.TYPE_INTEGER)
        ],
        responses={200: openapi.Response(description="Lista de eventos.")}
    )

    def get(self, request):

        """
        Vista para listar eventos con filtros de búsqueda y paginación.

        Permite filtrar eventos por nombre o fecha, ordenar los resultados por un campo específico
        y paginar los eventos en base a los parámetros recibidos en la URL.

        Parámetros:
        - nombre (opcional): Filtra los eventos cuyo nombre contenga el texto proporcionado.
        - fecha (opcional): Filtra los eventos que coincidan exactamente con la fecha proporcionada.
        - orden (opcional): Define el campo por el cual se ordenarán los eventos (por defecto, 'fecha').
        - limite (opcional): Define el número de eventos por página (por defecto, 5).
        - pagina (opcional): Especifica la página de resultados que se desea mostrar (por defecto, 1).

        Respuesta:
        - Devuelve un JSON con los eventos filtrados, la información de la paginación y el número total de eventos.
        """
        # Obtener los parámetros de la solicitud GET
        query_param_nombre = request.query_params.get("nombre", "")
        query_param_fecha = request.query_params.get("fecha", "")
        query_param_orden = request.query_params.get("orden", "fecha")
        query_param_limite_pag = int(request.query_params.get("limite", 5))
        query_param_n_pagina = int(request.query_params.get("pagina", 1))

        # Filtrado de eventos según los parámetros recibidos
        if query_param_nombre != "":
            eventos = Evento.objects.filter(nombre__icontains=query_param_nombre).order_by(query_param_orden)
        else:
            if query_param_fecha != "":
                eventos = Evento.objects.filter(fecha__exact=query_param_fecha).order_by(query_param_orden)
            else:
                eventos = Evento.objects.all().order_by(query_param_orden)

        # Dividir productos en páginas de tamaño `limite`
        paginator = Paginator(eventos, query_param_limite_pag)
        try:
            # Obtener los productos de la página actual
            eventos_pagina = paginator.page(query_param_n_pagina)
        except Exception as e:
            return Response({"error": str(e)}, status=400)  # Manejar errores de paginación

        # Formatear los eventos para la respuesta JSON
        lista_json_eventos = []
        for evento in eventos_pagina:
            json_evento = {}
            json_evento['id'] = evento.id,
            json_evento['nombre'] = evento.nombre
            json_evento['descripcion'] = evento.descripcion
            json_evento['fecha'] = evento.fecha
            json_evento['hora'] = evento.hora
            json_evento['max_asistencias'] = evento.max_asistencias
            json_evento['usuario'] = evento.usuario.username
            json_evento['url_img'] = evento.url_img
            lista_json_eventos.append(json_evento)

        # Respuesta con los eventos paginados y metadatos de la paginación
        data = {
            "count": paginator.count,  # Total de eventos encontrados
            "total_pages": paginator.num_pages,  # Número total de páginas
            "current_page": query_param_n_pagina,  # Página actual
            "next": query_param_n_pagina + 1 if eventos_pagina.has_next() else None,  # Página siguiente si existe
            "previous": query_param_n_pagina - 1 if eventos_pagina.has_previous() else None,  # Página anterior si existe
            "results": lista_json_eventos  # Lista de eventos de la página actual
        }
        return render (request, 'Lista_eventos.html', {"data":data})

class crear_eventoAPIView(APIView):
    permission_classes = [esOrganizador]

    @swagger_auto_schema(
        operation_description="Crea un nuevo evento.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del evento'),
                'fecha': openapi.Schema(type=openapi.TYPE_STRING, format="date", description='Fecha del evento'),
                'hora': openapi.Schema(type=openapi.TYPE_STRING, format="time", description='Hora del evento'),
                'max_asistencias': openapi.Schema(type=openapi.TYPE_INTEGER,description='Capacidad máxima de asistentes'),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario.'),
                'url_img': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la imagen.')
            },
            required=['nombre', 'descripcion', 'fecha', 'hora', 'max_asistencias', 'usuario', 'url_img']
        ),
        responses={201: openapi.Response(description="Evento creado"),
                   404: openapi.Response( description="No existe el usuario asociado al evento que se desea crear en nuestra base de datos.")
                   }
    )
    def post (self, request):
        """
        Vista para crear un nuevo evento.

        Esta vista permite a un usuario de tipo 'organizador' crear un evento proporcionando los datos necesarios
        como nombre, descripción, fecha, hora, etc., y asociarlo a un usuario existente.

        Parámetros del cuerpo de la solicitud (JSON):
        - tipo_usuario: El tipo de usuario que realiza la solicitud (debe ser 'organizador').
        - usuario: El nombre de usuario del organizador que está creando el evento.
        - nombre: El nombre del evento.
        - descripcion: Una descripción del evento.
        - fecha: La fecha en la que se llevará a cabo el evento.
        - hora: La hora en la que comenzará el evento.
        - max_asistencias: El número máximo de asistentes permitido para el evento.
        - url_img: URL de la imagen asociada al evento.

        Respuesta:
        - Si el usuario es válido y el evento se crea correctamente, devuelve los detalles del evento creado.
        - Si el tipo de usuario no es 'organizador', devuelve un error con código de estado 403 (Prohibido).
        """

        diccionario_nuevo_evento = request.data
        if request.method == "POST":
            # Crear un nuevo evento con los datos proporcionados
            nuevo_evento = Evento.objects.create(
                nombre=diccionario_nuevo_evento["nombre"],
                descripcion=diccionario_nuevo_evento["descripcion"],
                fecha=diccionario_nuevo_evento["fecha"],
                hora=diccionario_nuevo_evento["hora"],
                max_asistencias=diccionario_nuevo_evento["max_asistencias"],
                usuario=request.user,
                url_img=diccionario_nuevo_evento["url_img"]
            )

            # Responder con los detalles del evento creado
            return Response({"id": nuevo_evento.id, "nombre": nuevo_evento.nombre, "mensaje": "Evento guardado correctamente."},status=201)

class actualizar_eventoAPIView(APIView):
    permission_classes = [esOrganizador]
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un  evento.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del evento'),
                'fecha': openapi.Schema(type=openapi.TYPE_STRING, format="date", description='Fecha del evento'),
                'hora': openapi.Schema(type=openapi.TYPE_STRING, format="time", description='Hora del evento'),
                'max_asistencias': openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacidad máxima de asistentes'),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario.'),
                'url_img': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la imagen.')
            },
        ),
        responses={200: openapi.Response(description="Evento actualizado."),
                   404: openapi.Response(description="No hay ningún evento identificado por el id deseado en nuestra base de datos.")}
    )

    def put (self, request, id):
        return self.actualizar_evento(request,id)

    @swagger_auto_schema(
        operation_description="Actualiza totalmente un  evento.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del evento'),
                'fecha': openapi.Schema(type=openapi.TYPE_STRING, format="date", description='Fecha del evento'),
                'hora': openapi.Schema(type=openapi.TYPE_STRING, format="time", description='Hora del evento'),
                'max_asistencias': openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacidad máxima de asistentes'),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario.'),
                'url_img': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la imagen.')
            },
            required=['nombre', 'descripcion', 'fecha', 'max_asistencias']
        ),
        responses={200: openapi.Response(description="Evento actualizado."),
                   404: openapi.Response(description="No hay ningún evento identificado por el id deseado en nuestra base de datos.")}
    )
    def patch (self, request, id):
        return(self.actualizar_evento(request, id))

    def actualizar_evento(self, request, id):

        """
        Vista para actualizar los detalles de un evento existente.

        Permite a un usuario de tipo 'organizador' modificar los atributos de un evento, como nombre, descripción,
        fecha, hora, número máximo de asistentes y la imagen asociada.

        Parámetros del cuerpo de la solicitud (JSON):
        - tipo_usuario: El tipo de usuario que realiza la solicitud (debe ser 'organizador').
        - id: El ID del evento a actualizar.
        - nombre: Nuevo nombre del evento (opcional).
        - descripcion: Nueva descripción del evento (opcional).
        - fecha: Nueva fecha del evento (opcional).
        - hora: Nueva hora del evento (opcional).
        - max_asistencias: Nuevo número máximo de asistentes (opcional).
        - url_img: Nueva URL de la imagen asociada al evento (opcional).

        Respuesta:
        - Si el evento y el usuario asociado existen, se actualizan los detalles y se devuelve el evento actualizado.
        - Si el evento no existe, se devuelve un error con código de estado 404 (No encontrado).
        - Si el usuario no existe, se devuelve un error con código de estado 404 (No encontrado).
        - Si el usuario no existe en el sistema, se devuelve un error con código de estado 404 (No encontrado).
        - Si el tipo de usuario no es 'organizador', no se actualiza el evento y se devuelve un error con código de estado 403 (Prohibido).
        """

        if request.method in ["PUT", "PATCH"]:
            # Cargar los datos del cuerpo de la solicitud
            campos_modif_evento = request.data
            try:
                 # Obtener el evento a actualizar mediante su ID
                evento = Evento.objects.get(id=id)
                # Actualizar los atributos del evento
                evento.nombre = campos_modif_evento.get("nombre", evento.nombre)
                evento.descripcion = campos_modif_evento.get("descripcion", evento.descripcion)
                evento.fecha = campos_modif_evento.get("fecha", evento.fecha)
                evento.hora = campos_modif_evento.get("hora", evento.hora)
                evento.max_asistencias = campos_modif_evento.get("max_asistencias", evento.max_asistencias)
                evento.url_img = campos_modif_evento.get("url_img", evento.url_img)
                try:
                    nombre_usuario = campos_modif_evento.get("usuario", evento.usuario)
                    usuario = UsuarioPersonalizado.objects.get(username__iexact=nombre_usuario)
                    evento.usuario = usuario
                except UsuarioPersonalizado.DoesNotExist:
                    return Response({"mensaje": "El usuario no existe."}, status=404)
                evento.save()

                # Responder con el evento actualizado
                return Response({"id": evento.id, "nombre": evento.nombre, "mensaje": "Evento actualizado."},status=200)
            # Si el usuario no existe, devolver un error 404
            except Evento.DoesNotExist:
            # Si el evento no existe, devolver un error 404
                return Response(
                        {"mensaje": "No hay ningún evento identificado por el id deseado en nuestra base de datos."},
                        status=404)
            except:
                return Response({"mensaje":"El nombre del usuario no existe en nuestras bases de datos."}, status=404)



class eliminar_eventoAPIView(APIView):
    permission_classes = [esOrganizador]

    @swagger_auto_schema(
        operation_description="Elimina eventos filtrados por título o fecha.",
        responses={200: openapi.Response(description="Lista de eventos."),
                   404: openapi.Response(description="No existe un evento con el id especificado en nuestra base de datos")
                   }
    )

    def delete (self, request, id):
            if  request.method == "DELETE":
                try:
                    evento_eliminar = Evento.objects.get(id=id)
                    evento_eliminar.delete()
                    return Response({"id": id, "evento": evento_eliminar.nombre,"mensaje": "Evento eliminado con éxito."})
                except Evento.DoesNotExist:
                    return Response({"mensaje": "No existe un evento con el id especificado en nuestra base de datos."},
                                        status=404)

class listar_reservasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            operation_description="Obtener lista de reservas de un usuario autenticado.",
            responses={200: openapi.Response("Lista de productos"), }
        )
    def get(self, request):

        """
        Vista para listar las reservas de un usuario.

        Esta vista permite obtener todas las reservas realizadas por un usuario,
        filtradas por su nombre de usuario.

        Parámetros de la solicitud:
        - `autenticado` (str): Indica si el usuario está autenticado ("true" o "false").
        - `usuario` (str): Nombre de usuario para el cual se desean obtener las reservas.

        Respuesta:
        - Devuelve una lista con las reservas del usuario, incluyendo:
          - ID de la reserva.
          - Estado de la reserva.
          - Nombre del usuario.
          - Nombre del evento asociado.
          - Número de entradas reservadas.

        - Si el usuario no está autenticado, devuelve un error 403.
        - Si el usuario no existe, devuelve un error 404.
        """

        # Obtener todas las reservas del usuario
        usuario = request.user.username
        reservas_usuario = Reserva.objects.select_related('usuario').filter(usuario__username=usuario)

        # Construcción de la respuesta con los detalles de la reserva
        data_reservas = [
            {
                "id": sql_reserva.id,
                "estado": sql_reserva.estado,
                "usuario": request.user.username,
                "evento": sql_reserva.evento.nombre,
                "entradas_reservadas": sql_reserva.entradas_reservadas,
            }
            for sql_reserva in reservas_usuario
        ]
        return render(request,'Panel_usuario.html', {"data":data_reservas})

class eliminar_reservasAPIView(APIView):
    permission_classes = [esParticipante]
    @swagger_auto_schema(
        operation_description="Eliminar reservas  para los usuarios participantes logueados, acorde a un id especificado en la url.",
        responses={200: openapi.Response("Reserva eliminada con éxito."),
                   404: openapi.Response("¡Error! No existe el id de la reserva que se desea eliminar.")
        }
    )
    def delete(self, request, id):

        """
        Vista para cancelar una reserva existente.

        Permite a un participante cancelar su reserva especificando el ID de la reserva.

        Parámetros de la solicitud (URL):
        - tipo_usuario: Tipo de usuario que realiza la solicitud (debe ser 'participante').

        Respuesta:
        - Si la reserva se elimina correctamente, devuelve un mensaje de éxito con los detalles de la reserva eliminada.
        - Si no se encuentra la reserva, devuelve un error con código 404 (No encontrado).
        - Si el tipo de usuario no es 'participante', devuelve un error con código 403 (Prohibido).

        Respuesta de error:
        - Si el tipo de usuario no es 'participante', se devuelve un error con código de estado 403.
        - Si la reserva con el ID especificado no existe, se devuelve un error con código de estado 404.
        """

        # Verificar si el tipo de usuario es 'participante' y si la solicitud es de tipo DELETE
        try:
            # Verificar si la reserva con el ID proporcionado existe
            reserva_eliminar = Reserva.objects.get(id=id)
            # Obtener información de la reserva que será eliminada
            info_reserva = {
                "id": reserva_eliminar.id,
                "evento": reserva_eliminar.evento.nombre
            }
            #Eliminar la reserva
            reserva_eliminar.delete()
            # Responder con mensaje de éxito
            return Response({"mensaje": "Reserva eliminada con éxito.", "info_reserva": info_reserva},status=200)
        except Reserva.DoesNotExist:
            # Si la reserva no existe, devolver un error con código 404
            return Response({"mensaje": "¡Error! No existe el id de la reserva que se desea eliminar."},status=404)

class crear_reservaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Crea una nueva reserva.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'evento': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'entradas_reservadas': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de entradas reservadas'),
                'estado': openapi.Schema(type=openapi.TYPE_STRING, description="Estado de la reserva")
            },
            required=['evento', 'entradas_reservadas','estado']
        ),
        responses={201: openapi.Response(description="Se ha creado la reserva correctamente."),
                   403: openapi.Response(description="El nombre del evento introducido no se asocia con ninguno que esté guardado en nuestra base de datos.")}
    )
    def post (self, request):

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
           """
        diccionario_nueva_reserva = request.data
        nombre_evento = diccionario_nueva_reserva["evento"]
        try:
            # Verificar si el evento existe
            objeto_evento = Evento.objects.get(nombre__iexact = nombre_evento)
            nueva_reserva = Reserva.objects.create(
                estado=diccionario_nueva_reserva["estado"],
                usuario=request.user,
                evento=objeto_evento,
                entradas_reservadas=diccionario_nueva_reserva["entradas_reservadas"]
            )
            return Response({"id": nueva_reserva.id, "nombre": nueva_reserva.evento.nombre, "mensaje": "Se ha creado la reserva correctamente."}, status = 201)
         # Si el evento no existe
        except Evento.DoesNotExist:
            return Response({ "mensaje": "El nombre del evento introducido no se asocia con ninguno que esté guardado en nuestra base de datos."}, status = 404)

class actualizar_reservaAPIView(APIView):
    permission_classes = [esOrganizador]

    @swagger_auto_schema(
        operation_description="Modifica los organizadores los campos  parcialmente  de la reserva concretada.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'evento': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'entradas_reservadas': openapi.Schema(type=openapi.TYPE_INTEGER,description='Número de entradas reservadas'),
                'estado': openapi.Schema(type=openapi.TYPE_STRING, description="Estado de la reserva"),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del usuario")
            },
        ),
        responses={200: openapi.Response(description="Se ha modificado la reserva correctamente."),
                   404: openapi.Response(description="¡Error! No se pudo efectuar la modificación debido a que el nombre del evento introducido no está registrado.")}
    )
    def patch(self,request,id):
        return self.actualizar_reserva(request, id)

    @swagger_auto_schema(
        operation_description="Modifica los organizadores los campos totalmente   de la reserva.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'evento': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'entradas_reservadas': openapi.Schema(type=openapi.TYPE_INTEGER,description='Número de entradas reservadas'),
                'estado': openapi.Schema(type=openapi.TYPE_STRING, description="Estado de la reserva"),
                'usuario':openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del usuario")
            },
            required=['evento', 'entradas_reservadas', 'estado', 'usuario']
        ),
        responses={200: openapi.Response(description="Se ha modificado la reserva correctamente."),
                   404: openapi.Response(description="¡Error! No se pudo efectuar la modificación debido a los siguientes motivos:"
                                                     "\n- Nombre del evento introducido no está registrado."
                                                     "\n- No existe el usuario introducido"
                                                    "\n- No existe el id de la reserva.")}
    )

    def put (self, request, id):
        return self.actualizar_reserva(request, id)

    def actualizar_reserva(self, request, id):

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
         - Si no se encuentra la reserva o el evento, devuelve un error.
         - Si el usuario que efectúa la actualización de la reserva no es de tipo organizador, se mostrará mensaje de error.
         """

        campos_modif_reserva = request.data
        try:
            # Verificar si la reserva con el id especificado existe
            reserva_modif = Reserva.objects.get(id = id)
        except Reserva.DoesNotExist:
            return Response({ "mensaje": "¡Error! No existe el id de la reserva que se desea modificar."},status = 404)
        try:
            # Verificar si el usuario existe
            nombre_usuario = campos_modif_reserva.get("usuario", reserva_modif.usuario.username)
            objeto_usuario = UsuarioPersonalizado.objects.get(username__iexact = nombre_usuario)
        except UsuarioPersonalizado.DoesNotExist:
            return  Response({"mensaje": "¡Error! No existe el usuario introducido."}, status = 404)
        try:
            reserva_modif.estado = campos_modif_reserva.get("estado", reserva_modif.estado)
            reserva_modif.entradas_reservadas = campos_modif_reserva.get("entradas_reservadas",reserva_modif.entradas_reservadas)
            nombre_evento = campos_modif_reserva.get("evento", reserva_modif.evento.nombre)
            # Verificar si el evento existe
            objeto_evento = Evento.objects.get(nombre__iexact = nombre_evento)
            reserva_modif.usuario = objeto_usuario
            reserva_modif.evento = objeto_evento
            reserva_modif.save()
            return Response({"id": reserva_modif.id, "evento": reserva_modif.evento.nombre,"mensaje": "Reserva actualizada con éxito."})
        except Evento.DoesNotExist:
            return Response({"mensaje": "¡Error! No se pudo efectuar la modificación debido a que el nombre del evento introducido no está registrado."}, status = 404)

class listar_comentariosAPIView(APIView):
    permission_classes =  [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Obtener lista de comentarios de un evento.",
        responses={200: openapi.Response( description="Lista de comentarios."),
                   404: openapi.Response(description="Posibles errores de no encontrado:\n"
                    "- No hay comentarios asociados al evento especificado.\n"
                    "- ¡Error! El id del evento deseada para su listado es incorrecto.")
        },
    )
    def get(self, request, id):
        """
           Vista para listar los comentarios asociados a un evento.

           Permite listar los comentarios que los usuarios han realizado en un evento especificado por su ID.

           Parámetros de la solicitud (URL):
           - id: ID del evento (obligatorio).

           Respuesta:
           - Si existen comentarios para el evento, devuelve una lista de comentarios en formato JSON.
           - Si no se encuentran comentarios o el evento no existe, devuelve un error con el mensaje correspondiente.

           Respuesta de error:
           - Si el evento no existe, se devuelve un error con código de estado 404 (No encontrado).
           - Si no hay comentarios asociados al evento, se devuelve un error con código de estado 404 (No encontrado).
           """
        try:
            # Verificar si el evento con el ID proporcionado existe
            objeto_evento = Evento.objects.get(id=id)
            # Consultar los comentarios asociados a ese evento
            consulta_comentarios = Comentario.objects.select_related('evento').filter(evento=objeto_evento)
            # Formatear los comentarios en una lista
            lista_comentarios = [{"id": sql_comentario.id,
                            "texto": sql_comentario.texto,
                            "usuario": sql_comentario.usuario.username,
                            "fecha": sql_comentario.fecha,
                            "evento": objeto_evento.nombre}
                            for sql_comentario in consulta_comentarios]
        # Si no hay comentarios para el evento
            if len(lista_comentarios) == 0:
                return render({"mensaje": "No hay comentarios asociados al evento especificado."}, status = 404, )
            else:
                return render(lista_comentarios)
        # Si el evento no existe
        except Evento.DoesNotExist:
            return render({"mensaje": "¡Error! El id del evento deseada para su listado es incorrecto."}, status = 404)


class crear_comentarioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Crea un nuevo evento.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'texto': openapi.Schema(type=openapi.TYPE_STRING, description='Texto asociado al comentario.'),
                'fecha': openapi.Schema(type=openapi.TYPE_STRING, format="date-time",description='Fecha y hora del evento.'),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario.'),
                'evento': openapi.Schema(type=openapi.TYPE_STRING, description='Evento al que se le asociará el comentario creado.'),
            },
            required=['texto', 'fecha', 'usuario', 'evento']
        ),
        responses={201: openapi.Response(description="El comentario se ha creado correctamente."),
                   404: openapi.Response(description="El evento que se desea asociar en la creación del comentario no existe en nuestra base de datos.")}
    )
    def post(self, request):

        """
           Vista para crear un nuevo comentario para un evento.

           Permite a los usuarios autenticados crear comentarios asociados a un evento específico.

           Parámetros del cuerpo de la solicitud (JSON):
           - usuario: Nombre del usuario que crea el comentario (obligatorio).
           - evento: Nombre del evento al que se asocia el comentario (obligatorio).
           - texto: El contenido del comentario (obligatorio).
           - fecha: La fecha en que el comentario fue creado (obligatorio).

           Respuesta:
           - Si el comentario se crea correctamente, devuelve el ID del comentario y el nombre del evento.
           - Si el usuario no está autenticado o no existen el evento o el usuario, devuelve un error con el mensaje correspondiente.

           Respuesta de error:
           - Si el usuario no está autenticado, se devuelve un error con código de estado 403 (Prohibido).
           - Si el usuario no existe en la base de datos, se devuelve un error con código de estado 404 (No encontrado).
           - Si el evento no existe en la base de datos, se devuelve un error con código de estado 404 (No encontrado).
           """
        try:
            # Procesar el cuerpo de la solicitud para crear el comentario
            diccionario_comentario = request.data
            nombre_evento = diccionario_comentario["evento"]
            # Verificar si el evento existe en la base de datos
            objeto_evento = Evento.objects.get(nombre = nombre_evento)
            # Crear el comentario
            nuevo_comentario = Comentario.objects.create(
                texto = diccionario_comentario["texto"],
                fecha = diccionario_comentario["fecha"],
                usuario = request.user,
                evento = objeto_evento
            )
            return Response({"id": nuevo_comentario.id, "evento": objeto_evento.nombre,"mensaje": "El comentario se ha creado correctamente."}, status = 201)
        except Evento.DoesNotExist:
            # Error si el evento no existe
            return Response({"mensaje":"El evento que se desea asociar en la creación del comentario no existe en nuestra base de datos."}, status = 404)


def comprobar_username(nombre_usuario):

    """
    Verifica si el nombre de usuario existe en la base de datos.

    Parámetros:
    - nombre_usuario: El nombre de usuario a verificar.

    Retorna:
    - True si el nombre de usuario existe.
    - False si el nombre de usuario no existe.
    """

    return UsuarioPersonalizado.objects.filter(username = nombre_usuario).exists()

def comprobar_contrasena (pass_usuario):

    """
    Verifica si la contraseña existe en la base de datos.

    Parámetros:
    - pass_usuario: La contraseña del usuario.

    Retorna:
    - True si la contraseña es válida.
    - False si la contraseña es incorrecta.
    """

    return UsuarioPersonalizado.objects.filter(password = pass_usuario).exists()

def comprobar_email (email_usuario):

    """
    Verifica si el email existe en la base de datos.

    Parámetros:
    - email_usuario: El email del usuario.

    Retorna:
    - True si el email existe.
    - False si el email no existe.
    """
    return UsuarioPersonalizado.objects.filter(email = email_usuario).exists()

class registerAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Permite dar de alta a un usuario en el sistema.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                'tipo_usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario en el sistema.'),
                'biografia': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario en el sistema.'),
            },
            required=['username', 'password', 'email', 'tipo_usuario']
        ),
        responses={201: openapi.Response(description="El usuario ha sido dado de alta con éxito."),
                    400: openapi.Response(description="Posibles errores al intentar registrarse un usuario:\n"
                    "- Se han dejado campo/s obligatorio/s sin rellenar. Recuerda que el único campo opcional es la biografía.\n"
                    "- El tipo de usuario es incorrecto, debería ser organizador o participante.\n"
                    "- El email introducido ya está en uso.\n"
                    "- El nombre de usuario introducido ya está en uso.\n"
                    "- La contraseña introducida ya está en uso."),
        }
    )
    def post(self, request):

        """
            Vista para registrar un nuevo usuario en el sistema.

            Permite la creación de un usuario, donde se deben proporcionar los siguientes datos:
            - username: Nombre de usuario (obligatorio).
            - password: Contraseña (obligatoria).
            - email: Correo electrónico (obligatorio).
            - tipo_usuario: Tipo de usuario (obligatorio, debe ser 'organizador' o 'participante').
            - biografia: Biografía del usuario (opcional).

            La función realiza las siguientes validaciones:
            - Verifica que no se dejen campos obligatorios vacíos (username, password, email, tipo_usuario).
            - Comprueba que el nombre de usuario, correo electrónico y contraseña no estén siendo utilizados por otro usuario.
            - Verifica que el tipo de usuario sea uno de los valores permitidos ('organizador' o 'participante').

            Respuesta:
            - Si todos los datos son válidos, crea un nuevo usuario y devuelve los detalles del usuario junto con un mensaje de éxito.
            - Si algún campo obligatorio está vacío o hay un error con los datos, se devuelve un mensaje de error indicando el problema.
            """
        diccionario_usuario_alta = request.data
        nombre_usuario = diccionario_usuario_alta.get("username", "")
        pass_usuario = diccionario_usuario_alta.get("password", "")
        email_usuario = diccionario_usuario_alta.get("email", "")
        tipo_usuario = diccionario_usuario_alta.get("tipo_usuario", "").lower()
        biografia_usuario = diccionario_usuario_alta.get("biografia","")

        # Validación de campos obligatorios
        if nombre_usuario == "" or pass_usuario == "" or email_usuario == "" or tipo_usuario == "":
            return Response({"mensaje": "Se han dejado campo/s obligatorio/s sin rellenar. Recuerda que el único campo opcional es la biografía."}, status = 400)

        # Validación de que los datos sean únicos y tipo de usuario válido
        if tipo_usuario not in ["organizador","participante"]:
            return Response({"tipo_usuario": tipo_usuario, "mensaje": "El tipo de usuario es incorrecto, debería ser organizador o participante."},status=400)

        if comprobar_email(email_usuario):
            return Response({"email": email_usuario, "mensaje": "El email introducido ya está en uso."}, status=400)

        if comprobar_username(nombre_usuario):
            return Response({"usuario": nombre_usuario, "mensaje": "El nombre de usuario introducido ya está en uso."}, status=400)

        if comprobar_contrasena(pass_usuario):
            return Response({"mensaje": "La contraseña introducida ya está en uso"},status=400)

        # Creación del nuevo usuario
        nuevo_usuario = UsuarioPersonalizado.objects.create(
            username = nombre_usuario,
            password = pass_usuario,
            email = email_usuario,
            tipo = tipo_usuario,
            biografia = biografia_usuario
        )
        return Response({"usuario": nuevo_usuario.username, "email": nuevo_usuario.password, "mensaje": "El usuario ha sido dado de alta con éxito."}, status = 201)

def pagina_login(request):
    return render(request, 'Login.html')

def detalle_evento(request, id):
    evento = Evento.objects.get(id=id)
    print(evento)
    evento_detalles ={"nombre": evento.nombre,
         "descripcion": evento.descripcion,
         "fecha": evento.fecha,
         "hora": evento.fecha,
         "max_asistencias": evento.max_asistencias,
         "usuario":evento.usuario.username,
         "url_img":evento.url_img,
    }
    print(evento_detalles)
    return render (request,'EventoDetalle.html', {'evento':evento_detalles})


