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
from webeventosapp import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('listar_eventos', views.listar_eventos),
    path('crear_evento', views.crear_evento),
    path('admin/', admin.site.urls),
    path('actualizar_evento/<int:id>', views.actualizar_evento),
    path('eliminar_evento/<int:id>', views.eliminar_evento),
    path('listar_reservas', views.listar_reservas),
    path('crear_reserva', views.crear_reserva),
    path('actualizar_reserva/<int:id>', views.actualizar_reserva),
    path('eliminar_reserva/<int:id>', views.eliminar_reserva),
    path('listar_comentario/evento/<int:id>', views.listar_comentarios),
    path('crear_comentario', views.crear_comentario),
    path('login', views.login),
    path('register', views.register),
]
