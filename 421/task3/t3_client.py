import socket

port = 5050
format = 'utf-8'
DATA = 16
device_name = socket.gethostname()
server_ip = socket.gethostbyname(device_name)
client_ip = socket.gethostbyname(device_name)


server_socket_address = (server_ip, port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_socket_address)


def sending_message(msg):
    message = msg.encode(format)
    msg_length = len(message)
    msg_length_str = str(msg_length).encode(format)
    msg_length_str += b' ' * (DATA - len(msg_length_str)) 
    
    client.send(msg_length_str)
    client.send(message)
    
    sent_from_server = client.recv(128).decode(format)
    print("sent from server:", sent_from_server)

while True:
    msg = input("Enter message to send (or 'disconnect' to exit): ")
    sending_message(msg)
    if msg == "disconnect":
        break