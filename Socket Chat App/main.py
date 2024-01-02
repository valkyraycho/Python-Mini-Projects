from tkinter import *
import multiprocessing

import client
import server

if __name__ == "__main__":
    client1 = multiprocessing.Process(target=client.main)
    client2 = multiprocessing.Process(target=client.main)
    server = multiprocessing.Process(target=server.main)
    server.start()
    client1.start()
    client2.start()
    
