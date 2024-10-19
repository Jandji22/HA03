import socket
import threading
import os

# Function to handle incoming messages and files from the client
def handle_client(client_socket):
    while True:
        try:
            # Receive the header to determine if it's a message or file
            header = client_socket.recv(1024).decode('utf-8')
            if header.startswith("FILE"):
                # Handle file reception
                filename = header.split()[1]
                filesize = int(header.split()[2])
                print(f"\nReceiving file: {filename} of size {filesize} bytes")
                with open(os.path.basename(filename), "wb") as f:
                    data = client_socket.recv(filesize)
                    f.write(data)
                print(f"Received file: {filename}")
                print_prompt()
            else:
                # Handle message reception
                print(f"\nClient: {header}")
                print_prompt()
        except:
            print("Client disconnected")
            break

# Function to send messages and files to the client or server
def send_message(socket):
    while True:
        message = input("Enter message or 'FILE <filename>' to send a file: ")
        if message.startswith("FILE"):
            # Handle file sending
            filename = message.split()[1]
            filesize = os.path.getsize(filename)
            print(f"Sending file: {filename} of size {filesize} bytes")
            socket.send(f"FILE {filename} {filesize}".encode('utf-8'))
            with open(filename, "rb") as f:
                data = f.read()
                socket.send(data)
            print(f"Sent file: {filename}")
        else:
            # Handle message sending
            print(f"Sending message: {message}")
            socket.send(message.encode('utf-8'))

# Function to receive messages and files from the server or client
def receive_message(socket):
    while True:
        try:
            # Receive the header to determine if it's a message or file
            header = socket.recv(1024).decode('utf-8')
            if header.startswith("FILE"):
                # Handle file reception
                filename = header.split()[1]
                filesize = int(header.split()[2])
                print(f"\nReceiving file: {filename} of size {filesize} bytes")
                with open(os.path.basename(filename), "wb") as f:
                    data = socket.recv(filesize)
                    f.write(data)
                print(f"Received file: {filename}")
                print_prompt()
            else:
                # Handle message reception
                print(f"\nServer: {header}")
                print_prompt()
        except:
            print("Server disconnected")
            break

# Function to print the input prompt
def print_prompt():
    print("Enter message or 'FILE <filename>' to send a file: ", end='', flush=True)

# Function to start the server
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Server listening on port {port}")

    while True:
        # Accept incoming client connections
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        # Start a thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        # Start a thread to send messages to the client
        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        send_thread.start()

# Function to start the client
def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))

    # Start a thread to send messages to the server
    send_thread = threading.Thread(target=send_message, args=(client,))
    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_message, args=(client,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

if __name__ == "__main__":
    # Ask the user if they want to start a server or client
    mode = input("Do you want to start a server or client? (server/client): ").strip().lower()
    # Ask the user which port to use
    port = int(input("Enter the port to use: ").strip())

    if mode == "server":
        start_server(port)
    elif mode == "client":
        start_client(port)
    else:
        print("Invalid mode selected. Please choose 'server' or 'client'.")
