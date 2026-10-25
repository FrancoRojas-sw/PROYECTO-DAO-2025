from repositories.torneo_repository import TorneoRepository
from models.torneo import Torneo


class TorneoService:  #Servicio para la gestión de torneos.
    
    @staticmethod
    def crear_torneo(nombre, fecha_inicio, fecha_fin, categoria): #Crea un nuevo torneo (sin reservas inicialmente).
        if not nombre:
            raise ValueError("El torneo debe tener nombre.")
        
        torneo = Torneo(None, nombre, fecha_inicio, fecha_fin, categoria)
        id_torneo = TorneoRepository.crear(torneo)
        print(f" Torneo creado: {nombre} ({categoria})")
        return id_torneo

    @staticmethod
    def listar_torneos():
        return TorneoRepository.obtener_todos()

    @staticmethod
    def asignar_reserva_a_torneo(id_torneo, id_reserva):
        try:
            TorneoRepository.asignar_reserva(id_torneo, id_reserva)
            print(f" Reserva #{id_reserva} asignada al torneo {id_torneo} (guardada en BD)")
            return True
        except ValueError as e:
            print(f" Validación: {e}")
            raise
        except Exception as e:
            print(f" Error al asignar reserva: {e}")
            raise

    @staticmethod
    def desasignar_reserva_de_torneo(id_torneo, id_reserva):
        try:
            TorneoRepository.desasignar_reserva(id_torneo, id_reserva)
            print(f" Reserva #{id_reserva} desasignada del torneo {id_torneo}")
            return True
        except Exception as e:
            print(f" Error al desasignar reserva: {e}")
            raise

    @staticmethod
    def obtener_reservas_torneo(id_torneo):
        try:
            reservas = TorneoRepository.obtener_reservas_de_torneo(id_torneo)
            print(f" Torneo {id_torneo} tiene {len(reservas)} reservas")
            return reservas
        except Exception as e:
            print(f" Error al obtener reservas del torneo: {e}")
            return []

    @staticmethod
    def eliminar_torneo(id_torneo):
        try:
            TorneoRepository.eliminar(id_torneo)
            print(f" Torneo eliminado (ID {id_torneo}) + sus relaciones (CASCADE)")
            return True
        except ValueError as e:
            print(f" Validación: {e}")
            raise
        except Exception as e:
            print(f" Error al eliminar torneo: {e}")
            raise