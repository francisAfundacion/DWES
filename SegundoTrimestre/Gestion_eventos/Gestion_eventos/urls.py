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
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='api_token_auth'),
    path('listar_eventos/',listar_eventosAPIView.as_view()),
    path('crear_evento', crear_eventoAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('actualizar_evento/<int:id>',actualizar_eventoAPIView.as_view()),
    path('eliminar_evento/<int:id>', eliminar_eventoAPIView.as_view()),
   # path('login', loginAPIView.as_view()),
    #path('listar_reservas', views.listar_reservas),
    #path('crear_reserva', views.crear_reserva),
    #path('actualizar_reserva/<int:id>', views.actualizar_reserva),
    #path('eliminar_reserva/<int:id>', views.eliminar_reserva),
    #path('listar_comentario/evento/<int:id>', views.listar_comentarios),
    #path('crear_comentario', views.crear_comentario),
    #path('login', views.login),
    #path('register', views.register),
    #path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
]
