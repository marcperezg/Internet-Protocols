import socket
import random

# configuraciones
IP = "localhost" #"127.0.0.1"
PORT = 1234
timeout = 2  # tiempo de espera para ACK
n_packets = 10  # numero de paquetes a enviar
loss_prob = 1  # probabilidad de perdida de paquetes
tolerancia = 15 # tolerancia de perdidas de ACK (no recibidos) o paquetes

# inicializacion de socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)

# envia informacion sobre el numero de paquetes a enviar
client_socket.sendto(str(n_packets).encode(), (IP, PORT))

# lista para almacenar los paquetes recibidos
received_ack = []


paq_perdidos = 0 

for i in range(1, n_packets+1):
    # envio de paquetes
    if random.uniform(0, 1) >= loss_prob:
        client_socket.sendto(str((i, "mensaje")).encode(), (IP, PORT))
        print("Paquete enviado:", i)
    else:
        paq_perdidos = 0
        while paq_perdidos < tolerancia:
            print("Paquete perdido:", i)
            if random.uniform(0, 1) >= loss_prob:
                break
            paq_perdidos += 1
    
    if paq_perdidos == tolerancia:
        print("No se puede enviar paquete, cerrando conexión")
        break
    else:
        ack_received = False
        cont_envios = 0 # contador para evitar bucles infinitos de envios de paquetes (se intenta 10 veces)
        while not ack_received and cont_envios < tolerancia:
            cont_envios += 1
            try:
                # espera por confirmacion (ACK)
                ack, server_address = client_socket.recvfrom(1024)
                ack = int(ack.decode())
                print("ACK recibido:", ack)
                received_ack.append(ack)
                ack_received = True
            except socket.timeout:
                print("timeout, retransmitiendo paquete:", i)
                client_socket.sendto(str((i, "mensaje")).encode(), (IP, PORT))
        if cont_envios == tolerancia:
            print("No se recibe ACK del paquete, ", i, ", cerrando conexión")
            break


    

#muestra los paquetes recibidos
print("Paquetes recibidos:", received_ack)

#cierre de socket
client_socket.close()

