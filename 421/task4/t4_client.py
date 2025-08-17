import socket

port = 5050
format = 'utf-8'
DATA = 16
device_name = socket.gethostname()
server_ip = socket.gethostbyname(device_name)

server_socket_address = (server_ip, port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(server_socket_address)
    print(f"Connected to Salary Calculator Server at {server_ip}:{port}")
    print("=" * 50)
    print("SALARY CALCULATOR")
    print("=" * 50)
    print("Salary Calculation Rules:")
    print("• Hours <= 40: Tk 200 per hour")
    print("• Hours > 40: Tk 8000 + Tk 300 for each hour over 40")
    print("=" * 50)
    
except ConnectionRefusedError:
    print(f"Could not connect to server at {server_ip}:{port}")
    print("Make sure the server is running first.")
    exit()

def send_hours(hours_str):
    """Send hours worked to server and receive salary calculation"""
    message = hours_str.encode(format)
    msg_length = len(message)
    msg_length_str = str(msg_length).encode(format)
    msg_length_str += b' ' * (DATA - len(msg_length_str))
    
    # Send message length first, then the actual message
    client.send(msg_length_str)
    client.send(message)
    
    # Receive response from server
    response = client.recv(1024).decode(format)
    print("Server response:", response)
    return response

def main():
    while True:
        try:
            print("\nEnter the number of hours worked (or 'disconnect' to exit):")
            user_input = input("Hours: ").strip()
            
            if user_input.lower() == "disconnect":
                send_hours("disconnect")
                break
            
            # Validate input
            try:
                hours = float(user_input)
                if hours < 0:
                    print("Please enter a non-negative number of hours.")
                    continue
                
                # Send hours to server
                send_hours(user_input)
                
            except ValueError:
                print("Please enter a valid number.")
                continue
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            send_hours("disconnect")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    print("Disconnected from server.")
    client.close()

if __name__ == "__main__":
    main()
