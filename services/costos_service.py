from repositories.costos_repository import CostosRepository

class CostosService: #Servicio para la gestión de reportes de costos y presupuestos.

    @staticmethod
    def obtener_ingresos_por_cancha():
        try:
            return CostosRepository.ingresos_por_cancha()
        except Exception as e:
            print(f" Error: {e}")
            return []

    @staticmethod
    def obtener_pagos_por_metodo():
        try:
            return CostosRepository.pagos_por_metodo()
        except Exception as e:
            print(f" Error: {e}")
            return []

    @staticmethod
    def obtener_estado_pagos():
        try:
            return CostosRepository.estado_pagos()
        except Exception as e:
            print(f" Error: {e}")
            return None

    @staticmethod
    def obtener_presupuesto_mensual():
        try:
            return CostosRepository.presupuesto_mensual()
        except Exception as e:
            print(f" Error: {e}")
            return []

    @staticmethod
    def obtener_ingresos_por_cliente():
        try:
            return CostosRepository.ingresos_por_cliente_top()
        except Exception as e:
            print(f" Error: {e}")
            return []

    @staticmethod
    def obtener_proyeccion():
        try:
            return CostosRepository.proyeccion_presupuesto()
        except Exception as e:
            print(f" Error: {e}")
            return None

    @staticmethod
    def obtener_resumen_cobranza():
        try:
            return CostosRepository.resumen_cobranza()
        except Exception as e:
            print(f" Error: {e}")
            return []