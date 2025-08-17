import socket

port = 5050
format = 'utf-8'
DATA =16
DISCONNECT_MSG = "disconnect"
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
        
        if not upcoming_message_length:
            print("client disconnected abruptly:" , client_address)
            break
        
        print(f"Upcoming message length: {upcoming_message_length.strip()}")
        
        message_length = int(upcoming_message_length.strip())
        message = server_socket.recv(message_length).decode(format)
        
        if message.lower() == DISCONNECT_MSG:
            server_socket.send("BYE, NICE TO SERVE U".encode(format))
            print("Disconnected With",client_address)
            connected = False
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

        # if message == "disconnect":
            
        #     print("Client disconnected with", client_address)
        #     connected = False
        #     #break
        
        print(f"Received message: {message}")
        #server_socket.send("Message received".encode(format))
        
    server_socket.close()
        
    
