from django.shortcuts import render
from django.http import JsonResponse
from .models import Evento, UsuarioPersonalizado, Reserva, Comentario
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from datetime import datetime
import json

@require_http_methods(["GET"])
def listar_eventos(request):

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
    query_param_nombre = request.GET.get("nombre", "")
    query_param_fecha = request.GET.get("fecha", "")
    query_param_orden = request.GET.get("orden", "fecha")
    query_param_limite_pag = int(request.GET.get("limite", 5))
    query_param_n_pagina = int(request.GET.get("pagina", 1))

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
        return JsonResponse({"error": str(e)}, status=400)  # Manejar errores de paginación

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

    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
@csrf_exempt
def crear_evento(request):
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
    - Si el usuario no existe, devuelve un error indicando que el usuario no se encuentra en la base de datos.
    - Si el tipo de usuario no es 'organizador', devuelve un error con código de estado 403 (Prohibido).
    """

    diccionario_nuevo_evento = json.loads(request.body)
    tipo_usuario = diccionario_nuevo_evento['tipo_usuario']

    if request.method == "POST" and tipo_usuario == "organizador":
        nombre_usuario_post = diccionario_nuevo_evento["usuario"]
        try:
            # Obtener el usuario asociado al evento
            consulta_usuario_post = UsuarioPersonalizado.objects.get(username__iexact=nombre_usuario_post)
            # Crear un nuevo evento con los datos proporcionados
            nuevo_evento = Evento.objects.create(
                nombre=diccionario_nuevo_evento["nombre"],
                descripcion=diccionario_nuevo_evento["descripcion"],
                fecha=diccionario_nuevo_evento["fecha"],
                hora=diccionario_nuevo_evento["hora"],
                max_asistencias=diccionario_nuevo_evento["max_asistencias"],
                usuario=consulta_usuario_post,
                url_img=diccionario_nuevo_evento["url_img"]
            )

            # Responder con los detalles del evento creado
            return JsonResponse({"id": nuevo_evento.id, "nombre": nuevo_evento.nombre, "mensaje": "Evento guardado correctamente."},status=201)

        except UsuarioPersonalizado.DoesNotExist:
            # Si no existe el usuario asociado al evento, devolver un error 404
            return JsonResponse({"mensaje": "No existe el usuario asociado al evento que se desea crear en nuestra base de datos."},status=404)
    else :
        return JsonResponse({"mensaje":"El tipo de usuario no es organizador. No se puede efectuar la creación del evento."}, status=403)

@require_http_methods(["PUT","PATCH"])
@csrf_exempt
def actualizar_evento(request, id):
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
    - Si el usuario no existe en el sistema, se devuelve un error con código de estado 404 (No encontrado).
    - Si el tipo de usuario no es 'organizador', no se actualiza el evento y se devuelve un error con código de estado 403 (Prohibido).
    """

    if request.method in ["PUT", "PATCH"]:
        # Cargar los datos del cuerpo de la solicitud
        campos_modif_evento = json.loads(request.body)
        tipo_usuario = campos_modif_evento["tipo_usuario"]

        # Verificar que el usuario es de tipo 'organizador'
        if tipo_usuario == "organizador":
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

                # Obtener el usuario asociado al evento (se verifica que exista)
                nombre_usuario = campos_modif_evento.get("usuario", evento.usuario.username)
                consulta_usuario = UsuarioPersonalizado.objects.get(username=nombre_usuario)
                evento.usuario = consulta_usuario

                # Guardar los cambios en el evento
                evento.save()

                # Responder con el evento actualizado
                return JsonResponse({"id": evento.id, "nombre": evento.nombre, "mensaje": "Evento actualizado."})
                # Si el usuario no existe, devolver un error 404
            except Evento.DoesNotExist:
                # Si el evento no existe, devolver un error 404
                return JsonResponse({"mensaje": "No hay ningún evento identificado por el id deseado en nuestra base de datos."}, status=404)
        else:
            # Si el tipo de usuario no es 'organizador', devolver un error 403
            return JsonResponse({"mensaje": "¡Error! Solo un organizador puede modificar los eventos."}, status=403)


