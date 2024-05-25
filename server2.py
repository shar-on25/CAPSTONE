import socket
import threading

# Dictionary to store client connections
clients = {}

# Function to handle client connections
def handle_client(client_socket, client_address, client_name):
    print(f"New connection from {client_address}, username: {client_name}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                recipient, message = message.split(':', 1)
                send_private_message(client_name, recipient, message)
    except Exception as e:
        print(f"Connection with {client_address}, username: {client_name} closed: {e}")
        client_socket.close()
        del clients[client_name]

# Function to send a private message to a specific client
def send_private_message(sender, recipient, message):
    if recipient in clients:
        recipient_socket = clients[recipient]
        try:
            recipient_socket.sendall(f"{sender}: {message}".encode('utf-8'))
        except Exception as e:
            print(f"Error sending private message to {recipient}: {e}")

# Main function to start the server
def main():
    host = '127.0.0.1'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"\nServer is listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_name = client_socket.recv(1024).decode('utf-8')
            clients[client_name] = client_socket
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    main()
