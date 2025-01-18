from django.db import models
# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class UsuarioPersonalizado(AbstractUser):
    TIPO_USUARIO = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante')
    ]
    tipo = models.CharField(max_length = 20, choices = TIPO_USUARIO)
    biografia = models.CharField(max_length = 300 ,null = True)

class Evento(models.Model):
    nombre = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 500)
    fecha = models.DateField()
    hora = models.TimeField()
    max_asistencias = models.IntegerField()
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete = models.CASCADE)

    def __str__ (self):
        return self.nombre

class Reserva(models.Model):
    TIPO_ESTADO = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ]
    estado = models.CharField(max_length = 20 , choices = TIPO_ESTADO ,default = "pendiente")
    entradas_reservadas = models.IntegerField()
    usuario = models.ForeignKey( UsuarioPersonalizado, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete = models.CASCADE)

class Comentario(models.Model):
    texto = models.CharField(max_length = 250)
    fecha = models.DateTimeField(default = datetime.now())
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete = models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete = models.CASCADE)