@require_http_methods(["DELETE"])
@csrf_exempt
def eliminar_evento(request, id):
    if request.method == "DELETE":
        data = json.loads(request.body)
        tipo_usuario = data.get("tipo_usuario", "")
        if tipo_usuario == "organizador" and request.method == "DELETE":
            try:
                evento_eliminar = Evento.objects.get(id=id)
                evento_eliminar.delete()
                return JsonResponse({"id": id, "evento": evento_eliminar.nombre,"mensaje": "Evento eliminado con éxito."})
            except Evento.DoesNotExist:
                return JsonResponse({"mensaje": "No existe un evento con el id especificado en nuestra base de datos."},
                                    status=404)
        else:
            return JsonResponse({"mensaje": "No se permite la acción de borrado sobre eventos a usuarios que no son organizadores."},status=403)

@require_http_methods(["DELETE"])
@csrf_exempt
def eliminar_reserva(request, id):

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

    tipo_usuario = request.GET.get("tipo_usuario")
    # Verificar si el tipo de usuario es 'participante' y si la solicitud es de tipo DELETE
    if request.method == "DELETE" and tipo_usuario == "participante":
        try:
            # Verificar si la reserva con el ID proporcionado existe
            reserva_eliminar = Reserva.objects.get(id=id)
            # Obtener información de la reserva que será eliminada
            info_reserva = {
                "id": reserva_eliminar.id,
                "evento": reserva_eliminar.evento.nombre
            }
            # Eliminar la reserva
            reserva_eliminar.delete()
            # Responder con mensaje de éxito
            return JsonResponse({"mensaje": "Producto eliminado con éxito.", "info_reserva": info_reserva})
        except Reserva.DoesNotExist:
            # Si la reserva no existe, devolver un error con código 404
            return JsonResponse({"mensaje": "¡Error! No existe el id de la reserva que se desea eliminar."}, status=404)
    else:
        # Si el tipo de usuario no es 'participante', devolver un error con código 403
        return JsonResponse({"mensaje": "¡Error! El tipo de usuario no es de tipo participante. No podrá eliminar reservas."}, status=403)

@require_http_methods(["GET"])
def listar_reservas(request):

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

    autenticado = request.GET.get("autenticado", "false").lower() == "true"
    print(autenticado)

    if not autenticado:
        return JsonResponse({"mensaje": "El usuario al no estar autenticado, no podrá listar los comentarios."},
                            status=403)

    nombre_usuario = request.GET.get("usuario")

    try:
        # Obtener el usuario por nombre (ignorando mayúsculas/minúsculas)
        objeto_usuario = UsuarioPersonalizado.objects.get(username__iexact=nombre_usuario)
    except ObjectDoesNotExist:
        return JsonResponse({"mensaje": "El usuario no existe."}, status=404)

    # Obtener todas las reservas del usuario
    reservas_usuario = Reserva.objects.select_related('usuario').filter(usuario=objeto_usuario)

    # Construcción de la respuesta con los detalles de la reserva
    data_reservas = [
        {
            "id": sql_reserva.id,
            "estado": sql_reserva.estado,
            "usuario": nombre_usuario,
            "evento": sql_reserva.evento.nombre,
            "entradas_reservadas": sql_reserva.entradas_reservadas,
        }
        for sql_reserva in reservas_usuario
    ]

    return JsonResponse(data_reservas, safe=False)

@require_http_methods(["POST"])
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


