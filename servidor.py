from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Conectar a la bd SQLite
def conectar_db():
    return sqlite3.connect("usuarios.db")

# Crear las tablas 
def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)

    # Tabla de tareas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        completada BOOLEAN DEFAULT 0,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    conn.commit()
    conn.close()

# Crear tablas al iniciar servidor
crear_tabla()

# Endpoint Registro de usuarios (POST /registro)
@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos"}), 400

    # Hashear contraseña
    hash_contrasena = generate_password_hash(contrasena)

    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                       (usuario, hash_contrasena))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"})
    except sqlite3.IntegrityError:
        # Si el usuario ya existe, devolver error 
        return jsonify({"error": "El usuario ya existe"}), 409

# Endpoint Inicio de sesión (POST /login)
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    # Verificar que el usuario exista y que la contraseña sea correcta
    if resultado and check_password_hash(resultado[0], contrasena):
        return jsonify({"mensaje": "Inicio de sesión exitoso"})
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint Mostrar página HTML (GET /tareas)
@app.route("/tareas", methods=["GET"])
def tareas():
    return render_template("index.html") 

# Endpoint Ver tareas en formato JSON (GET /tareas/json)
@app.route("/tareas/json", methods=["GET"])
def ver_tareas():
    usuario = request.args.get("usuario")
    contrasena = request.args.get("contrasena")

    # Validar credenciales
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan credenciales"}), 400

    conn = conectar_db()
    cursor = conn.cursor()

    # Obtener id y hash de contraseña del usuario
    cursor.execute("SELECT id, contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[1], contrasena):
        usuario_id = resultado[0]
        # Obtener todas las tareas del usuario
        cursor.execute("SELECT id, descripcion, completada FROM tareas WHERE usuario_id = ?", (usuario_id,))
        tareas = cursor.fetchall()
        conn.close()
        # Devolver lista de tareas con formato JSON
        return jsonify([{
            "id": t[0],
            "descripcion": t[1],
            "completada": bool(t[2])
        } for t in tareas])
    else:
        conn.close()
        return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint Crear una tarea (POST /tareas)
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")
    descripcion = datos.get("descripcion")

    # Validar que todos los datos estén presentes
    if not usuario or not contrasena or not descripcion:
        return jsonify({"error": "Faltan datos"}), 400

    conn = conectar_db()
    cursor = conn.cursor()

    # Validar usuario y contraseña
    cursor.execute("SELECT id, contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[1], contrasena):
        usuario_id = resultado[0]
        # Insertar nueva tarea para el usuario
        cursor.execute("INSERT INTO tareas (usuario_id, descripcion) VALUES (?, ?)",
                       (usuario_id, descripcion))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Tarea creada exitosamente"})
    else:
        conn.close()
        return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint Eliminar una tarea (DELETE /tareas/<id>)
@app.route("/tareas/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    # Validar credenciales
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan credenciales"}), 400

    conn = conectar_db()
    cursor = conn.cursor()

    # Validar usuario y contraseña
    cursor.execute("SELECT id, contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[1], contrasena):
        usuario_id = resultado[0]
        # Eliminar tarea que pertenezca al usuario
        cursor.execute("DELETE FROM tareas WHERE id = ? AND usuario_id = ?", (id_tarea, usuario_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Tarea eliminada"})
    else:
        conn.close()
        return jsonify({"error": "Credenciales inválidas"}), 401

# Nuevo Endpoint para marcar tarea como completada (PATCH /tareas/<id>/completar)
@app.route("/tareas/<int:id_tarea>/completar", methods=["PATCH"])
def completar_tarea(id_tarea):
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan credenciales"}), 400

    conn = conectar_db()
    cursor = conn.cursor()

    # Validar usuario y contraseña
    cursor.execute("SELECT id, contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[1], contrasena):
        usuario_id = resultado[0]
        # Marcar tarea como completada
        cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ? AND usuario_id = ?", (id_tarea, usuario_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Tarea marcada como completada"})
    else:
        conn.close()
        return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == "__main__":
    app.run(debug=True)
