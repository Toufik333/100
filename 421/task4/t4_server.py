import socket
import threading

port = 5050
format = 'utf-8'
DATA = 16
device_name = socket.gethostname()
server_ip = socket.gethostbyname(device_name)

server_socket_address = (server_ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_socket_address)

server.listen()
print(f"Salary Calculator Server listening on {server_ip}:{port}")

def calculate_salary(hours):
    """
    Calculate salary based on hours worked:
    - <= 40 hours: Tk 200 per hour
    - > 40 hours: Tk 8000 + Tk 300 for each hour over 40
    """
    if hours <= 40:
        salary = hours * 200
    else:
        overtime_hours = hours - 40
        salary = 8000 + (overtime_hours * 300)
    return salary

def client_handle(server_socket, client_address):
    print(f"Connected to client at {client_address}")
    connected = True
    
    while connected:
        try:
            # Receive message length
            upcoming_message_length = server_socket.recv(DATA).decode(format)
            
            if not upcoming_message_length.strip():
                print("Client disconnected abruptly:", client_address)
                break
            
            print(f"Upcoming message length: {upcoming_message_length.strip()}")
            
            # Receive the actual message
            message_length = int(upcoming_message_length.strip())
            message = server_socket.recv(message_length).decode(format)
            
            if message.lower() == "disconnect":
                server_socket.send("BYE, THANKS FOR USING SALARY CALCULATOR".encode(format))
                print("Client disconnected:", client_address)
                connected = False
            else:
                try:
                    # Parse hours from message
                    hours = float(message)
                    if hours < 0:
                        response = "ERROR: Hours cannot be negative"
                    else:
                        salary = calculate_salary(hours)
                        response = f"Hours worked: {hours}, Calculated salary: Tk {salary}"
                    
                    server_socket.send(response.encode(format))
                    print(f"Processed: {hours} hours -> Tk {salary if hours >= 0 else 'N/A'}")
                    
                except ValueError:
                    error_msg = "ERROR: Please send a valid number for hours"
                    server_socket.send(error_msg.encode(format))
                    print(f"Invalid input received: {message}")
            
            print(f"Received message: {message}")
            
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    
    server_socket.close()

while True:
    try:
        server_socket, client_address = server.accept()
        thread = threading.Thread(target=client_handle, args=(server_socket, client_address))
        thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        break
