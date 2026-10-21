class Torneo:
    def __init__(self, id_torneo=None, nombre="", fecha_inicio="", fecha_fin="", categoria=""):
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.categoria = categoria
        self.reservas = []  

    def agregar_reserva_memoria(self, reserva):
        self.reservas.append(reserva)

    def cargar_reservas_desde_bd(self, reservas):
        self.reservas = reservas

    def __str__(self):
        return f"Torneo {self.nombre} ({self.categoria}) - {len(self.reservas)} reservas"