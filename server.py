"""
Description: A simple client-server application using TCP sockets.
"""

import socket
import threading
from datetime import datetime
import os

# Maximum number of clients allowed
MAX_CLIENTS = 3
clients = {}  # Dictionary to store current client info
client_history = {}  # Dictionary to store history of all clients
FILE_REPOSITORY = "file_repository"  # Directory for storing files

# Lock for thread-safe operations on shared data
clients_lock = threading.Lock()


def send_status(client_socket):
    """
    Sends the status of connected clients to the specified client socket.
    """
    status_message = "Connected clients history:\n"
    with clients_lock:
        for name, info in client_history.items():
            disconnection_time = info['disconnected_at'] if info['disconnected_at'] else "Still connected"
            status_message += (f"{name}: Address: {info['address']}, "
                               f"Connected at: {info['connected_at']}, "
                               f"Disconnected at: {disconnection_time}\n")
    client_socket.send(status_message.encode())


def send_file_list(client_socket):
    """
    Sends a list of available files in the repository to the specified client socket.
    """
    files = os.listdir(FILE_REPOSITORY)
    file_list = "\n".join(files)
    client_socket.send(f"Available files:\n{file_list}".encode())


def handle_print(client_socket, item_name):
    """
    Sends the contents of the specified file to the client.
    """
    file_path = os.path.join(FILE_REPOSITORY, item_name)

    if os.path.isfile(file_path):
        with open(file_path, "r") as f:  # Open as text for reading
            content = f.read()
            client_socket.send(f"Contents of {item_name}:\n{content}".encode())
    else:
        client_socket.send(f"No such file: {item_name}".encode())


def handle_client(client_socket, client_address):
    """
    Handles communication with a connected client.
    """
    with clients_lock:
        client_name = f"Client{len(client_history) + 1:02d}"
        connection_time = datetime.now()

        # Store client info
        clients[client_name] = {
            'address': client_address,
            'connected_at': connection_time,
            'disconnected_at': None
        }
        client_history[client_name] = clients[client_name].copy()

    client_socket.send(f"Welcome to the server {client_name}".encode())
    print(f"{client_name} connected from {client_address} at {connection_time}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"{client_name} sent: {message}")

            # Handle various commands
            if message.lower() == "exit":
                break
            elif message.lower() == "status":
                send_status(client_socket)
            elif message.lower() == "list":
                send_file_list(client_socket)
            elif message.lower().startswith("print "):
                handle_print(client_socket, message[6:])
            else:
                response = f"{message} ACK"
                client_socket.send(response.encode())
        except ConnectionResetError:
            print(f"{client_name} forcibly disconnected.")
            break
        except Exception as e:
            print(f"Error handling {client_name}: {e}")
            break

    # Clean up on exit
    with clients_lock:
        disconnection_time = datetime.now()
        clients[client_name]['disconnected_at'] = disconnection_time
        client_history[client_name]['disconnected_at'] = disconnection_time
        del clients[client_name]

    client_socket.close()
    print(f"{client_name} disconnected at {disconnection_time}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(MAX_CLIENTS)
    print("Server listening on port 8080")

    if not os.path.exists(FILE_REPOSITORY):
        os.makedirs(FILE_REPOSITORY)

    while True:
        client_socket, addr = server.accept()

        with clients_lock:
            # Check if the server is full
            if len(clients) < MAX_CLIENTS:
                # Start a new thread for the client
                client_thread = threading.Thread(
                    target=handle_client, args=(client_socket, addr))
                client_thread.start()
            else:
                # If the server is full, reject the connection
                print("Server full. Rejecting new connection.")
                client_socket.send(
                    "Server is full. Please try again later.".encode())
                client_socket.close()


if __name__ == "__main__":
    main()
