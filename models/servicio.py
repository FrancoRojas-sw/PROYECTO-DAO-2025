class Servicio:
    def __init__(self, id_servicio=None, nombre="", costo=0.0):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.costo = costo

    def __str__(self):
        return f"{self.nombre} (${self.costo})"

    def es_valido(self):
        return bool(self.nombre and self.costo >= 0)