@require_http_methods(["PUT","PATCH"])
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
     - Si el usuario que efectúa la actualización de la reserva no es de tipo organizador, se mostrará mensaje de error.
     """

    if request.method in ["PUT","PATCH"]:
        campos_modif_reserva = json.loads(request.body)
        try:
            # Verificar si la reserva con el id especificado existe
            reserva_modif = Reserva.objects.get(id = id)
        except Reserva.DoesNotExist:
            return JsonResponse({ "mensaje": "¡Error! No existe el id de la reserva que se desea modificar."},status = 404)
        try:
            # Verificar si el usuario existe
            nombre_usuario = campos_modif_reserva.get("usuario", reserva_modif.usuario.username)
            objeto_usuario = UsuarioPersonalizado.objects.get(username__iexact = nombre_usuario)
        except UsuarioPersonalizado.DoesNotExist:
            return  JsonResponse({"mensaje": "¡Error! No se pudo efectuar la modificación debido a que el nombre de usuario introducido no está registrado."}, status = 404)
        try:
            if objeto_usuario.tipo == "organizador":
                reserva_modif.estado = campos_modif_reserva.get("estado", reserva_modif.estado)
                reserva_modif.entradas_reservadas = campos_modif_reserva.get("entradas_reservadas",reserva_modif.entradas_reservadas)
                nombre_evento = campos_modif_reserva.get("evento", reserva_modif.evento.nombre)
                # Verificar si el evento existe
                objeto_evento = Evento.objects.get(nombre__iexact = nombre_evento)
                reserva_modif.usuario = objeto_usuario
                reserva_modif.evento = objeto_evento
                reserva_modif.save()
                return JsonResponse({"id": reserva_modif.id, "evento": reserva_modif.evento.nombre,"mensaje": "Reserva actualizada con éxito."})
            else:
                return JsonResponse({"mensaje": "No se le permite  actualizar la reserva al no ser un usuario de tipo organizador."}, status=403)
        except Evento.DoesNotExist:
            return JsonResponse({"mensaje": "¡Error! No se pudo efectuar la modificación debido a que el nombre del evento introducido no está registrado."}, status = 404)


@require_http_methods(["GET"])
@csrf_exempt
def listar_comentarios(request, id):

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
            return JsonResponse({"mensaje": "No hay comentarios asociados al evento especificado."}, status = 404)
        else:
            return JsonResponse(lista_comentarios, safe=False)
    # Si el evento no existe
    except Evento.DoesNotExist:
        return JsonResponse({"mensaje": "¡Error! El id del evento deseada para su listado es incorrecto."}, status = 404)

@require_http_methods(["POST"])
@csrf_exempt
def crear_comentario(request):

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

    if request.method == "POST":
        # Verificación de si el usuario está autenticado
        autenticado = request.GET.get("autenticado", "false").lower() == "true"
        if  not autenticado:
            return JsonResponse({"mensaje": "No se le permite a usuarios no autenticados crear comentarios."}, status= 403)
        else:
            # Procesar el cuerpo de la solicitud para crear el comentario
            diccionario_comentario = json.loads(request.body)
            nombre_usuario = diccionario_comentario["usuario"]
            # Verificar si el usuario existe en la base de datos
            objeto_usuario = UsuarioPersonalizado.objects.get(username = nombre_usuario)
            try:
                nombre_evento = diccionario_comentario["evento"]
                # Verificar si el evento existe en la base de datos
                objeto_evento = Evento.objects.get(nombre = nombre_evento)
                # Crear el comentario
                nuevo_comentario = Comentario.objects.create(
                    texto = diccionario_comentario["texto"],
                    fecha = diccionario_comentario["fecha"],
                    usuario =objeto_usuario,
                    evento = objeto_evento
                )
                return JsonResponse({"id": nuevo_comentario.id, "evento": objeto_evento.nombre,"mensaje": "El comentario se ha creado correctamente."}, status = 201)
            except Evento.DoesNotExist:
                    # Error si el evento no existe
                    return  JsonResponse({"mensaje":"El evento que se desea asociar en la creación del comentario no existe en nuestra base de datos."}, status = 404)


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

@require_http_methods(["POST"])
def login(request):

    """
       Vista para iniciar sesión de un usuario.

       Permite a los usuarios iniciar sesión proporcionando su nombre de usuario y contraseña.

       Parámetros del cuerpo de la solicitud (JSON):
       - username: El nombre de usuario del usuario (obligatorio).
       - password: La contraseña del usuario (obligatoria).

       Respuesta:
       - Si el nombre de usuario y la contraseña son correctos, se devuelve un mensaje de éxito indicando que el usuario ha iniciado sesión con éxito.
       - Si el nombre de usuario no existe o la contraseña es incorrecta, se devuelve un error de autenticación indicando el problema.

       Respuesta de error:
       - Si las credenciales son incorrectas (ya sea el nombre de usuario o la contraseña), se devuelve un error con código de estado 401 (No autorizado) y un mensaje de error correspondiente.
       """
    if request.method == "POST":
        diccionario_usuario = json.loads(request.body)
        nombre_usuario =  diccionario_usuario["username"]
        pass_usuario =  diccionario_usuario["password"]

        # Se obtienen los datos de la solicitud
        if comprobar_username(nombre_usuario) :
            # Verificar si la contraseña es correcta
            if comprobar_contrasena(pass_usuario):
                return JsonResponse({"usuario":nombre_usuario,"mensaje": "El usuario se ha logueado con éxito en el sistema."})
            else:
                # Si la contraseña es incorrecta
                return JsonResponse({"usuario":nombre_usuario, "mensaje": "La contraseña es incorrecta.No ha sido posible iniciar sesión."}, status = 401)
        else:
            # Si el nombre de usuario es incorrecto
            return  JsonResponse({"usuario":nombre_usuario, "mensaje":"El username es incorrecto. No ha sido posible iniciar sesión."}, status = 401)

@require_http_methods(["POST"])
@csrf_exempt
def register(request):

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

    if request.method == "POST":
        diccionario_usuario_alta = json.loads(request.body)
        nombre_usuario = diccionario_usuario_alta.get("username", "")
        pass_usuario = diccionario_usuario_alta.get("password", "")
        email_usuario = diccionario_usuario_alta.get("email", "")
        tipo_usuario = diccionario_usuario_alta.get("tipo_usuario", "").lower()
        print(tipo_usuario)
        biografia_usuario = diccionario_usuario_alta.get("biografia","")

        # Validación de campos obligatorios
        if nombre_usuario == "" or pass_usuario == "" or email_usuario == "" or tipo_usuario == "":
            return JsonResponse({"mensaje": "Se han dejado campo/s obligatorio/s sin rellenar. Recuerda que el único campo opcional es la biografía."}, status = 400)

        # Validación de que los datos sean únicos y tipo de usuario válido
        if tipo_usuario not in ["organizador","participante"]:
            return JsonResponse({"tipo_usuario": tipo_usuario, "mensaje": "El tipo de usuario es incorrecto, debería ser organizador o participante."})

        if comprobar_email(email_usuario):
            return JsonResponse({"email": email_usuario, "mensaje": "El email introducido ya está en uso."})

        if comprobar_username(nombre_usuario):
            return JsonResponse({"usuario": nombre_usuario, "mensaje": "El nombre de usuario introducido ya está en uso." })

        if comprobar_contrasena(pass_usuario):
            return JsonResponse({"mensaje": "La contraseña introducida ya está en uso"})
        # Creación del nuevo usuario
        nuevo_usuario = UsuarioPersonalizado.objects.create(
            username = nombre_usuario,
            password = pass_usuario,
            email = email_usuario,
            tipo = tipo_usuario,
            biografia = biografia_usuario
        )
        return JsonResponse({"usuario": nuevo_usuario.username, "email": nuevo_usuario.password, "mensaje": "El usuario ha sido dado de alta con éxito."}, status = 201)