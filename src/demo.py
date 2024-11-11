import threading 

def main(): 
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
