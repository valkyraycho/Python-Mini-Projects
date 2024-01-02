# Group#: G3
# Student Names: Ray Cho, Jack Kelly

from tkinter import *
import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'

clients = {}
clients_lock = threading.Lock()

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """    
    def __init__(self, window):
        window.title("Server")
        
        # Create and place GUI components using Tkinter frames and labels
        frame1 = Frame(window)
        frame1.grid(row=1, column=1, sticky='w')
        Label(frame1, text="Chat Server ").pack(side=LEFT)
        
        frame2 = Frame(window)
        frame2.grid(row=2, column=1, sticky='w')
        Label(frame2, text="Chat History:").pack(side=LEFT)
        
        # Create a Text widget along with a scrollbar for displaying readonly chat history
        self.text_history = Text(window, width=50, height=15, state='disabled', wrap=WORD)
        self.text_history.grid(row=4, column=1, sticky='nwse')
        scrollbar = Scrollbar(window, command=self.text_history.yview)
        scrollbar.grid(row=4, column=2, sticky='nwse')
        self.text_history.config(yscrollcommand=scrollbar.set)
        
        # To make the chat history responsive
        window.columnconfigure(1, weight=1)
        window.rowconfigure(4, weight=1)
        
        # Create a server socket, bind it to the specified address and port, and start listening
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(ADDR)
        self.serverSocket.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        
        # Initialize a counter for assigning unique client IDs
        self.client_counter = 0
        
        # Start a new thread to check for incoming client connections
        threading.Thread(target=self.check_for_clients).start()
        
    def check_for_clients(self):
        # Continuously check for incoming client connections
        while True:
            # Accept a new client connection
            clientSocket, addr = self.serverSocket.accept()
            
            # Use a lock to safely update and access the clients dictionary
            with clients_lock:
                # Increment the client counter to assign a unique client ID
                self.client_counter += 1
                # Store client information in the dictionary
                clients.update({clientSocket: (self.client_counter, addr[1])})
                
            # Send the client information back to the client   
            clientSocket.send(str(clients[clientSocket]).encode(FORMAT))
            
            # Start a new thread to handle the communication with the client
            serverThread = threading.Thread(target=self.handle_client, args=(clientSocket, addr))
            serverThread.start()
            
            # Print the current number of active connections
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        
    def handle_client(self, clientSocket, addr):
        # Handle communication with an individual client
        print(f"[NEW CONNECTION] @port {addr[1]} connection established")
        
        # Continuously listen for messages from the client
        while True:
            try:
                # Receive a message from the client
                message_received = clientSocket.recv(1024).decode(FORMAT)
                if message_received:
                    # Check if the client wants to disconnect
                    if message_received == DISCONNECT_MSG:
                        # Use a lock to safely update and access the clients dictionary
                        with clients_lock:
                            clients.pop(clientSocket, None)
                            clientSocket.close()
                    else:
                        # Format the received message with the client's ID and display it in the server GUI
                        message_received = f"Client {clients[clientSocket][0]}: {message_received}"
                        self.text_history.configure(state='normal')
                        self.text_history.insert(END, message_received+ "\n")
                        self.text_history.configure(state='disabled')
                        
                        # Use a lock to safely access the clients dictionary
                        with clients_lock:
                            # Send the message to all other connected clients
                            for client in clients:
                                if client != clientSocket:
                                    client.send(message_received.encode(FORMAT))
                                        
            # Handle exceptions related to client disconnection
            except (OSError, ConnectionResetError) as e:
                print(f"Error in handle_client: {e}")
                print(f"[CONNECTION CLOSED] @port {addr[1]} connection closed")
                
                # Use a lock to safely remove the disconnected client from the clients dictionary
                with clients_lock:
                    clients.pop(clientSocket, None)
                clientSocket.close()
                break
         
def main():  
    window = Tk()
    c = ChatServer(window)
    window.mainloop()

if __name__ == '__main__':  
    main()