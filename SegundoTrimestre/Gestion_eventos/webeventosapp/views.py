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
            return JsonResponse({"mensaje": "¡Error! No existe el id de la reserva que se desea eliminar."},status=404)
        else:
            return JsonResponse({"mensaje": "¡Error! El tipo de usuario no es participante. No podrá eliminar reservas."}, status=403)

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
        if not autenticado:
            return JsonResponse({"mensaje": "No se le permite a usuarios no autenticados crear comentarios."},
                                status=403)
        else:
            # Procesar el cuerpo de la solicitud para crear el comentario
            diccionario_comentario = json.loads(request.body)
            nombre_usuario = diccionario_comentario["usuario"]
            # Verificar si el usuario existe en la base de datos
            objeto_usuario = UsuarioPersonalizado.objects.get(username=nombre_usuario)
            try:
                nombre_evento = diccionario_comentario["evento"]
                # Verificar si el evento existe en la base de datos
                objeto_evento = Evento.objects.get(nombre=nombre_evento)
                # Crear el comentario
                nuevo_comentario = Comentario.objects.create(
                    texto=diccionario_comentario["texto"],
                    fecha=diccionario_comentario["fecha"],
                    usuario=objeto_usuario,
                    evento=objeto_evento
                )
                return JsonResponse({"id": nuevo_comentario.id, "evento": objeto_evento.nombre,
                                     "mensaje": "El comentario se ha creado correctamente."}, status=201)
            except Evento.DoesNotExist:
                # Error si el evento no existe
                return JsonResponse({"mensaje": "El evento que se desea asociar en la creación del comentario no existe en nuestra base de datos."},status=404)

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

@csrf_exempt
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