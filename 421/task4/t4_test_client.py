import socket
import time

port = 5050
format = 'utf-8'
DATA = 16
device_name = socket.gethostname()
server_ip = socket.gethostbyname(device_name)

server_socket_address = (server_ip, port)

def send_hours_test(client, hours_str):
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
    return response

def run_tests():
    """Test various scenarios for salary calculation"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(server_socket_address)
        print(f"Connected to Salary Calculator Server at {server_ip}:{port}")
        print("=" * 60)
        print("TESTING SALARY CALCULATION")
        print("=" * 60)
        
        # Test cases
        test_cases = [
            ("20", "20 hours (part-time): Expected Tk 4000"),
            ("40", "40 hours (full-time): Expected Tk 8000"),
            ("45", "45 hours (5 overtime): Expected Tk 8000 + 5*300 = Tk 9500"),
            ("50", "50 hours (10 overtime): Expected Tk 8000 + 10*300 = Tk 11000"),
            ("60", "60 hours (20 overtime): Expected Tk 8000 + 20*300 = Tk 14000"),
            ("0", "0 hours: Expected Tk 0"),
            ("invalid", "Invalid input test"),
            ("-5", "Negative hours test")
        ]
        
        for hours, description in test_cases:
            print(f"\nTest: {description}")
            print(f"Sending: {hours} hours")
            response = send_hours_test(client, hours)
            print(f"Result: {response}")
            time.sleep(0.5)  # Small delay between tests
        
        # Disconnect
        print(f"\nDisconnecting...")
        response = send_hours_test(client, "disconnect")
        print(f"Server response: {response}")
        
    except ConnectionRefusedError:
        print(f"Could not connect to server at {server_ip}:{port}")
        print("Make sure the server is running first.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
        print("Test completed.")

if __name__ == "__main__":
    run_tests()
