**Sistema de Gestión de Tareas con API Flask y SQLite**
Este proyecto es un sistema básico para gestionar usuarios y tareas a través de una API REST construida con Flask y SQLite.

**Requisitos:** Python 3.7 o superior.

**Librerías necesarias:** Flask, requests y Werkzeug (para el hasheo de contraseñas). 

**Archivos principales:**

- servidor.py: Código del servidor Flask con endpoints para registro, login y gestión de tareas.
- templates/index.html: Página de bienvenida.
- cliente.py: Script Python para interactuar con la API desde consola.

**Ejecución del proyecto:**

1. Clonar o descargar el repositorio escribiendo en la terminal: git clone https://github.com/msteinaker/PFO2-GestionDeTareas.git

2. Posicionarse en la carpeta principal del proyecto con el comando: cd PFO2-GestionDeTareas

3. Abrir una terminal e instalar las librerías con el comando: 
pip install Flask requests Werkzeug

4. Ejecutar el servidor con: python servidor.py

5. El servidor correrá en http://127.0.0.1:5000

6. Para probar la parte del cliente, abrir otra terminal y ejecutar: python cliente.py

7. El cliente mostrará un menú para registrar usuarios, iniciar sesión, crear, ver y eliminar tareas.

**Funcionalidades:**
- Registrar un nuevo usuario: se pedirán usuario y contraseña. Si ya existe, nos mostrará un mensaje. Si todo está correcto, se creará uno nuevo con esos datos.
- Iniciar sesión: el cliente te pedirá estas credenciales, y el servidor va a verificar si son válidas, enviándonos un mensaje para confirmar si pudimos iniciar sesión o no.
- Crear tareas: luego de iniciar sesión, podrás crear tareas con su descripción.
- Ver tareas: el cliente te mostrará las tareas asociadas a ese usuario.
- Eliminar tareas: se te pedirá que ingreses la ID de la tarea que quieras eliminar.
- Marcar tareas como completadas: podrás marcar las tareas que hayas creado como completadas, poniendo su ID. 


**Endpoints principales:**
- POST /registro: registra usuarios, recibiendo un JSON con usuario y contraseña.
  Ejemplo de solicitud: {"usuario": "nombre", "contraseña": "1234"}
- POST /login: Inicia sesión verificando las credenciales.
- GET /tareas: muestra la página HTML de bienvenida.
- GET /tareas/json: lista las tareas del usuario.
- POST /tareas: crea una tarea.
- DELETE /tareas/<id>: elimina una tarea teniendo en cuenta su ID.
- PATCH /tareas/<id>: 
