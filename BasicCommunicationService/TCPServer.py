from socket import *
import threading
import os
from ServerStructs import *

# Limpiamos terminal
os.system("clear")

#################################
#       INICIACION SERVER       #
#################################

server = SERVER()

# Dirección IP del servidor
# server.server_addr = input("Introduce direccion IP: ")

# Puerto de comunicación
# server.server_port = input("Introduce puerto: ")

# Petición de conexión IPv4 y TCP
server.server_socket = socket(AF_INET, SOCK_STREAM)

#################################

mainCanal = CANAL()
mainCanal.canal_name = "MAIN_CANAL"

# Función que gestiona el servidor "main"


def server_start():

    # Se inicializa el socket en la dirección IP y el puerto
    server.server_socket.bind((server.server_addr, server.server_port))

    # Empezamos a escuchar en el puerto inicializado
    server.server_socket.listen()

    # Añadimos el canal principal a la lista de canales del servidor
    server.server_canals.append(mainCanal)

    print(f"Chat iniciado (Servidor)")
    print(f"------------------------")

    while True:
        # Aceptamos conexión
        conn, addr = server.server_socket.accept()

        # Creamos un nuevo cliente
        newClient = CLIENTE()

        # Guardamos el nombre de nuestro cliente
        newClient.client_name = str(conn.recv(1024).decode())

        # Guardamos la conexion
        newClient.client_connection = conn

        # El cliente nuevo se inicia en el canal principal
        newClient.client_canal = mainCanal

        # Añadimos el cliente a la lista de clientes del servidor
        server.server_clients.append(newClient)

        # Añadimos el cliente al canal principal (main)
        server.server_canals[0].canal_clients.append(newClient)

        # Notificamos conforme el cliente se ha unido
        print("(" + newClient.client_name +
              ") conectado desde la dirección IP " + addr[0])
        # Iniciamos un proceso para manejar los nuevos eventos del cliente
        threading.Thread(target=manage_client, args=(newClient,)).start()

# Función para gestionar a los clientes


def manage_client(client):
    while True:
        try:
            # Recibimos paquete de datos
            data = client.client_connection.recv(1024)

            # Si tenemos un paquete de datos vacío cancelamos
            if not data:
                break

            # Decodificamos el mensaje
            message = data.decode()

            # Preparamos el mensaje
            message = eval(message)

            # Comprovar si és un mensaje especial
            try:
                is_message = manage_instructuion(message, client)

                if is_message:
                    # Imprimimos el mensaje junto a la persona que lo ha enviado
                    print("[" + message[0].upper() + "]: " + message[1])

                    # Difundimos el mensaje
                    send_message(message, client)
            except:
                new_message = ["from_server", "Se ha producido un error con su instrucción, prueba a ejecutar el comando HELP para ayuda"]
                client.client_connection.send(str(new_message).encode())

        # Si se genera una excepción con el cliente, lo quitamos de la conexión
        except:
            
            # Eliminamos el thread
            break

# Función para difundir el mensaje entre todos los clientes


def send_message(message, from_client):

    # For para recorrer todos los clientes conectados
    for client in from_client.client_canal.canal_clients:

        # Comprobamos que el cliente no es el emisor del mensaje
        if from_client != client:

            # Enviamos el mensaje
            client.client_connection.send(str(message).encode())


