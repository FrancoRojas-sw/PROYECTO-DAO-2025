from datetime import datetime

class Reserva:
    def __init__(self, id_reserva=None, fecha=None, cliente=None, cancha=None, horario=None, monto=0.0, estado="pendiente"):
        self.id_reserva = id_reserva
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.cliente = cliente
        self.cancha = cancha
        self.horario = horario
        self.monto = monto
        self.estado = estado

    def __str__(self):
        return f"Reserva #{self.id_reserva} - {self.cliente} - {self.cancha} - {self.fecha}"

    def confirmar(self):
        self.estado = "confirmada"

    def cancelar(self):
        self.estado = "cancelada"