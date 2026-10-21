import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "dao_canchas.db"

def migrar_servicios():
    """Migra los servicios de texto a tablas normalizadas."""
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    
    try:
        print("📋 Iniciando migración de servicios...")
        
        # 1. Crear las nuevas tablas si no existen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicio (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                costo REAL NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cancha_servicio (
                id_cancha INTEGER NOT NULL,
                id_servicio INTEGER NOT NULL,
                PRIMARY KEY (id_cancha, id_servicio),
                FOREIGN KEY (id_cancha) REFERENCES cancha (id_cancha) ON DELETE CASCADE,
                FOREIGN KEY (id_servicio) REFERENCES servicio (id_servicio) ON DELETE CASCADE
            )
        """)
        
        # 2. Obtener todas las canchas con servicios
        cursor.execute("SELECT id_cancha, servicios FROM cancha WHERE servicios IS NOT NULL AND servicios != ''")
        canchas_con_servicios = cursor.fetchall()
        servicios_creados = {}
        total_asociaciones = 0
        
        # 3. Procesar cada cancha
        for id_cancha, servicios_texto in canchas_con_servicios:
            if not servicios_texto:
                continue
            # Dividir servicios por coma o punto y coma
            servicios_lista = [s.strip() for s in servicios_texto.replace(';', ',').split(',') if s.strip()]
            
            for servicio_nombre in servicios_lista:
                # Verificar si el servicio ya existe
                if servicio_nombre not in servicios_creados:
                    cursor.execute("SELECT id_servicio FROM servicio WHERE nombre = ?", (servicio_nombre,))
                    resultado = cursor.fetchone()
                    if resultado:
                        id_servicio = resultado[0]
                    else:
                        # Crear nuevo servicio con costo por defecto de 0
                        cursor.execute("INSERT INTO servicio (nombre, costo) VALUES (?, ?)", (servicio_nombre, 0.0))
                        id_servicio = cursor.lastrowid
                        print(f"Servicio creado: {servicio_nombre} (ID {id_servicio})")
                    servicios_creados[servicio_nombre] = id_servicio
                else:
                    id_servicio = servicios_creados[servicio_nombre]
                
                # Asociar servicio a cancha
                try:
                    cursor.execute(
                        "INSERT INTO cancha_servicio (id_cancha, id_servicio) VALUES (?, ?)",
                        (id_cancha, id_servicio)
                    )
                    total_asociaciones += 1
                except sqlite3.IntegrityError:
                    # Ya existe la asociación
                    pass
        
        conexion.commit()
        
        print(f"\n Migración completada:")
        print(f"   - Servicios únicos creados: {len(servicios_creados)}")
        print(f"   - Asociaciones cancha-servicio: {total_asociaciones}")
        print(f"\n Los servicios tienen costo $0.00 por defecto.")
        print(f"   Puedes actualizarlos desde la aplicación o manualmente en la BD.\n")
        
    except Exception as e:
        print(f" Error durante la migración: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def verificar_migracion():
    """Verifica el estado de la migración."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # Contar servicios
        cursor.execute("SELECT COUNT(*) FROM servicio")
        total_servicios = cursor.fetchone()[0]
        
        # Contar asociaciones
        cursor.execute("SELECT COUNT(*) FROM cancha_servicio")
        total_asociaciones = cursor.fetchone()[0]
        
        # Mostrar servicios
        cursor.execute("SELECT id_servicio, nombre, costo FROM servicio")
        servicios = cursor.fetchall()
        
        print("\n Estado actual de la base de datos:")
        print(f"   - Total de servicios: {total_servicios}")
        print(f"   - Total de asociaciones cancha-servicio: {total_asociaciones}")
        
        if servicios:
            print("\n Servicios registrados:")
            for id_serv, nombre, costo in servicios:
                cursor.execute(
                    "SELECT COUNT(*) FROM cancha_servicio WHERE id_servicio = ?",
                    (id_serv,)
                )
                num_canchas = cursor.fetchone()[0]
                print(f"   [{id_serv}] {nombre} - ${costo:.2f} (usado en {num_canchas} cancha(s))")
        
    except sqlite3.OperationalError as e:
        print(f" Tablas aún no existen: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    print("=" * 60)
    print(" MIGRACIÓN DE SERVICIOS A TABLAS NORMALIZADAS")
    print("=" * 60)
    
    migrar_servicios()
    verificar_migracion()
    
    print("\n" + "=" * 60)
    print(" Proceso completado")
    print("=" * 60)