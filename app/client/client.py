import tkinter as tk
import threading
import socket


def set_connection():
    user_input = input(
        'Please enter server connection info as follows: [ip_addr]:[port]\n\tex:\n\t127.0.0.1:1337\n\n')
    try:
        ip, port = user_input.split(':')
        port = int(port)
    except BaseException as e:
        ip, port = '127.0.0.1', 1337
    return (ip, port)

HOST, PORT = set_connection()

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.text_area = tk.Text(master, state='disabled', bg='black', fg='white')
        self.text_area.tag_config("system", foreground="lime")
        self.text_area.tag_config("username", foreground="cyan")
        self.text_area.tag_config("message", foreground="white")
        self.text_area.pack(expand=True, fill='both')

        self.entry = tk.Entry(master)
        self.entry.pack(fill='x')
        self.entry.bind("<Return>", self.send_message)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            self.socket.sendall(msg.encode('utf-8'))
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.display_message(data)
            except:
                break

    def display_message(self, msg):
        self.text_area.configure(state='normal')

        # System messages (like join/leave) start with a known pattern
        if "- - -" in msg:
            self.text_area.insert(tk.END, msg + "\n", "system")
        elif ": " in msg:
            # Format: username: message
            username, content = msg.split(": ", 1)
            self.text_area.insert(tk.END, username + ": ", "username")
            self.text_area.insert(tk.END, content + "\n", "message")
        else:
            # fallback
            self.text_area.insert(tk.END, msg + "\n")

        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

root = tk.Tk()
client = ChatClient(root)
root.mainloop()
