from repositories.horario_repository import HorarioRepository
from models.horario import Horario


class HorarioService: #Servicio para registrar y listar horarios disponibles.

    @staticmethod
    def registrar_horario(hora_inicio, hora_fin):
        if not (hora_inicio and hora_fin):
            raise ValueError("Ambas horas son requeridas.")
        
        nuevo = Horario(None, hora_inicio, hora_fin)
        HorarioRepository.crear(nuevo)
        print(f" Horario registrado: {hora_inicio} - {hora_fin}")

    @staticmethod
    def listar_horarios():
        return HorarioRepository.obtener_todos()

    @staticmethod
    def modificar_horario(id_horario, hora_inicio, hora_fin): #Modifica un horario existente.
        if not (hora_inicio and hora_fin):
            raise ValueError("Ambas horas son requeridas.")
        
        horario_actualizado = Horario(id_horario, hora_inicio, hora_fin)
        HorarioRepository.actualizar(horario_actualizado)
        print(f" Horario modificado: {hora_inicio} - {hora_fin}")

    @staticmethod
    def eliminar_horario(id_horario):
        HorarioRepository.eliminar(id_horario)
        print(f" Horario eliminado (ID {id_horario})")