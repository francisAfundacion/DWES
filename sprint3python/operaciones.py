#1. Crea una carpeta llamada sprint3python en tu repositorio. Añade un archivo de
#código operaciones.py que contenga funciones para las operaciones suma, resta,
#multiplicación y división (controla división por 0). Haz commit y push.

def suma (num1, num2): 
    return num1+num2
def resta (num1, num2):
    return num1-num2
def multiplicacion (num1, num2):
    return num1*num2
def division (num1, num2):
    try:
        resultado = num1 / num2
        return resultado
    except ZeroDivisionError:
        resultado = "No se puede efectuar divisiones, cuando el denominador presenta el valor 0



    