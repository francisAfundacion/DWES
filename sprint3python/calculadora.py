from operaciones import suma, resta, multiplicacion, division

# Bucle principal que permite al usuario realizar varias operaciones aritméticas.
otra_operacion = "s"
while otra_operacion == "s":
    resultado = 0
    numero_1 = int(input('Introduzca primer número para la operación aritmética deseada: '))
    numero_2 = int(input('Introduzca segundo número para la operación aritmética deseada: '))
    tipo_operacion = input('Introduzca tipo de operación que se desea realizar(suma, resta, multiplicacion, division): ')

    # Realiza la operación correspondiente según el tipo introducido por el usuario.
    if tipo_operacion == "suma":
        resultado = suma(numero_1, numero_2)
    elif tipo_operacion == "resta":
        resultado = resta(numero_1, numero_2)
    elif tipo_operacion == "multiplicacion":
        resultado = multiplicacion(numero_1, numero_2)
    elif tipo_operacion == "division":
        resultado = division(numero_1, numero_2)
    else:
        # Si el tipo de operación no es válido, se asigna un mensaje de error.
        resultado = "El tipo de operación introducido no es correcto."

    print(f"El resultado de la operación {tipo_operacion} entre los numeros {numero_1} y {numero_2} es de: {resultado}")
    otra_operacion = input("¿Desea realizar otra operación? s(para efectuar otra operación), n(para finalizar): ")

    # Valida la respuesta del usuario y asegura que solo se introduzcan "s" o "n".
    while otra_operacion != "s" and otra_operacion != "n":
        print("Ha introducido un valor diferente de los presentados(s o n).")
        otra_operacion = input("¿Desea realizar otra operación? s(para efectuar otra operación), n(para finalizar): ")

    if otra_operacion == "n":
        print("Ha finalizado el programa.")


