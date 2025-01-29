# Chat Multicanal con Comunicación TCP y UDP

Es un sistema de chat multicanal que permite la comunicación entre múltiples clientes mediante TCP y UDP.

---

## **Estructura del Proyecto**

El proyecto se divide en dos partes principales:

- `/Basic-Client-Server-UDP-Communication` → Contiene la implementación básica de comunicación UDP cliente-servidor.

  - `Client.py` → Cliente UDP.
  - `Servidor.py` → Servidor UDP.

- `/Multi-Channel` → Implementación del chat multicanal basado en TCP.
  - `/client`
    - `TCPClient.py` → Cliente TCP.
  - `/server`
    - `TCPServer.py` → Servidor TCP.
    - `ServerStructs.py` → Definiciones de estructuras para el servidor.
  - `/docs`
    - `Xat_Multicanal.pdf` → Documentación del proyecto.
- `README.md` → Instrucciones de instalación y ejecución.

---

## **Instalación y Requisitos**

### **Requisitos Previos**

- Python 3.x instalado en el sistema.
- Biblioteca `socket` (incluida por defecto en Python).

### **Configuración**

1. Clona o descarga el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/MultiXat.git
   cd MultiXat
   ```

2. Asegúrate de que Python esté instalado:
   ```bash
   python3 --version
   ```

---

## **Cómo Ejecutarlo**

### **Ejecutar el Servidor UDP**

Desde la carpeta `/Basic-Client-Server-UDP-Communication`, inicia el servidor con:

```bash
python3 Basic-Client-Server-UDP-Communication/Servidor.py
```

Esto iniciará el servidor UDP en `localhost:1234`, esperando paquetes de clientes.

---

### **Ejecutar un Cliente UDP**

Desde la carpeta `/Basic-Client-Server-UDP-Communication`, inicia un cliente con:

```bash
python3 Basic-Client-Server-UDP-Communication/Client.py
```

El cliente enviará paquetes al servidor, y este responderá con ACKs.  
Si los paquetes o ACKs se pierden, el cliente retransmite hasta alcanzar el **límite de tolerancia**.

---

### **Ejecutar el Servidor TCP**

Desde la carpeta `/Multi-Channel/server`, inicia el servidor con:

```bash
python3 Multi-Channel/server/TCPServer.py
```

Esto iniciará el servidor en la dirección IP `0.0.0.0` y el puerto `12000`, quedando a la espera de clientes.

---

### **Ejecutar un Cliente TCP**

Desde la carpeta `/Multi-Channel/client`, inicia un cliente con:

```bash
python3 Multi-Channel/client/TCPClient.py
```

Esto conectará el cliente al servidor y permitirá la comunicación.  
El cliente pedirá un nombre de usuario antes de unirse al chat.

Para ejecutar múltiples clientes, **abre nuevas terminales** y ejecuta el mismo comando varias veces.

---

## **Funcionamiento del Chat TCP**

El chat permite a los usuarios interactuar en canales y enviar mensajes privados.

### **Comandos Disponibles**

| Comando                             | Función                                |
| ----------------------------------- | -------------------------------------- |
| `CREA <canal>`                      | Crea un canal público.                 |
| `CONFIDENCIAL <canal> <contraseña>` | Crea un canal privado con contraseña.  |
| `ELIMINAR <canal>`                  | Elimina un canal.                      |
| `ENTRA <canal>`                     | Entra en un canal.                     |
| `PRIVAT <usuario> <mensaje>`        | Envía un mensaje privado.              |
| `MOSTRA_CANALS`                     | Muestra los canales disponibles.       |
| `MOSTRA_USUARIS`                    | Muestra los usuarios del canal actual. |
| `MOSTRA_TOTS`                       | Muestra todos los usuarios conectados. |
| `HELP`                              | Lista de comandos.                     |
| `SORTIR`                            | Salir del chat.                        |

---

## **Funcionamiento de la Comunicación UDP**

El protocolo UDP se utiliza para simular un sistema de envío de paquetes con pérdidas.

- **El cliente envía paquetes al servidor con una cierta probabilidad de pérdida.**
- **El servidor responde con ACKs, que también pueden perderse.**
- **El cliente retransmite si no recibe el ACK en un tiempo determinado.**

### **Parámetros Ajustables**

En `Client.py` y `Servidor.py` se pueden modificar:

- `loss_prob`: Probabilidad de pérdida de paquetes.
- `timeout`: Tiempo máximo de espera por un ACK.
- `tolerancia`: Número máximo de reintentos antes de cerrar la conexión.

---

## **Autores**

- Mariona Farré Tapias
- Marc Pérez Guerrero
