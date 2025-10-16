# entities/player.py

class Player:
    def __init__(self, name="Jugador"):
        self.name = name
        self.score = 0

    def atender_alerta(self, alerta):
        print(f"{self.name} atendió una alerta: {alerta}")
