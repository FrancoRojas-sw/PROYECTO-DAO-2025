from repositories.cancha_repository import CanchaRepository
from models.cancha import Cancha

class CanchaService: #Reglas de negocio para gestión de canchas deportivas.

    @staticmethod
    def registrar_cancha(nombre, tipo_superficie, iluminacion, precio_hora, servicios=""):
        if not nombre or precio_hora <= 0:
            raise ValueError("Datos inválidos para crear la cancha.")
        
        nueva = Cancha(
            nombre=nombre,
            tipo_superficie=tipo_superficie,
            iluminacion=iluminacion,
            precio_hora=precio_hora,
            servicios=servicios
        )
        CanchaRepository.crear(nueva)
        print(f" Cancha registrada: {nueva}")

    @staticmethod
    def listar_canchas():
        return CanchaRepository.obtener_todas()

    @staticmethod
    def modificar_cancha(id_cancha, nombre, tipo_superficie, iluminacion, precio_hora, servicios=""):
        if not nombre or precio_hora <= 0:
            raise ValueError("Datos inválidos para modificar la cancha.")
        
        cancha_actualizada = Cancha(
            id_cancha=id_cancha,
            nombre=nombre,
            tipo_superficie=tipo_superficie,
            iluminacion=iluminacion,
            precio_hora=precio_hora,
            servicios=servicios
        )
        CanchaRepository.actualizar(cancha_actualizada)
        print(f" Cancha modificada: {cancha_actualizada}")

    @staticmethod
    def eliminar_cancha(id_cancha):
        CanchaRepository.eliminar(id_cancha)
        print(f" Cancha eliminada (ID {id_cancha})")