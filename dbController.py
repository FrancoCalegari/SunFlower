# db_controller.py

import sqlite3

DB_NAME = "SunFlower.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Crear tablas si no existen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        contraseña TEXT NOT NULL,
        Correo TEXT NOT NULL,
        telefono NUMERIC NOT NULL,
        RelacionCon TEXT,
        cumpleaños NUMERIC NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        titulo TEXT NOT NULL,
        descripción TEXT NOT NULL,
        duracionEvento NUMERIC NOT NULL,
        TiempoEstimado NUMERIC NOT NULL,
        genero TEXT NOT NULL,
        clasificacion TEXT NOT NULL,
        FueraDentro TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relaciones (
        NombreRelacion TEXT NOT NULL,
        FechaDeRelacion NUMERIC NOT NULL,
        EventosExtra TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