# Función para gestionar las diferentes instrucciones
def manage_instructuion(message, client):

    # Codigo de resultado para notificar al cliente
    OperationResult = """"""

    # Separamos el mensaje por partes
    split_message = message[1].split(" ", 2)

    # Obtenemos la instruccion del mensaje, si hay
    instruction = split_message[0]

    # Opción CREA canal (no confidencial)
    if "CREA" in instruction:
        
        # Obtenemos el nombre del nuevo canal
        instr_extension = split_message[1]

        # Comprovamos que no exista un canal con ese nombre
        if get_canal_index(instr_extension) == -1:

            # Creamos el nuevo canal
            canal_aux = CANAL()

            # Le ponemos el nombre
            canal_aux.canal_name = instr_extension

            # Lo añadimos a la lista de canales del servidor
            server.server_canals.append(canal_aux)

            # Cambiamos el codigo de resultado de la operación para notificar al cliente
            OperationResult = """Se ha creado el canal"""

            # Imprimimos resultado por la pantalla del servidor
            print(client.client_name + " ha creado un canal nuevo")

        else:

            # En caso de que el ya exista un canal con ese nombre
            OperationResult = """El canal ya existe, no se ha creado"""

            # Imprimimos resultado por la pantalla del servidor
            print(client.client_name + " ha intentado crear un canal sin exito")
    
    # Opción CREA canal (confidencial)
    elif "CONFIDENCIAL" in instruction:

        # Obtenemos el nombre del nuevo canal
        instr_extension = split_message[1]

        # Comprovamos que no exista un canal con ese nombre
        if get_canal_index(instr_extension) == -1:

            # Creamos el nuevo canal
            canal_aux = CANAL()

            # Le ponemos el nombre
            canal_aux.canal_name = instr_extension

            # Le ponemos la contraseña
            canal_aux.contrasena = split_message[2]

            # Marcamos como un canal confidencial
            canal_aux.confidencial = True

            # Lo añadimos a la lista de canales del servidor
            server.server_canals.append(canal_aux)

            # Cambiamos el codigo de resultado de la operación para notificar al cliente
            OperationResult = """Se ha creado el canal confidencial, la contraseña es: """ + canal_aux.contrasena

            # Imprimimos resultado por la pantalla del servidor
            print(client.client_name + " ha creado un canal confidencial nuevo")

        else:

            # En caso de que el ya exista un canal con ese nombre
            OperationResult = """El canal ya existe, no se ha creado"""

            # Imprimimos resultado por la pantalla del servidor
            print(client.client_name + " ha intentado crear un canal confidencial sin exito")

    # Opción para eliminar un canal
    elif "ELIMINAR" in instruction:

        # Obtenemos el nombre del nuevo canal
        instr_extension = split_message[1]

        # Obtenemos el indice del canal
        index = get_canal_index(instr_extension)

        # Comprovamos que existe
        if index == -1:

            # Notificamos el cliente de que no existe el canal
            OperationResult = """El canal no existe"""

            # Imprimimos por pantalla que han intentado eliminar un canal
            print(client.client_name + " ha intentado eliminar un canal sin exito")

        # Comprovamos que no es el canal principal
        elif server.server_canals[index].canal_name == "MAIN_CANAL":

            # Notificamos el cliente de que no se puede eliminar este canal
            OperationResult = """Este canal no se puede eliminar"""

            # Imprimimos por pantalla del servidor que han intentado eliminar el canal principal
            print(client.client_name + " ha intentado eliminar el canal principal")

        # Si existe lo eliminamos
        else:

            # For para mover a todos los clientes de ese canal 
            for _client in  server.server_canals[index].canal_clients:
                
                # Asignamos el canal por defecto a los clientes del canal que va a ser eliminado
                _client.client_canal = server.server_canals[0]

                # Añadimos los clientes al canal por defecto
                server.server_canals[0].canal_clients.append(_client)

            # Elimina el canal de la lista de canales del servidor
            server.server_canals.pop(index)

            # Notificamos que se ha eliminado el canal
            OperationResult = """Se ha eliminado el canal, los clientes se han movido a MAIN_CANAL"""

            # Imprimimos en la pantalla del servidor el resultado
            print(client.client_name + " ha eliminado un canal")
    
    # Opción para entrar en otro canal (sales del anterior)
    elif "ENTRA" in instruction:

        # Obtenemos el nombre del nuevo canal
        instr_extension = split_message[1]

        # Obtenemos el indice del canal
        index = get_canal_index(instr_extension)

        # Comprovamos que existe el canal
        if index == -1:
            OperationResult = """El canal no existe"""
        else:

            # Miramos si es un canal confidencial
            if server.server_canals[index].confidencial:

                # Hacemos un try por si no ha puesto ninguna contraseña y se genera un error
                try:

                    # Miramos si la contraseña es correcta
                    if split_message[2] == server.server_canals[index].contrasena:

                        # Obtenemos el indice del canal antiguo
                        canal_antiguo = get_canal_index(client.client_canal.canal_name)

                        # Inicializamos el indice del cliente a 0
                        client_index = 0

                        # For para obtener el indice del cliente que hay que mover
                        for i, _client in enumerate(server.server_canals[canal_antiguo].canal_clients):
                            if _client.client_name == client.client_name:
                                client_index = i

                        # Eliminamos al cliente del canal antiguo
                        server.server_canals[canal_antiguo].canal_clients.pop(client_index)

                        # Le asignamos el nuevo canal al cliente
                        client.client_canal = server.server_canals[index]

                        # Añadimos al cliente al nuevo canal
                        server.server_canals[index].canal_clients.append(client)

                        # Notificamos al cliente conforme ha entrado
                        OperationResult = """Has entrado en el canal confidencial"""

                        # Imprimimos por pantalla del server la acción
                        print(client.client_name + " se ha movido a un canal confidencial")

                    else:

                        # Notificamos al cliente conforme la contraseña no corresponde
                        OperationResult = """Contraseña incorrecta"""

                        # Imprimimos por pantalla del server la acción
                        print(client.client_name + " no ha introducido la contraseña correcta")

                except:

                    # Notificamos al cliente conforme necesita contraseña
                    OperationResult = """Necesitas una contraseña para entrar a este canal"""

                    # Imprimimos por pantalla del server la acción
                    print(client.client_name + " no ha introducido contraseña")

            else:

                # Obtenemos el indice del canal antiguo
                canal_antiguo = get_canal_index(client.client_canal.canal_name)

                # Inicializamos el indice del cliente a 0
                client_index = 0

                # For para obtener el indice del cliente que hay que mover
                for i, _client in enumerate(server.server_canals[canal_antiguo].canal_clients):
                    if _client.client_name == client.client_name:
                        client_index = i

                # Eliminamos al cliente del canal antiguo
                server.server_canals[canal_antiguo].canal_clients.pop(client_index)

                # Le asignamos el nuevo canal al cliente
                client.client_canal = server.server_canals[index]

                # Añadimos al cliente al nuevo canal
                server.server_canals[index].canal_clients.append(client)

                # Notificamos al cliente conforme ha entrado
                OperationResult = """Has entrado en el canal"""

                # Imprimimos por pantalla del server la acción
                print(client.client_name + " se ha movido a otro canal")

    # Oción para cambiar el nombre del canal
    elif "NOU_NOM_CANAL" in instruction:

        # Obtenemos el canal que queremos cambiar
        instr_extension = split_message[1]

        # Obtenemos el indice del canal
        index = get_canal_index(instr_extension)

        # Miramos si existe
        if index == -1:
            OperationResult = """El canal no existe"""

        else:
            try:

                # Miramos que el nuevo nombre no exista
                if get_canal_index(split_message[2]) == -1:

                    # Le asignamos el nuevo nombre al canal
                    server.server_canals[index].canal_name = split_message[2]

                    # Notificamos al cliente
                    OperationResult = """Se ha cambiado el nombre del canal"""

                    # Imprimimos por pantalla la accion
                    print(client.client_name + " ha cambiado el nombre de un canal")

                else:

                    # Notificamos al cliente que ya existe un canal con ese nombre
                    OperationResult = """Ya existe un canal con ese nombre"""

                    # Imprimimos por pantalla la accion
                    print(client.client_name + " ha intentado cambiar el nombre de un canal sin exito")

            except:

                # Notificamos al cliente conforme no se ha introducido un nombre nuevo
                OperationResult = """No se ha introducido un nuevo nombre para el canal"""

                # Imprimimos por pantalla la accion
                print(client.client_name + " ha intentado cambiar el nombre de un canal sin exito")
                
    # Opcion enviar un mensaje privado
    elif "PRIVAT" in instruction:

        # Obtenemos el nombre del cliente al que queremos enviar un privado
        instr_extension = split_message[1]

        # Obtenemos el indice del cliente
        index = get_client_index(instr_extension)

        # Comprovamos que existe
        if index == -1:
            OperationResult = """El cliente no existe"""
            
        else:

            # Montamos el mensaje privado
            priv_message = [client.client_name, str(split_message[2])]

            # Enviamos el mensaje solo al cliente mencionado
            server.server_clients[index].client_connection.send(
                str(priv_message).encode())
            
            # Notificamos al cliente conforme se ha enviado el privado
            OperationResult = """Se ha enviado el mensaje privado"""

            # Imprimimos por pantalla del servidor el mensaje
            print("Mensaje privado a: " + server.server_clients[index].client_name)
            print(priv_message)

    # Opción para mostrar en que canal estoy
    elif "ON_ESTIC" in instruction:

        # Notificamos al cliente con el nombre de canal donde esta
        OperationResult = """Estas al canal: """ + \
            str(client.client_canal.canal_name)
        
        # Imprimimos por pantalla del server la accion
        print(client.client_name + " ha pedido el nombre del canal donde esta")

    # Opcion para mostrar los canales
    elif "MOSTRA_CANALS" in instruction:

        # Obtenemos todos los nombres de los canales
        canals_names = [
            it_canal.canal_name for it_canal in server.server_canals]
        
        # Los montamos en un mensaje
        canals_names_str = "\n".join(canals_names)

        # Notificamos con los nombres de todos los canales
        OperationResult = """[CANALES]""" + "\n" + canals_names_str

        # Imprimimos por pantalla del server la accion
        print(client.client_name + " ha pedido todos los canales disponibles")

    # Opcion para mostrar los usuarios del canal
    elif "MOSTRA_USUARIS" in instruction:

        # Obtenemos todos los nombres de los usuarios del canal
        users_in_canal = [
            it_user.client_name for it_user in client.client_canal.canal_clients]
        
        # Los montamos en un mensaje
        users_in_canal_str = "\n".join(users_in_canal)

        # Notificamos al cliente con todos los usuarios del canal
        OperationResult = """[USUARIOS EN EL CANAL]""" + \
            "\n" + users_in_canal_str
        
        # Imprimimos por pantalla del server la accion
        print(client.client_name + " ha pedido todos los usuarios de su canal")
        
    # Opcion para mostrar todos los clientes del servidor
    elif "MOSTRA_TOTS" in instruction:

        # Obtenemos todos los nombres de los clientes
        clients_names = [
            it_client.client_name for it_client in server.server_clients]
        
        # Montamos en un mensaje
        clients_names_str = "\n".join(clients_names)

        # Notificamos al cliente con todos los usuarios del servidor
        OperationResult = """[CLIENTS]""" + "\n" + clients_names_str

        # Imprimimos por pantalla del server la accion
        print(client.client_name + " ha pedido todos clientes del servidor")

    # Opcion con todos los comandos disponibles
    elif "HELP" in instruction:
        OperationResult = """Llista [OPCIONS]
        - CREA + nom_canal
        - CONFIDENCIAL + nom_canal + contraseña
        - ELIMINAR + nom_canal
        - ENTRA + nom_canal (Correspon a l'opció de canvia)
        - NOU_NOM_CANAL + nom_canal + nou_nom
        - PRIVAT + nom_usuari + missatge
        - ON_ESTIC
        - MOSTRA_CANALS
        - MOSTRA_USUARIS
        - MOSTRA_TOTS
        - HELP
        - SORTIR"""

        # Imprimimos por pantalla del servidor la accion
        print(f"Se ha enviado la lista de ocpiones al cliente: " +
              client.client_name.upper())
        
    # Opcion para salir del servidor
    elif "SORTIR" in instruction:

        index = get_client_index(client.client_name)

        index_canal = get_canal_index(client.client_canal.canal_name)

        # Inicializamos el indice del cliente a 0
        client_index = -1

        # For para obtener el indice del cliente que hay que mover
        for i, _client in enumerate(server.server_canals[index_canal].canal_clients):
            if _client.client_name == client.client_name:
                client_index = i

        # Eliminamos el cliente del canal
        server.server_canals[index_canal].canal_clients.pop(client_index)

        # Eliminamos el cliente del servidor
        server.server_clients.pop(index)

        # Notificamos al cliente conforme ha salido
        OperationResult = """Has salido, ya puedes cerrar el terminal"""

        # Montamos mensaje para el cliente
        new_message = ["from_server", OperationResult]

        # Enviamos el mensaje
        client.client_connection.send(str(new_message).encode())

        # Cerrar la conexión del cliente
        client.client_connection.close()

    # Si es un mensaje normal
    else:

        # En caso de que sea un mensaje normal devolvemos true
        return True
    
    try:

        # Montamos mensaje para el cliente
        new_message = ["from_server", OperationResult]

        # Enviamos el mensaje
        client.client_connection.send(str(new_message).encode())

    except:

        print("Se ha eliminado el cliente del servidor")

# Función para obtener el indice del canal dentro de la lista de canales
def get_canal_index(canalName):

    # For que itera canal por canal, i corresponde al indice dentro de la lista
    for i, canal in enumerate(server.server_canals):

        # Si los nombres de los canales son iguales devolvemos el indice
        if canal.canal_name == canalName:
            return i
        
    # Si no devolvemos un -1 para decir que no se ha encontrado
    return -1

# Función para obtener el indice de cliente dentro de la lista de clientes
def get_client_index(clientName):

    # For que itera cliente por cliente, i corresponde al indice dentro de la lista
    for i, client in enumerate(server.server_clients):

        # Si los nombres de los clientes son iguales devolvemos el indice
        if client.client_name == clientName:
            return i
        
    # Si no devolvemos un -1 para decir que no se ha encontrado
    return -1

# Iniciamos nuestro servidor
server_start()
