"""
Description: A client application to connect to the server
"""

import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("localhost", 8080))
    except ConnectionRefusedError:
        print("Unable to connect to the server. It may be down or not running.")
        return

    # Receive the client's name from the server
    welcome_message = client.recv(1024).decode()
    print(welcome_message)

    if "Server is full" in welcome_message:
        print("The server is currently full. Please try again later.")
        client.close()
        return

    while True:
        message = input(
            "Send a message (type 'exit' to quit, 'status' to check connected clients, 'list' to see files, 'print <filename>' to see file contents): ")
        client.send(message.encode())

        if message.lower() == "exit":
            break
        else:
            response = client.recv(4096).decode()
            print(f"Server response: {response}")

    client.close()
    print("Disconnected from the server.")


if __name__ == "__main__":
    main()
