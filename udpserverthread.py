import socket


class UDPServerThread:
    """
    Runs as a single thread and handles the table updates
    """
    __slots__ = "router_ip"

    def __init__(self, ip):
        self.router_ip = ip

    def receive(self, virtual_router, port):
        """
        Listens on the given port. Receive table updates from neighbours and process it.
        :return: received data as a bytes object
        """
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.router_ip, port))

        while True:
            data, addr = udp_socket.recvfrom(65535)
            virtual_router.receive_update(data, addr)
