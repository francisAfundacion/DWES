"""
URL configuration for Gestion_eventos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.authtoken.views import ObtainAuthToken
from webeventosapp.views import listar_eventosAPIView
from webeventosapp.views import crear_eventoAPIView
from webeventosapp.views import actualizar_eventoAPIView
from webeventosapp.views import eliminar_eventoAPIView
from webeventosapp.views import listar_reservasAPIView
from webeventosapp.views import eliminar_reservasAPIView
from webeventosapp.views import crear_reservaAPIView
from webeventosapp.views import actualizar_reservaAPIView
from webeventosapp.views import listar_comentariosAPIView
from webeventosapp.views import crear_comentarioAPIView
from webeventosapp.views import registerAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from django.contrib import admin
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentación",
        default_version="v1",
        description="Documentación de la API",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='api_token_auth'),
    path('listar_eventos/',listar_eventosAPIView.as_view()),
    path('crear_evento', crear_eventoAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('actualizar_evento/<int:id>',actualizar_eventoAPIView.as_view()),
    path('eliminar_evento/<int:id>', eliminar_eventoAPIView.as_view()),
    path('listar_reservas', listar_reservasAPIView.as_view()),
    path('crear_reserva', crear_reservaAPIView.as_view()),
    path('actualizar_reserva/<int:id>', actualizar_reservaAPIView.as_view()),
    path('eliminar_reserva/<int:id>', eliminar_reservasAPIView.as_view() ),
    path('listar_comentario/evento/<int:id>', listar_comentariosAPIView.as_view()),
    path('crear_comentario', crear_comentarioAPIView.as_view()),
    path('register', registerAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
