import socket
import threading

port = 5050
format = 'utf-8'
DATA =16
device_name = socket.gethostname()
server_ip = socket.gethostbyname(device_name)

server_socket_address = (server_ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_socket_address)

server.listen()
print(f"Server listening on {server_ip}:{port}")

def client_handle(server_socket, client_address):
    print(f"Connected to client at {client_address}")
    connected = True
    while connected:
        upcoming_message_length = server_socket.recv(DATA).decode(format)
        
        if not upcoming_message_length.strip():
            print("Client disconnected abruptly:", client_address)
            break
        
        print(f"Upcoming message length: {upcoming_message_length.strip()}")
        
        message_length = int(upcoming_message_length.strip())
        message = server_socket.recv(message_length).decode(format)
        
        if message.lower() == "disconnect":
            server_socket.send("BYE, NICE TO SERVE U".encode(format))
            print("Client disconnected with", client_address)
            connected = False
            #break
        else:
            vowels = "aeiouAEIOU"
            count = 0
            for char in message:
                if char in vowels:
                    count += 1
            if count == 0:
                server_socket.send("Not Enough Vowels".encode(format))
            elif count <=2:
                server_socket.send("Enough Vowels I guess".encode(format))
            else:
                server_socket.send("Too Many Vowels".encode(format))
        print(f"Received message: {message}")
        
        
    server_socket.close()
        
    
while True:
    server_socket , client_address = server.accept()
    thread = threading.Thread(target=client_handle, args=(server_socket, client_address))
    thread.start()