import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import socket
from pynput import keyboard
import threading
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Keylogger")

        self.is_running = False
        self.logged_text = ""

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, relief="raised")
        self.style.configure("TLabel", padding=5)

        # Text Area
        self.text_area = scrolledtext.ScrolledText(master, width=50, height=20)
        self.text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Start/Stop Button (Connect/Disconnect)
        self.start_stop_button = ttk.Button(master, text="Connect", command=self.toggle_connection)
        self.start_stop_button.grid(row=1, column=0, padx=10, pady=10)

        # Clear Button
        self.clear_button = ttk.Button(master, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=1, column=1, padx=10, pady=10)

        # Status Label
        self.status_label = ttk.Label(master, text="Status: Disconnected")
        self.status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.socket = None
        self.receive_thread = None

    def toggle_connection(self):
        if self.is_running:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
            self.is_running = True
            self.start_stop_button.config(text="Disconnect")
            self.status_label.config(text="Status: Connected")
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except ConnectionRefusedError:
            tk.messagebox.showerror("Error", "Connection refused. Make sure the server is running.")
            self.socket = None

    def disconnect(self):
        if self.socket:
            self.is_running = False
            self.socket.close()
            self.socket = None
            self.start_stop_button.config(text="Connect")
            self.status_label.config(text="Status: Disconnected")

    def receive_data(self):
        try:
            while self.is_running:
                data = self.socket.recv(1024)
                if not data:
                    self.disconnect()
                    break
                self.update_text_area(data.decode())
        except (socket.error, OSError) as e:
            print(f"Error receiving data: {e}")
            self.disconnect()

    def update_text_area(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)  # Scroll to the end

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)

def main():
    root = tk.Tk()
    gui = KeyloggerGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, gui))  # Handle window closing
    root.mainloop()

def on_closing(root, gui):
    """Handle window closing event."""
    gui.disconnect()  # Ensure disconnection before closing
    root.destroy()

if __name__ == "__main__":
    main()
