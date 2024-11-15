def suma(num1, num2):
    """
    Función que suma dos números.

    Esta función recibe dos parámetros numéricos, los suma y retorna el resultado.

    Parámetros:
    num1 (int, float): Primer número a sumar.
    num2 (int, float): Segundo número a sumar.

    Retorna:
    int, float: El resultado de la suma de los dos números proporcionados.
    """
    return num1 + num2

def resta(num1, num2):
    """
    Función que resta dos números.

    Esta función recibe dos parámetros numéricos, realiza la resta entre ellos y retorna el resultado.

    Parámetros:
    num1 (int, float): Primer número, del cual se le restará el segundo número.
    num2 (int, float): Segundo número, que será restado al primero.

    Retorna:
    int, float: El resultado de la resta entre los dos números proporcionados.
    """
    return num1 - num2

def multiplicacion(num1, num2):
    """
    Función que multiplica dos números.

    Esta función recibe dos parámetros numéricos, los multiplica y retorna el resultado.

    Parámetros:
    num1 (int, float): Primer número a multiplicar.
    num2 (int, float): Segundo número a multiplicar.

    Retorna:
    int, float: El resultado de la multiplicación de los dos números proporcionados.
    """
    return num1 * num2

def division(num1, num2):
    """
    Función que divide dos números.

    Esta función recibe dos parámetros numéricos, realiza la división entre ellos y retorna el resultado.
    Si el denominador es 0, se maneja una excepción y se devuelve un mensaje de error.

    Parámetros:
    num1 (int, float): Numerador de la división.
    num2 (int, float): Denominador de la división.

    Retorna:
    int, float o str: El resultado de la división entre los dos números proporcionados. Si el denominador es 0,
                      retorna un mensaje de error indicando que no es posible dividir por 0.
    """
    try:
        resultado = num1 / num2
    except ZeroDivisionError:
        resultado = "No se puede efectuar divisiones, cuando el denominador presenta el valor 0"
    return resultado
    