import socket
import random

# configuraciones
IP = "localhost"
PORT = 1234
timeout = 5 # tiempo de espera para paquete
loss_prob = 0.3  # probabilidad de perdida de ACK
n_packets = None # variable para almacenar el numero de paquetes a recibir
numpaket = 1 # variable que determina si ese paquete ya se ha almacenado

# inicializacion de socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))

# recibe el numero de paquetes a recibir
n_packets, client_address = server_socket.recvfrom(1024)
n_packets = int(n_packets.decode())
server_socket.settimeout(timeout)

# lista para almacenar los paquetes recibidos
received_packets = []
fin_timeout = False
paq_ant = 0

while len(received_packets) < n_packets and not fin_timeout:
    save_paq = True # variable para asegurar que no se guarda un paquete si el ack no se envia

    try:
        # recepcion de paquetes
        packet, client_address = server_socket.recvfrom(1024)
        packet = eval(packet.decode())
        print("Paquete recibido:", packet)
    except socket.timeout:
        print("Fin del timeout, cerrando conexión")
        fin_timeout = True
        break
    
    # envio de confirmacion (ACK)
    if random.uniform(0, 1) >= loss_prob:
        server_socket.sendto(str(packet[0]).encode(), client_address)
        print("ACK enviado:", packet[0])
    else:
        save_paq = False
        print("ACK perdido:", packet[0])
    
    if paq_ant < packet[0]:
        # almacena el paquete recibido
        paq_ant = packet[0]
        received_packets.append(packet)
        numpaket += 1
        


#muestra los paquetes recibidos
print("Paquetes recibidos:", received_packets)

# cierre de socket
server_socket.close()

