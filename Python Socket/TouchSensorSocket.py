import argparse
import threading
import read_serial_func
import socket

def read_serial_and_update(client_socket):
    try:
        for data in read_serial_func.read_serial_func(COM_PORT, BAUD_RATE):
            b1 = int(data == "1")
            print(b1)
            client_socket.sendall(bytes([b1]))  # Send the value (0 or 1) to Unity
    except (ConnectionResetError, BrokenPipeError):
        print("Unity connection forcibly closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Touch Sensor Socket Script")
    parser.add_argument("COM_PORT", help="COM port for serial communication")
    parser.add_argument("BAUD_RATE", type=int, help="Baud rate for serial communication")
    args = parser.parse_args()

    COM_PORT = args.COM_PORT
    BAUD_RATE = args.BAUD_RATE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 12345))  # Using localhost IP and port
        server_socket.listen(1)

        print("Waiting for Unity to connect...")
        client_socket, client_address = server_socket.accept()
        print("Unity connected:", client_address)

        update_thread = threading.Thread(target=read_serial_and_update, args=(client_socket,))
        update_thread.daemon = True
        update_thread.start()

        try:
            update_thread.join()
        finally:
            client_socket.close()
