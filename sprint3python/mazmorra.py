from heroe import Heroe  # Importa la clase Heroe desde heroe.py

import random 

from monstruo import Monstruo  # Importa la clase Monstruo desde monstruo.py

from tesoro import Tesoro  # Importa la clase Tesoro desde tesoro.py

class Mazmorra:
    def __init__(self, heroe):
        """
        Constructor que inicializa una mazmorra con un héroe y una lista de monstruos.

        Parámetros:
        heroe (Heroe): El héroe que participará en la mazmorra.

        Atributos:
        heroe (Heroe): Referencia al objeto héroe.
        monstruos (list): Lista de monstruos que el héroe enfrentará.
        tesoro (Tesoro): Objeto Tesoro relacionado con los beneficios del héroe.
        """
        self.heroe = heroe
        self.monstruos = [
            Monstruo("Goblin", 10, 2, 20),
            Monstruo("Trol", 6, 7, 40),
            Monstruo("Caballero", 12, 10, 32),
            Monstruo("Banshee", 9, 12, 25),
            Monstruo("Esqueleto viviente", 3, 4, 28),
            Monstruo("Dragón legendario", 20, 15, 200)
        ]
        self.tesoro = Tesoro()

    def control_opciones_combate(self):
        """
        Controla las opciones de combate durante el enfrentamiento entre el héroe y el monstruo.

        Muestra un menú con las opciones disponibles para el héroe: Atacar, Defender o Curarse.

        Retorna:
        int: La opción seleccionada por el héroe (1 = Atacar, 2 = Defender, 3 = Curarse).
        """
        diccionario_opciones_combate = {
            1: "Atacar",
            2: "Defender",
            3: "Curarse"
        }
        valido = False
        while not valido:
            valido = True
            opcion_combate = int(input("¿Qué deseas hacer?\n1.Atacar.\n2.Defender.\n3.Curarse.\nTeclee opcion(1-3):"))

            if diccionario_opciones_combate.get(opcion_combate) is None:
                print("Opción no válida.")
                valido = False
        return opcion_combate

    def enfrentar_enemigo(self, enemigo):
        """
        Lógica para enfrentar a un enemigo en combate, alternando turnos entre el héroe y el monstruo.

        Parámetros:
        enemigo (Monstruo): El monstruo con el que el héroe combate.

        Retorna:
        bool: True si el monstruo ha sido derrotado, False si el héroe ha sido derrotado.
        """
        heroe_derrotado = False
        monstruo_derrotado = False
        while not heroe_derrotado and not monstruo_derrotado:
            if not self.heroe.esta_vivo():
                heroe_derrotado = True
            else:
                if not enemigo.esta_vivo():
                    monstruo_derrotado = True
                else:
                    entrada_opcion = self.control_opciones_combate() 
                    if entrada_opcion == 1:
                        self.heroe.atacar(enemigo)
                    elif entrada_opcion == 2:
                        self.heroe.defenderse()
                    elif entrada_opcion == 3:
                        self.heroe.curarse()

                enemigo.atacar(self.heroe)
                if entrada_opcion == 2:
                    self.heroe.reset_defensa()
                
        return monstruo_derrotado

    def buscar_tesoro(self):
        """
        Simula la búsqueda de un tesoro tras derrotar a un monstruo, generando un beneficio aleatorio.

        Retorna:
        int: Un valor aleatorio que representa el tipo de beneficio obtenido.
        """
        print("Buscando tesoro...")
        return random.choice(self.tesoro.get_beneficios())

    def jugar(self):
        """
        Inicia el juego de la mazmorra, en el que el héroe debe enfrentarse a los monstruos hasta derrotarlos a todos.

        Durante el juego, el héroe enfrentará a los monstruos, recibirá beneficios aleatorios al derrotarlos
        y actualizará sus estadísticas.
        """
        num_monstruos = len(self.monstruos)
        heroe_muerto = False
        monstruo_derrotado = False
        print("Héroe entra en la mazmorra.")

        while not heroe_muerto and num_monstruos > 0:
            print(f"Te has encontrado con un {self.monstruos[0].get_nombre()}")
            monstruo_derrotado = self.enfrentar_enemigo(self.monstruos[0])

            if monstruo_derrotado:
                print(f"{self.heroe.get_nombre()} ha derrotado a {self.monstruos[0].get_nombre()}")
                del (self.monstruos[0])
                beneficio_aleatorio = self.buscar_tesoro()
                self.sumar_estadisticas(beneficio_aleatorio)
                print(f"Estadísticas actuales del héroe: \nSalud: {self.heroe.get_salud()}.\nAtaque: {self.heroe.get_ataque()}.\nDefensa: {self.heroe.get_defensa()}.")
                num_monstruos -= 1
            else:
                heroe_muerto = True

        if not heroe_muerto:
            print(f"¡{self.heroe.get_nombre()} ha derrotado a todos los monstruos y ha conquistado la mazmorra!.")
        else:
            print("Héroe ha sido derrotado en la mazmorra.")

    def sumar_estadisticas(self, beneficio_aleatorio):
        """
        Suma o actualiza las estadísticas del héroe tras obtener un beneficio aleatorio.

        Parámetros:
        beneficio_aleatorio (int): El tipo de beneficio obtenido tras derrotar a un monstruo.
        """
        ADITIVO_STAT = 5

        if beneficio_aleatorio == "Aumento de ataque":
            self.heroe.set_ataque(self.heroe.get_ataque() + ADITIVO_STAT)
        elif beneficio_aleatorio == "Aumento de defensa":
            self.heroe.set_defensa(self.heroe.get_defensa() + ADITIVO_STAT)
        else:
            if self.heroe.get_salud() + ADITIVO_STAT <= 100:
                self.heroe.set_salud(self.heroe.get_salud() + ADITIVO_STAT)
            else:
                self.heroe.set_salud(self.heroe.get_salud_maxima())

def main():
    nombre_heroe = input("Introduzca nombre del héroe: ")
    heroe= Heroe(nombre_heroe)
    mazmorra_instancia = Mazmorra(heroe)
    mazmorra_instancia.jugar()

if __name__ == "__main__":
    main()