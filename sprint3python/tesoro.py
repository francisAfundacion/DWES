
class Tesoro:
    def __init__(self):
        """
        Constructor que inicializa un tesoro con una lista de beneficios posibles.

        Atributos:
        beneficios: Lista de posibles beneficios que el héroe puede obtener al interactuar con el tesoro.                   
        """
        self.beneficios = ["Aumento de ataque", "Aumento de defensa", "Restauración de salud"]
    
    def get_beneficios(self):
        """
        Obtiene la lista de beneficios disponibles del tesoro.

        Retorna:
        beneficios: La lista de beneficios que puede obtener el héroe.
        """
        return self.beneficios