from monstruo import Monstruo

class Heroe:
    def __init__(self, nombre):
        """
        Constructor que inicializa un héroe con valores predeterminados, excepto su nombre.

        Parámetros:
        nombre (str): El nombre del héroe.

        Atributos:
        ataque (int): Valor inicial del ataque (predeterminado a 12).
        defensa (int): Valor inicial de la defensa (predeterminado a 8).
        salud (int): Salud actual del héroe (predeterminado a 100).
        salud_maxima (int): Salud máxima del héroe (predeterminado a 100).
        """
        self.nombre = nombre
        self.ataque = 12
        self.defensa = 8
        self.salud = 100
        self.salud_maxima = 100

    def get_nombre(self):
        """
        Obtiene el nombre del héroe.

        Retorna:
        str: El nombre del héroe.
        """
        return self.nombre
    
    def set_nombre(self, nombre):
        """
        Establece un nuevo nombre al héroe.

        Parámetros:
        nombre (str): El nuevo nombre del héroe.
        """
        self.nombre = nombre
    
    def get_ataque(self):
        """
        Obtiene el valor de ataque del héroe.

        Retorna:
        int: El valor de ataque del héroe.
        """
        return self.ataque
    
    def set_ataque(self, ataque):
        """
        Establece un nuevo valor de ataque al héroe.

        Parámetros:
        ataque (int): El nuevo valor de ataque.
        """
        self.ataque = ataque

    def get_defensa(self):
        """
        Obtiene el valor de defensa del héroe.

        Retorna:
        int: El valor de defensa del héroe.
        """
        return self.defensa
    
    def set_defensa(self, defensa):
        """
        Establece un nuevo valor de defensa al héroe.

        Parámetros:
        defensa (int): El nuevo valor de defensa.
        """
        self.defensa = defensa
    
    def get_salud(self):
        """
        Obtiene el valor de salud del héroe.

        Retorna:
        int: El valor de salud del héroe.
        """
        return self.salud
    
    def set_salud(self, salud):
        """
        Establece un nuevo valor de salud al héroe.

        Parámetros:
        salud (int): El nuevo valor de salud.
        """
        self.salud = salud
    
    def get_salud_maxima(self):
        """
        Obtiene el valor de salud máxima del héroe.

        Retorna:
        int: El valor de salud máxima.
        """
        return self.salud_maxima
       
    def atacar(self, enemigo):
        """
        Realiza un ataque al enemigo, infligiendo daño si el ataque supera la defensa del enemigo.

        Parámetros:
        enemigo (Monstruo): El objeto enemigo que recibe el ataque.

        Si el ataque es mayor que la defensa del enemigo, se calcula el daño e impacta la salud del enemigo.
        """
        if self.ataque > enemigo.get_defensa():
            dano_infligido = abs(enemigo.get_defensa() - self.ataque)
            if (enemigo.get_salud() - dano_infligido < 0 ):
                enemigo.set_salud(0)
            else:
                enemigo.set_salud(enemigo.get_salud() - dano_infligido)
            print(f"El enemigo {enemigo.get_nombre()} ha recibido {dano_infligido} puntos de daño.")
        else:
            print(f"El enemigo ha bloqueado el ataque.")

    def curarse(self):
        """
        Cura al héroe, aumentando su salud en 5 puntos sin exceder la salud máxima.

        Si la salud del héroe no puede aumentar más, se ajusta al valor máximo.
        """
        CURACION = 5
        if (self.salud + CURACION <= self.salud_maxima):
            self.salud = self.salud + CURACION
        else:
            self.salud = self.salud_maxima
        print(f"Héroe se ha curado. Salud actual: {self.salud}")

    def defenderse(self):
        """
        Aumenta temporalmente la defensa del héroe en 5 puntos.

        La defensa del héroe se incrementa por un turno, mejorando su capacidad de resistir ataques.
        """
        INCREMENTO_DEFENSA = 5
        self.defensa = self.defensa + INCREMENTO_DEFENSA
        print(f"Héroe se defiende. Defensa aumentada temporalmente a {self.defensa}.")

    def reset_defensa(self):
        """
        Restaura la defensa del héroe a su valor original.

        La defensa se disminuye en 5 puntos para devolverla a su valor predeterminado.
        """
        DECREMENTO_DEFENSA = 5
        self.defensa = self.defensa - DECREMENTO_DEFENSA
        print(f"La defensa de {self.nombre} vuelve a la normalidad.")

    def esta_vivo(self):
        """
        Verifica si el héroe está vivo.

        Retorna:
        bool: True si la salud del héroe es mayor que 0, de lo contrario, False.
        """
        return self.salud > 0