from socket import *
import threading
import os

# Dirección IP del servidor
serverName = 'localhost' # '127.0.0.1' 
#serverName = input("Introduce direccion IP: ")

# Puerto de comunicación
serverPort = 12000 
#serverPort = input("Introduce puerto: ")

# No se usa pero lo dejo por si a caso
# UserName = "..." # Nombre del Cliente

# Función para obtener el nombre de usuario
def nombreUsuario():
    return input("Introduce tu nombre: ")

# Función que gestiona el cliente "main"
def cliente():
    # Petición de conexión IPv4 y TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Obtenemos nombre
    UserName = nombreUsuario()

    # Limpiamos terminal
    os.system("clear")

    # Abrimos conexión TCP con el servidor
    clientSocket.connect((serverName,serverPort))
    print(f"Chat iniciado (Cliente)")

    # Enviamos nuestro nombre al servidor
    clientSocket.send(UserName.encode())

    # Iniciamos un proceso para cada evento (recepción de mensajes)
    threading.Thread(target=recibir_mensajes, args=(clientSocket,)).start()

    # Metodo para enviar un mensaje
    while True:
        # Escribimos el mensaje a enviar
        message = input()

        chat = [UserName, message]

        # Lo pasamos a string
        chat = str(chat)

        # Lo enviamos 
        clientSocket.send(chat.encode())

# Función para gestionar los mensajes recibidos
def recibir_mensajes(cSocket):
    while True:
        # Miramos si tenemos algun mensaje que recibir
        try:
            # Recibimos y guardamos el mensaje
            data = cSocket.recv(1024)

            # Si es un mensaje vacío se descarta y salimos
            if not data:
                break

            # Decodificamos el mensaje
            mensaje = data.decode()

            # Evaluamos para poder obtener el argumento 1 (nombre emisor) i 2 (mensaje)
            mensaje = eval(mensaje)

            # Imprimimos por pantalla
            print(mensaje[0].upper() + ": " + mensaje[1])

        # Si se genera una excepción por no recibir nada o se produce un error, salimos
        except ConnectionResetError:
            break

# Iniciamos nuestro cliente
cliente()
