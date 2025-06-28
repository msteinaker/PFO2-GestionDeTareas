import requests

API_URL = "http://127.0.0.1:5000"

def registrar_usuario():
    # Pedir al usuario su nombre y contraseña
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")

    # Preparar los datos para enviar al servidor
    datos = {"usuario": usuario, "contrasena": contrasena}

    # Hacer la petición POST al endpoint /registro
    r = requests.post(f"{API_URL}/registro", json=datos)

    # Mostrar la respuesta del servidor
    print(r.json())

def iniciar_sesion():
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")

    datos = {"usuario": usuario, "contrasena": contrasena}
    r = requests.post(f"{API_URL}/login", json=datos)

    print(r.json())

def crear_tarea():
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")
    descripcion = input("Descripción de la tarea: ")

    datos = {"usuario": usuario, "contrasena": contrasena, "descripcion": descripcion}
    r = requests.post(f"{API_URL}/tareas", json=datos)

    print(r.json())

def ver_tareas():
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")

    # Enviar los datos como parámetros GET
    params = {"usuario": usuario, "contrasena": contrasena}
    r = requests.get(f"{API_URL}/tareas/json", params=params)

    if r.status_code == 200:
        tareas = r.json()
        # Mostrar la lista de tareas con su estado (si está completada o no)
        for t in tareas:
            estado = "✅" if t["completada"] else "❌"
            print(f"{t['id']}: {t['descripcion']} {estado}")
    else:
        # Si hay un error, mostrar el mensaje recibido
        print(r.json())

def eliminar_tarea():
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")
    id_tarea = input("ID de la tarea a eliminar: ")

    datos = {"usuario": usuario, "contrasena": contrasena}
    r = requests.delete(f"{API_URL}/tareas/{id_tarea}", json=datos)

    print(r.json())

def completar_tarea():
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")
    id_tarea = input("ID de la tarea a completar: ")

    datos = {"usuario": usuario, "contrasena": contrasena}
    r = requests.patch(f"{API_URL}/tareas/{id_tarea}/completar", json=datos)

    print(r.json())

def menu():
    while True:
        print("\n--- Gestor de Tareas ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Crear tarea")
        print("4. Ver tareas")
        print("5. Eliminar tarea")
        print("6. Marcar tarea como completada")
        print("0. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            crear_tarea()
        elif opcion == "4":
            ver_tareas()
        elif opcion == "5":
            eliminar_tarea()
        elif opcion == "6":
            completar_tarea()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
