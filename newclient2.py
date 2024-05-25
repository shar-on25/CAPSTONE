import socket
import threading
import sys  # Import sys module for exiting the program

# Function to receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
    except Exception as e:
        print(f"Connection closed by server: {e}")
        sys.exit()  # Exit the program if the server closes the connection

# Function to send messages to the server
def send_message(client_socket, recipient, message):
    try:
        client_socket.sendall(f"{recipient}:{message}".encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

# Main function to start the client
def main():
    host = '127.0.0.1'
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("\nConnected to server. Start chatting...")
    username = input("Enter your username: ")
    client_socket.sendall(username.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    recipient = input("Enter recipient's username: ")

    try:
        while True:
            message = input("Enter your message (or type 'change' to change recipient or 'quit' to exit): ")
            if message.lower() == 'change':
                recipient = input("Enter new recipient's username: ")
            elif message.lower() == 'quit':
                client_socket.sendall("quit".encode('utf-8'))  # Inform server about quitting
                break  # Exit the loop and close the connection
            else:
                send_message(client_socket, recipient, message)
    except KeyboardInterrupt:
        print("Closing connection...")
        client_socket.close()

if __name__ == "__main__":
    main()
