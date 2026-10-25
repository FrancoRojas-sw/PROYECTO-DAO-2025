from repositories.pago_repository import PagoRepository
from repositories.reserva_repository import ReservaRepository
from repositories.conexion import obtener_conexion
from models.pago import Pago

class PagoService: #Lógica de negocio asociada a los pagos de reservas.

    @staticmethod
    def registrar_pago(reserva, monto, metodo):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        saldo_pendiente = PagoService.calcular_saldo_pendiente(reserva.id_reserva) # Obtener saldo pendiente
        
        if monto > saldo_pendiente:
            raise ValueError(f" El monto excede el saldo pendiente (${saldo_pendiente:.2f})")

        pago = Pago(
            monto=monto,
            metodo=metodo,
            reserva=reserva
        )

        PagoRepository.registrar(pago)
        print(f" Pago registrado por ${monto} ({metodo}) para reserva #{reserva.id_reserva}")
        
        nuevo_saldo = saldo_pendiente - monto
        
        if nuevo_saldo == 0:
            reserva.estado = "confirmada"
            print(f" Reserva #{reserva.id_reserva} completamente pagada")
        else:
            reserva.estado = "seña"
            print(f" Reserva #{reserva.id_reserva} con seña. Saldo pendiente: ${nuevo_saldo:.2f}")
        
        ReservaRepository.actualizar(reserva)

    @staticmethod
    def calcular_saldo_pendiente(id_reserva):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("SELECT monto FROM reserva WHERE id_reserva = ?", (id_reserva,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Reserva no encontrada")
            
            monto_total = resultado[0]
            
            cursor.execute("SELECT SUM(monto) FROM pago WHERE id_reserva = ?", (id_reserva,))
            resultado_pagos = cursor.fetchone()
            total_pagado = resultado_pagos[0] if resultado_pagos[0] else 0
            
            conexion.close()
            
            saldo_pendiente = monto_total - total_pagado
            return max(0, saldo_pendiente)  # No permitir saldos negativos
        except Exception as e:
            print(f"Error al calcular saldo pendiente: {e}")
            return 0

    @staticmethod
    def obtener_detalles_pago(id_reserva):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("SELECT monto FROM reserva WHERE id_reserva = ?", (id_reserva,))
            monto_total = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(monto) FROM pago WHERE id_reserva = ?", (id_reserva,))
            resultado = cursor.fetchone()
            total_pagado = resultado[0] if resultado[0] else 0
            
            conexion.close()
            
            saldo_pendiente = monto_total - total_pagado
            return {
                "monto_total": monto_total,
                "total_pagado": total_pagado,
                "saldo_pendiente": max(0, saldo_pendiente)
            }
        except Exception as e:
            print(f"Error al obtener detalles de pago: {e}")
            return {"monto_total": 0, "total_pagado": 0, "saldo_pendiente": 0}

    @staticmethod
    def eliminar_pago(id_pago):
        pago_data = PagoRepository.obtener_por_id(id_pago)
        if not pago_data:
            raise ValueError("Pago no encontrado.")
        
        id_reserva = pago_data[4]  # id_reserva está en índice 4
        
        reserva = ReservaRepository.obtener_por_id(id_reserva)
        if not reserva:
            raise ValueError("Reserva asociada no encontrada.")
        
        PagoRepository.eliminar(id_pago)
        print(f" Pago #{id_pago} eliminado correctamente")
        
        saldo_pendiente = PagoService.calcular_saldo_pendiente(id_reserva)
        if saldo_pendiente > 0:
            reserva.estado = "seña" if saldo_pendiente < PagoService.obtener_detalles_pago(id_reserva)["monto_total"] else "pendiente"
            if saldo_pendiente == PagoService.obtener_detalles_pago(id_reserva)["monto_total"]:
                reserva.estado = "pendiente"
        else:
            reserva.estado = "confirmada"
        
        ReservaRepository.actualizar(reserva)
        print(f" Estado de reserva #{id_reserva} actualizado")

    @staticmethod
    def obtener_pagos_ordenados():
        try:
            return PagoRepository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener pagos: {e}")
            return []

    @staticmethod
    def filtrar_por_cancha(id_cancha):
        try:
            return PagoRepository.filtrar_por_cancha(id_cancha)
        except Exception as e:
            print(f"Error al filtrar por cancha: {e}")
            return []

    @staticmethod
    def filtrar_por_metodo(metodo):
        try:
            return PagoRepository.filtrar_por_metodo(metodo)
        except Exception as e:
            print(f"Error al filtrar por método: {e}")
            return []

    @staticmethod
    def filtrar_por_cancha_y_metodo(id_cancha, metodo):
        try:
            return PagoRepository.filtrar_por_cancha_y_metodo(id_cancha, metodo)
        except Exception as e:
            print(f"Error al filtrar pagos: {e}")
            return []