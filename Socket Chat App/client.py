# Group#: G3
# Student Names: Ray Cho, Jack Kelly

from tkinter import *
import socket
import threading
# only needed for getting the current process name
from multiprocessing import current_process


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """    
    def __init__(self, window):
        window.title("client")
        
        # Create a TCP socket and connect to the server
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(ADDR)
        
        # Receive the initial message from the server, which includes the client's ID and port
        self.initial_message = self.clientSocket.recv(1024).decode(FORMAT)
        self.client_count, self.port = self.initial_message.split(",")
        self.client_count = self.client_count[1:]
        self.port = self.port[1:-1]
        
        # initialize the message to be sent
        self.message_to_send = StringVar()
        
        # Create and place GUI components using Tkinter frames and labels
        frame1 = Frame(window)
        frame1.grid(row=1, column=1, sticky='w')
        Label(frame1, text=f"Client{self.client_count} @port #{self.port}").pack(side=LEFT)
        
        frame2 = Frame(window)
        frame2.grid(row=2, column=1, sticky='w')
        Label(frame2, text="Chat message:").pack(side=LEFT)
        
        # Create an Entry widget for typing chat messages
        self.entry = Entry(frame2, width=30, textvariable=self.message_to_send, justify=RIGHT, font=('Calibri 13'))
        self.entry.pack(side=LEFT)
        # React when the user hits enter
        self.entry.bind('<Return>', lambda event: self.send_message())

        frame3 = Frame(window)
        frame3.grid(row=3, column=1, sticky='w')
        Label(frame3, text="Chat History:").pack(side=LEFT)

        # Create a Text widget for displaying chat history
        self.text_history = Text(window, width=50, height=15, wrap=WORD, state='disabled')
        self.text_history.grid(row=4, column=1, sticky='nswe')
        scrollbar = Scrollbar(window, command=self.text_history.yview)
        scrollbar.grid(row=4, column=2, sticky='nswe')
        self.text_history.config(yscrollcommand=scrollbar.set)
        self.text_history.tag_configure(RIGHT, justify="right")
        
        # To make the chat history responsive
        window.columnconfigure(1, weight=1)
        window.rowconfigure(4, weight=1)
        
        # Start a new thread to receive messages from the server
        client_thread = threading.Thread(target=self.receive_message, daemon=True)
        client_thread.start()
        
    def send_message(self):
        # Send a chat message to the server
        if self.clientSocket:
            # Handles the error when the client is disconnected and send a chat message to the server if not
            try:
                # Switch between the states of self.text_history to allow readonly
                self.text_history.configure(state='normal')
                self.text_history.insert(END, f"Client {self.client_count}: {self.message_to_send.get()}\n", RIGHT)
                self.text_history.configure(state='disabled')
                self.clientSocket.send(self.message_to_send.get().encode(FORMAT))
                # Clear the entry box
                self.entry.delete(0, END)
            
            # Handle socket errors or OSError, which may occur if the client is disconnected
            except (socket.error, OSError):
                print("[ERROR] Unable to send message. Client may be disconnected.")
    
    def receive_message(self):
        # Continuously receive messages from the server
        while True:
            try:
                received_message = self.clientSocket.recv(1024).decode(FORMAT)
                self.text_history.configure(state='normal')
                self.text_history.insert(END, f"{received_message}\n",)
                self.text_history.configure(state='disabled')
                
            # Handle ConnectionAbortedError, which may occur if the client is disconnected
            except ConnectionAbortedError:
                print(f"[CONNECTION HAS CLOSED] @port {self.port}")
                break

def main():  
    window = Tk()
    c = ChatClient(window)
    window.mainloop()

if __name__ == '__main__':  
    main()
