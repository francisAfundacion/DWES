class Monstruo:
    def __init__(self, nombre, ataque, defensa, salud):
        """
        Constructor que inicializa un monstruo con valores específicos.

        Parámetros:
        nombre (str): El nombre del monstruo.
        ataque (int): El valor de ataque del monstruo.
        defensa (int): El valor de defensa del monstruo.
        salud (int): La salud del monstruo.
        """
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.salud = salud

    def get_nombre(self):
        """
        Obtiene el nombre del monstruo.

        Retorna:
        str: El nombre del monstruo.
        """
        return self.nombre
    
    def set_nombre(self, nombre):
        """
        Establece un nuevo nombre al monstruo.

        Parámetros:
        nombre (str): El nuevo nombre del monstruo.
        """
        self.nombre = nombre

    def get_ataque(self):
        """
        Obtiene el valor de ataque del monstruo.

        Retorna:
        int: El valor de ataque del monstruo.
        """
        return self.ataque
    
    def set_ataque(self, ataque):
        """
        Establece un nuevo valor de ataque al monstruo.

        Parámetros:
        ataque (int): El nuevo valor de ataque.
        """
        self.ataque = ataque

    def get_defensa(self):
        """
        Obtiene el valor de defensa del monstruo.

        Retorna:
        int: El valor de defensa del monstruo.
        """
        return self.defensa

    def set_defensa(self, defensa):
        """
        Establece un nuevo valor de defensa al monstruo.

        Parámetros:
        defensa (int): El nuevo valor de defensa.
        """
        self.defensa = defensa
    
    def get_salud(self):
        """
        Obtiene el valor de salud del monstruo.

        Retorna:
        int: El valor de salud del monstruo.
        """
        return self.salud
    
    def set_salud(self, salud):
        """
        Establece un nuevo valor de salud al monstruo.

        Parámetros:
        salud (int): El nuevo valor de salud.
        """
        self.salud = salud

    def atacar(self, heroe):
        """
        El monstruo ataca al héroe, infligiendo daño si el ataque es mayor que la defensa del héroe.

        Parámetros:
        heroe (Heroe): El objeto héroe que recibe el ataque.

        Si el ataque del monstruo supera la defensa del héroe, se calcula el daño y se reduce la salud del héroe.
        Si el ataque es bloqueado por la defensa, se muestra un mensaje.
        """
        from heroe import Heroe
        print(f"El monstruo {self.nombre} ataca a {heroe.get_nombre()}.")
        if (self.ataque > heroe.get_defensa()):
            dano_recibido = (self.ataque - heroe.get_defensa())
            if (heroe.get_salud() - dano_recibido < 0):
                heroe.set_salud(0)
            else:
                heroe.set_salud(heroe.get_salud() - dano_recibido)
            print(f"El héroe {heroe.get_nombre()} ha recibido {dano_recibido} puntos de daño.")
            print(f"Salud actual del héroe {heroe.get_salud()} después de recibir daño.")
        else:
            print("El héroe ha bloqueado el ataque.")

    def esta_vivo(self):
        """
        Verifica si el monstruo está vivo.

        Retorna:
        bool: True si el monstruo tiene salud mayor a 0, False si la salud es 0 o menor.
        """
        return self.salud > 0
    