import threading
import time
import socket


class RPC:
    '''Base class for all RPC messages'''
    def __init__(self, leader_addr_port:tuple, follower_addr_ports:list[tuple]):
        self.leader_addr_port = leader_addr_port
        self.follower_addr_ports = follower_addr_ports
        
class Heartbeat(RPC, threading.Thread):
    def __init__(self, leader_addr_port:tuple, follower_addr_ports:list[tuple]):
        """
        The heartbeat message is sent by the leader to all the followers to maintain its authority.
        When a follower receives a heartbeat message, it resets its election timer.
        """
        RPC.__init__(self, leader_addr_port,follower_addr_ports)
        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        while True:
            time.sleep(5)
            for addr_port in self.follower_addr_ports:
                s = socket.socket(self.leader_addr_port)
                s.connect(addr_port)
                s.sendall("Heartbeat")
            s.close()
    
class RequestVote(RPC,threading.Thread):
    def __init__(self, term, candidate_id, last_log_index, last_log_term, follower_ports):
        RPC.__init__(self, None, follower_ports)
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        for addr_port in self.follower_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(addr_port)
            s.sendall("RequestVote")
            s.close()
        
    def run(self):
        pass

   

class AppendEntries(RPC):
    def __init__(self, term, candidate_id):
        self.term = term
        self.candidate_id = candidate_id