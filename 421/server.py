import socket

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

while True:
    server_socket , client_address = server.accept()
    print(f"Connected to client at {client_address}")
    connected = True
    
    while connected:
        upcoming_message_length = server_socket.recv(DATA).decode(format)
        
        print(f"Upcoming message length: {upcoming_message_length.strip()}")
        message_length = int(upcoming_message_length.strip())
        
        message = server_socket.recv(message_length).decode(format)
        
        if message == "disconnect":
            connected = False
            print("Client disconnected with", client_address)
            #break
        
        print(f"Received message: {message}")
        server_socket.send(b"Message received".encode(format))
        
    server_socket.close()
        
    
