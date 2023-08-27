#########################################################################
#   En este documento se definen las estrucuras basicas que tendran los #
#   canales, los clientes y el servidor (TCP).                          #
#########################################################################

from socket import *

class SERVER:
    def __init__(self):
        self.server_addr = '0.0.0.0'
        self.server_port = 12000
        self.server_clients = []
        self.server_canals = []
        self.server_socket = socket
        
class CANAL:
    def __init__(self):
        self.canal_name = "none"
        self.canal_clients = []
        self.contrasena = "none"
        self.confidencial = False

class CLIENTE:
    def __init__(self):
        self.client_name = "none"
        self.client_connection = socket 
        self.client_canal = CANAL()
