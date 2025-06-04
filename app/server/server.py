import threading
from socket import * # todo: import only used functions
from app.utils import text_color

online_clients: dict = {} # Dictionary to keep track of online users (Key: socket, Value: username)
clients_lock = threading.Lock()

def add_client(client_socket, username: str) -> None:
    """
    TODO: docs
    """
    with clients_lock:
        online_clients[client_socket] = username

def remove_client(client_socket) -> None:
    """
    TODO: docs
    """
    with clients_lock:
        online_clients.pop(client_socket)

def broadcast(message:str, sender:socket = None) -> None:
    """
    Broadcast a message to all online clients (except sender, in case message was sent by a client).
    :param message: The message to broadcast.
    :type message: str
    :param sender: The message sender (defaults to None).
    :type sender: socket
    :return: None
    :rtype: NoneType
    """
    with clients_lock:
        for client in online_clients:
            try:
                if sender == None:
                    client.sendall(message.encode('utf-8'))
                elif client != sender:
                    formatted_message = text_color.blue(f'{online_clients[sender]}: ') + message
                    client.sendall(formatted_message.encode('utf-8'))
            except:
                pass  # Optional: handle/remove dead sockets

def handle_client(client_socket, client_addr):
    """
    TODO: docs
    """
    print(f'Connection from {client_addr}')
    try:
        reply = text_color.green('Please enter a username:\r\n')
        client_socket.sendall(reply.encode('utf-8'))

        data = client_socket.recv(1024)
        username = data.decode('utf-8', errors='ignore').strip()

        add_client(client_socket, username)

        welcome = f"Welcome, {username}!\r\nType 'quit' to disconnect.\r\n"
        client_socket.sendall(welcome.encode('utf-8'))

        join_message = text_color.green(f'\r\n- - - {username} has joined the chat - - -\r\n')
        broadcast(join_message)

        while True:
            msg = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
            if msg.lower() == 'quit':
                goodbye = f"Goodbye, {username}!\r\n"
                client_socket.sendall(goodbye.encode('utf-8'))
                leave_message = text_color.green(f'\r\n- - - {username} has left the chat - - -\r\n')
                broadcast(leave_message)
                break
            broadcast(msg+'\n\r', client_socket)

    except Exception as e:
        print(f"Error with {client_addr}: {e}")
    finally:
        remove_client(client_socket)
        client_socket.close()
        print(f"Connection with {client_addr} closed.")


def run_server() -> None:
    """
    Begins the server workflow.
    """
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1337))
    server_socket.listen(5)
    print('Waiting For Clients...')
    while(1):
        client_socket, client_addr = server_socket.accept()
        print('Connection Established!')
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()

run_server()
