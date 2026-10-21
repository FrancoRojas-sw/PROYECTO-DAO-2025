import sqlite3
from pathlib import Path
from datetime import datetime
import random

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "dao_canchas.db"

def crear_tablas():
    """Crea las tablas si no existen."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Cliente
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    
    # Cancha
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cancha (
            id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            tipo_superficie TEXT NOT NULL,
            iluminacion BOOLEAN NOT NULL,
            precio_hora REAL NOT NULL,
            servicios TEXT
        )
    """)
    
    # Horario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horario (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            UNIQUE(hora_inicio, hora_fin)
        )
    """)
    
    # Reserva
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reserva (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            id_cliente INTEGER NOT NULL,
            id_cancha INTEGER NOT NULL,
            id_horario INTEGER NOT NULL,
            monto REAL NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
            FOREIGN KEY (id_cancha) REFERENCES cancha(id_cancha),
            FOREIGN KEY (id_horario) REFERENCES horario(id_horario),
            UNIQUE(fecha, id_cancha, id_horario)
        )
    """)
    
    # Pago
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pago (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            id_reserva INTEGER NOT NULL,
            fecha_pago DATE NOT NULL,
            monto REAL NOT NULL,
            metodo TEXT NOT NULL,
            FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva) ON DELETE CASCADE
        )
    """)
    
    conexion.commit()
    conexion.close()
    print(" Tablas creadas/verificadas")

def poblar():
    """Pobla la BD con datos de prueba."""
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()
    
    # Limpiar datos existentes (en orden inverso de dependencias)
    print(" Limpiando datos existentes...")
    cursor.execute("DELETE FROM pago")
    cursor.execute("DELETE FROM torneo_reserva")  # Eliminar asociaciones torneo-reserva
    cursor.execute("DELETE FROM reserva")
    cursor.execute("DELETE FROM torneo")
    cursor.execute("DELETE FROM cancha_servicio")  # Eliminar asociaciones cancha-servicio
    cursor.execute("DELETE FROM servicio")
    cursor.execute("DELETE FROM horario")
    cursor.execute("DELETE FROM cancha")
    cursor.execute("DELETE FROM cliente")
    cursor.execute("UPDATE sqlite_sequence SET seq=0")  # Resetear secuencias
    
    # Clientes - Aumentar cantidad
    print(" Insertando clientes...")
    nombres = ["Juan", "María", "Carlos", "Ana", "Pedro", "Laura", "Diego", "Sofía", 
               "Martín", "Valeria", "Lucas", "Camila", "Mateo", "Isabella", "Santiago",
               "Susana", "Federico", "Florencia", "Nicolás", "Catalina", "Sebastián",
               "Micaela", "Gabriel", "Lucía", "Tomás", "Victoria", "Facundo", "Julieta"]
    apellidos = ["González", "Rodríguez", "Fernández", "López", "Martínez", "García", 
                 "Pérez", "Sánchez", "Romero", "Torres", "Álvarez", "Díaz", "Moreno",
                 "Vayra", "Carrizo", "Ruiz", "Hernández", "Jiménez", "Flores", "Castro"]
    
    clientes = []
    for i in range(30):  # 30 clientes
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        telefono = f"11{random.randint(10000000, 99999999)}"
        email = f"{nombre.lower()}.{apellido.lower()}{i}@email.com"
        clientes.append((nombre, apellido, telefono, email))
    
    for nombre, apellido, telefono, email in clientes:
        try:
            cursor.execute(
                "INSERT INTO cliente (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
                (nombre, apellido, telefono, email)
            )
        except sqlite3.IntegrityError:
            pass  # Si hay duplicado, continuar
    print(f" {len(clientes)} clientes insertados")
    
    # Canchas
    print(" Insertando canchas...")
    canchas = [
        ("Cancha 1 - Pádel", "pádel", True, 45000.0, "red de pádel, pelotas"),
        ("Cancha 2 - Tenis", "tenis", True, 75000.0, "red de tenis, pelotas, con luz"),
        ("Cancha 3 - Futsal Interior", "futsal", False, 45000.0, "red de futsal, sintético"),
        ("Cancha 4 - Fútbol Sintético", "fútbol", True, 60000.0, "sintético, con luz"),
        ("Cancha 5 - Vóley", "vóley", True, 42000.0, "red de vóley, cancha interior"),
        ("Cancha 6 - Básquet", "básquet", True, 42000.0, "tableros, pelotas, cancha interior"),
        ("Cancha 7 - Fútbol 5 Sintético", "fútbol", False, 55000.0, "sintético, cancha 5v5"),
        ("Cancha 8 - Fútbol 7 Sintético", "fútbol", True, 65000.0, "sintético, con luz, cancha 7v7"),
    ]
    for nombre, tipo, iluminacion, precio, servicios in canchas:
        cursor.execute(
            "INSERT INTO cancha (nombre, tipo_superficie, iluminacion, precio_hora, servicios) VALUES (?, ?, ?, ?, ?)",
            (nombre, tipo, int(iluminacion), precio, servicios)
        )
    print(f" {len(canchas)} canchas insertadas")
    
    # Horarios
    print(" Insertando horarios...")
    horarios = [
        ("08:00", "09:00"),
        ("09:00", "10:00"),
        ("10:00", "11:00"),
        ("11:00", "12:00"),
        ("12:00", "13:00"),
        ("14:00", "15:00"),
        ("15:00", "16:00"),
        ("16:00", "17:00"),
        ("17:00", "18:00"),
        ("18:00", "19:00"),
        ("19:00", "20:00"),
        ("20:00", "21:00"),
    ]
    for inicio, fin in horarios:
        cursor.execute(
            "INSERT INTO horario (hora_inicio, hora_fin) VALUES (?, ?)",
            (inicio, fin)
        )
    print(f" {len(horarios)} horarios insertados")
    
    # Reservas - Muchas más reservas distribuidas
    print(" Insertando reservas...")
    from datetime import timedelta, date
    
    # Generar fechas de los últimos 3 meses
    fechas = []
    fecha_inicio = date(2025, 9, 1)
    fecha_fin = date(2025, 11, 30)
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        fechas.append(fecha_actual.strftime("%Y-%m-%d"))
        fecha_actual += timedelta(days=1)
    
    reservas_count = 0
    estados = ["confirmada", "confirmada", "confirmada", "pendiente", "cancelada"]  # Mayoría confirmadas
    
    # Obtener cantidad de clientes y canchas insertados
    cursor.execute("SELECT COUNT(*) FROM cliente")
    total_clientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM cancha")
    total_canchas = cursor.fetchone()[0]
    
    # Generar muchas reservas aleatorias
    for _ in range(150):  # Intentar crear 150 reservas
        fecha = random.choice(fechas)
        cliente_id = random.randint(1, total_clientes)
        cancha_id = random.randint(1, total_canchas)
        horario_id = random.randint(1, len(horarios))
        
        # Monto según la cancha
        cursor.execute("SELECT precio_hora FROM cancha WHERE id_cancha = ?", (cancha_id,))
        precio = cursor.fetchone()[0]
        monto = precio
        
        estado = random.choice(estados)
        
        try:
            cursor.execute(
                "INSERT INTO reserva (fecha, id_cliente, id_cancha, id_horario, monto, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (fecha, cliente_id, cancha_id, horario_id, monto, estado)
            )
            reservas_count += 1
        except sqlite3.IntegrityError:
            # Si hay conflicto de horario/cancha, continuar
            pass
    print(f" {reservas_count} reservas insertadas")
    
    # Pagos - Generar para la mayoría de reservas confirmadas
    print(" Insertando pagos...")
    cursor.execute("SELECT id_reserva, monto FROM reserva WHERE estado = 'confirmada'")
    reservas_confirmadas = cursor.fetchall()
    
    pagos_count = 0
    metodos = ["transferencia", "efectivo", "tarjeta", "mercado pago", "efectivo"]
    
    # Crear pagos para 80% de las reservas confirmadas
    for reserva_id, monto in reservas_confirmadas:
        if random.random() < 0.8:  # 80% de probabilidad
            metodo = random.choice(metodos)
            # Fecha de pago aleatoria cercana a la reserva
            dias_offset = random.randint(0, 5)
            fecha_pago = (date.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            
            try:
                cursor.execute(
                    "INSERT INTO pago (id_reserva, fecha_pago, monto, metodo) VALUES (?, ?, ?, ?)",
                    (reserva_id, fecha_pago, monto, metodo)
                )
                pagos_count += 1
            except sqlite3.IntegrityError:
                pass
    print(f" {pagos_count} pagos insertados")
    
    # TORNEOS - Nuevas secciones
    print(" Insertando torneos...")
    torneos = [
        ("Torneo de Pádel Verano 2025", "2025-12-01", "2025-12-15", "Pádel"),
        ("Copa de Tenis Abierta", "2025-12-10", "2025-12-20", "Tenis"),
        ("Futsal Challenge 2025", "2025-11-25", "2025-12-05", "Futsal"),
        ("Clásico de Vóley", "2025-11-20", "2025-11-30", "Vóley"),
        ("Torneo de Básquet Zona Norte", "2025-12-01", "2025-12-22", "Básquet"),
        ("Torneo de Pádel Mixto", "2025-12-08", "2025-12-18", "Pádel Mixto"),
        ("Campeonato de Tenis Dobles", "2025-12-15", "2025-12-25", "Tenis Dobles"),
        ("Futsal Femenino", "2025-12-02", "2025-12-12", "Futsal"),
        ("Vóley Masculino", "2025-11-28", "2025-12-08", "Vóley"),
        ("Básquet 3x3", "2025-12-05", "2025-12-15", "Básquet"),
    ]
    
    for nombre, fecha_inicio, fecha_fin, categoria in torneos:
        cursor.execute(
            "INSERT INTO torneo (nombre, fecha_inicio, fecha_fin, categoria) VALUES (?, ?, ?, ?)",
            (nombre, fecha_inicio, fecha_fin, categoria)
        )
    print(f" {len(torneos)} torneos insertados")
    
    # Asignar reservas a torneos (algunas reservas confirmadas)
    print(" Asignando reservas a torneos...")
    cursor.execute("SELECT id_reserva FROM reserva WHERE estado = 'confirmada' LIMIT 30")
    reservas_para_torneos = cursor.fetchall()
    
    torneos_count = len(torneos)
    asignaciones = 0
    
    for i, (reserva_id,) in enumerate(reservas_para_torneos):
        torneo_id = (i % torneos_count) + 1  # Distribuir entre torneos
        try:
            cursor.execute(
                "INSERT INTO torneo_reserva (id_torneo, id_reserva) VALUES (?, ?)",
                (torneo_id, reserva_id)
            )
            asignaciones += 1
        except sqlite3.IntegrityError:
            pass  # Ya está asignada
    print(f" {asignaciones} reservas asignadas a torneos")
    
    conexion.commit()
    conexion.close()

def main():
    print("\n INICIANDO POBLACIÓN DE BASE DE DATOS")
    print()
    
    try:
        crear_tablas()
        poblar()

        print()
        print("\n BASE DE DATOS POBLADA EXITOSAMENTE")
        print("\n Ahora podes abrir la app y visualizar todos los reportes con los datos reales.\n")
        
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()