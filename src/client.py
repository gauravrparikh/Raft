'''
A client will try to make a connection to an arbitrary server. 
If the server is the leader it will accept the client request and return the data 
If the server is not the leader, it will redirect the client to the leader.
'''
import socket
import threading
import communications 

class Client: 

    def __init__(self, data, port):
        self.data = data
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', port)) # connect to the server on the specified port.
        self.leader = None
        self.term = 0

    def log_request(self, data, server_port):
        self.data = data
        self.socket.send(data.encode())
        response = self.socket.recv(1024).decode()
        