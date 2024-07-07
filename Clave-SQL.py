# claves.py

# Importar el módulo de SQLite para la base de datos
import sqlite3

# Importar módulos de cryptography para la gestión de claves
from cryptography.fernet import Fernet

# Importar Flask para la aplicación web
from flask import Flask, request, render_template_string, redirect, url_for, session

# Crear una instancia de Flask
app = Flask(__name__)

# Clave secreta para la sesión (debe ser cambiada en una implementación real)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Función para generar una clave y guardarla en la base de datos
def generar_clave():
    # Generar una nueva clave
    clave = Fernet.generate_key()
    
    # Conectar a la base de datos SQLite (creará la base de datos si no existe)
    conn = sqlite3.connect('claves.db')
    cursor = conn.cursor()
    
    # Crear una tabla para almacenar las claves si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS claves (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        clave TEXT NOT NULL
                      )''')
    
    # Insertar la clave en la base de datos
    cursor.execute('INSERT INTO claves (clave) VALUES (?)', (clave,))
    
    # Guardar (commit) los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    
    return clave

# Función para inicializar la base de datos y crear la tabla de usuarios
def init_db():
    # Conectar a la base de datos SQLite (creará la base de datos si no existe)
    conn = sqlite3.connect('claves.db')
    cursor = conn.cursor()
    
    # Crear una tabla para almacenar usuarios si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                      )''')
    
    # Guardar (commit) los cambios y cerrar la conexión
    conn.commit()
    conn.close()

# Ruta raíz que muestra un mensaje de bienvenida y un formulario de registro de usuarios
@app.route('/')
def home():
    if 'username' in session:
        return f"<h1>Bienvenido, {session['username']}!</h1> <a href='/logout'>Cerrar sesión</a>"
    else:
        return render_template_string('''
            <h1>Bienvenido al gestor de claves</h1>
            <form action="/register" method="post">
                <label for="username">Nombre de usuario:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Registrar">
            </form>
            <h2>Iniciar sesión</h2>
            <form action="/login" method="post">
                <label for="username">Nombre de usuario:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Iniciar sesión">
            </form>
        ''')

# Ruta para manejar el registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('claves.db')
    cursor = conn.cursor()
    
    # Insertar el nuevo usuario en la base de datos
    cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
    
    # Guardar (commit) los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    
    session['username'] = username
    
    return redirect(url_for('home'))

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('claves.db')
    cursor = conn.cursor()
    
    # Buscar el usuario en la base de datos
    cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return 'Credenciales incorrectas. Inténtalo de nuevo.'

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    # Inicializar la base de datos y crear las tablas necesarias
    init_db()
    
    # Generar una clave y mostrarla en la consola (opcional)
    clave_generada = generar_clave()
    print(f"Clave generada y almacenada en la base de datos: {clave_generada.decode()}")
    
    # Ejecutar la aplicación Flask en el puerto 5800
    app.run(host='0.0.0.0', port=5800)
