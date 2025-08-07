import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Inserción manual
#cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", ("Jade",))
cursor.execute("DELETE from usuarios")

# Confirmar y cerrar
conn.commit()
conn.close()

print("Inserción exitosa.")