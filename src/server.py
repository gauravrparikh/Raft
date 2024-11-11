import socket
import time 
import threading
import random
import fire
from enum import Enum
import communications


"""
The leader accepts log entries from clients, replicates them on other servers,
and tells servers when it is safe to apply log entries to their state machines.

"""


class Server:
    def __init__(self, data, election_time_out, role="Follower", 
                server_in_socket_port=random.randint(10000, 60000), 
                server_out_socket_port=random.randint(10000, 60000)
                server_in_socket_port=random.randint(10000, 60000), 
                server_out_socket_port=random.randint(10000, 60000)
                ):
                
        # persistent state on all servers
        self.current_term = 0
        self.voted_for = None
        self.log = []

        # volatile state on all servers
        self.commit_index = 0
        self.last_applied = 0

        # volatile state on leaders
        self.next_index = []    
        self.match_index = []

        self.data = data
        self.election_time_out = election_time_out
        self.role = role

        # Each server has a socket where it is listening for RPCs from other servers
        self.in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_socket.bind(('localhost', in_socket_port))

        # Each server has a socket where it is sending RPCs to other servers
        self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_socket.bind(('localhost',out_socket_port ))

        # Each server has a socket where it is listening for RPCs from clients
        self.in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_socket.bind(('localhost', in_socket_port))

        # Each server has a socket where it is sending RPCs to clients
        self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_socket.bind(('localhost',out_socket_port ))
       
        print("Node is listening for clients on port: ", self.in_socket.getsockname())
        print("Node is listening for servers on port: ", self.in_socket.getsockname())

        print("Node is sending output to clients on port: ", self.out_socket.getsockname())
        print("Node is sending output to servers on port: ", self.out_socket.getsockname())
    
    
    def start(self):
            """Start a server
            - Create a socket to listen for client connections.
            - Accept client connections and ``handle_client()`` in a separate thread
            - Create a socket to listen for connections from other servers in the network
            - Accept connections and ``handle_servers()`` in a separate thread
            """
            print("Starting the proxy server...")
            # Create a socket to listen for client connections
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client_socket:
                print(f"Binding client socket to {self.server_addr}:{self.server_port}...")
                self.cdn_socket.bind((self.cdn_addr, self.cdn_port))
                self.cdn_socket.listen(10)
                print(f"Listening for connections on {self.cdn_addr}:{self.cdn_port}")

                # Accept client connections and handle them in separate threads
                while True:
                    print("Waiting for a client to connect...")
                    client_socket, address = self.accept_client_connection()
                    print(f"Client connected from {address}")
                    # Create a new thread for each client
                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_socket, address)
                    )
                    client_thread.start()
                    print(f"Started thread {client_thread.name} for client {address}")

    def accept_client_connection(self) -> tuple[socket.socket, tuple[str, int]]:
        """Accept client connection and return client socket and address"""
        # accept connections from outside
        client_socket, address = self.cdn_socket.accept()
        print(f"Accepted connection from client: {address}")
        return client_socket, address

    def accept_node_connection(self) -> tuple[socket.socket, tuple[str, int]]:
        pass
    
    def handle_node(self, node_socket: socket.socket, node_address: tuple[str, int]):
        pass

    def begin_election(self):
        self.current_term += 1
        self.voted_for = self.in_socket.getsockname()
        
        # send RequestVote RPCs to all other nodes
        RequestVote(self.current_term, self.in_socket.getsockname(), len(self.log), self.log[-1][0], self.out_socket.getsockname())


    def handle_client(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ):
        """Handle client connection by relaying traffic between client and origin server
        - The CDN server communicates with the client through ``client_socket`` and the
        origin server through ``origin_socket`` (see below)
        - Establish a TCP connection to the origin server
        - Create two threads to ``relay_messages()`` bidirectionally
        """
        print(f"Handling client {client_address} in a separate thread...")
        origin_socket = None
        try:
            # Connect to the origin server
            origin_socket = self.connect_to_origin()

            # Create threads to relay messages in both directions
            client_to_origin_thread = threading.Thread(
                target=self.relay_messages, args=(client_socket, origin_socket)
            )
            origin_to_client_thread = threading.Thread(
                target=self.relay_messages, args=(origin_socket, client_socket)
            )

            # Start both threads
            client_to_origin_thread.start()
            origin_to_client_thread.start()

            print(f"Started message relay threads for client {client_address}")

            # Wait for both threads to finish
            client_to_origin_thread.join()
            origin_to_client_thread.join()
            print(f"Message relay completed for client {client_address}")

        except Exception as e:
            print(f"Error while handling client {client_address}: {e}")
        finally:
            # Ensure both sockets are closed after the forwarding is done
            print("Closing client and origin sockets...")
            client_socket.close()
            if origin_socket:
                origin_socket.close()
            print(f"Both sockets closed for client {client_address}.")


    def connect_to_origin(self) -> socket.socket:
        """Connect to the origin server and return the socket object"""
        ...
        print(f"Connecting to the origin server at {self.origin_addr}:{self.origin_port}...")
        origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin_socket.connect((self.origin_addr, self.origin_port))
        print(f"Connected to the origin server at {self.origin_addr}:{self.origin_port}")
        return origin_socket

    def relay_messages(self, src_socket: socket.socket, dst_socket: socket.socket):
        """Relay messages from the source socket to the destination socket
        - This method should receive data from the source socket and send it to the
        destination socket.
        - This method returns when the source finishes sending data and initiates 
        graceful closure of TCP connection (i.e., when ``socket.recv()`` returns 
        an empty byte string). The connection will enter a half-closed state.
        """
        print(f"Starting message relay from {src_socket.getsockname()} to {dst_socket.getsockname()}...")
        while True:
            try:
                data = src_socket.recv(4096)
                if not data:
                    print(f"No more data from {src_socket.getsockname()}. Closing connection...")
                    break
                print(f"Received {len(data)} bytes. Forwarding to {dst_socket.getsockname()}...")
                dst_socket.sendall(data)
            except socket.error as e:
                print(f"Socket error during message relay: {e}")
                break
        print(f"Message relay from {src_socket.getsockname()} completed.")


    def broadcast_port(self):
        # broadcast the port number to all the nodes in the network
        return self.out_socket.getsockname(), self.socket.getsockname()
    
    def commit(self, data):
        # append the data to a text file 
        with open("data.txt", "a") as f:
            f.write(data)
        self.data
    
    def learn_ports(self, ports):
        # learn the ports of the other nodes in the network
        pass

    def heartbeat(self):
        while(self.status == "Leader"):
            time.sleep(5) # send heartbeat every 5 seconds
            self.out_socket.sendall("Heartbeat")
            print("Heartbeat sent")
        pass
        
    def await_heartbeat(self):
        # if I get heartbeat, I will reset the election timer, else I will start the election
        pass
    def election(self):
        # start the election process
        print("Starting election")
        pass

    def start(self):    
        if self.status == "Leader":
            heartbeat_thread = threading.Thread(target=self.heartbeat)
            heartbeat_thread.start()
        else:
            election_thread = threading.Thread(target=self.election)
            election_thread.start() 
        while True: 
            conn, addr = self.socket.accept()
            data = conn.recv(1024)
            print("Received data: ", data)
            if data == "Heartbeat":
                print("Received heartbeat")
            else:
                print("Received election message")
                # start election process
                self.election()
            conn.close()    
 
