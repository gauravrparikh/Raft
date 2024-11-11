import threading 
import logging 

import server
import client 

def main(): 
    logging.basicConfig(level=logging.DEBUG)
    servers, clients=setup()
    clients[0].log_data()

    #make 5 servers
    # make 2 clients 
    # start the servers
    # start the clients
    # ask client to log data to one of the servers
    # check if the data is replicated on all servers
    # kill one of the servers
    # see if the voting mechanism works
    # ask client to log data to one of the servers
    # check if the data is replicated on all servers
    # end the program
    pass
def setup():
    server_in_socket_ports = [4444, 4445, 4446, 4447, 4448]
    server_out_socket_ports = [4449, 4450, 4451, 4452, 4453]
    client_in_socket_ports = [4454, 4455]
    client_out_socket_ports = [4456, 4457]
    servers = []
    for i in range(5):
        servers.append(server.Server(data = "data", election_time_out = 5, role = "Follower", in_socket_port = server_in_socket_ports[i], out_socket_port = server_out_socket_ports[i]))
        servers[i].start()
    clients = []
    for i in range(2):
        clients.append(client.Client(data = "data", server_addr = "localhost", server_port = client_in_socket_ports[i], client_port = client_out_socket_ports[i]))
        clients[i].start()
    return servers, clients

if __name__ == "__main__":
    main()


# def run_proxy(
#     level: ProxyServerLevel | int,
#     cdn_addr: str = "127.0.0.1",
#     cdn_port: int = 4444,
#     origin_addr: str = "",
#     origin_port: int = 443,
#     cert_file: str = "certs/cdn_cert.pem",
#     key_file: str = "certs/cdn_key.pem",
#     origin_domain: str = "",
#     ignore_query_string: bool = False,
# ):
#     proxy_server = create_proxy_server(
#         level,
#         cdn_addr,
#         cdn_port,
#         origin_addr,
#         origin_port,
#         cert_file,
#         key_file,
#         origin_domain,
#         ignore_query_string,
#     )
#     proxy_server.start()


# if __name__ == "__main__":
#     fire.Fire(run_proxy)
