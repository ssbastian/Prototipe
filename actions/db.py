## Conexión con la base de datos
##

import sqlite3

def guardarUsuario(sender_id: str, nombre: str):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            sender_id TEXT PRIMARY KEY,
            nombre TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO usuarios (sender_id, nombre)
        VALUES (?, ?)
        ON CONFLICT(sender_id) DO UPDATE SET
            nombre = excluded.nombre
    """, (sender_id, nombre))
    conn.commit()
    conn.close()