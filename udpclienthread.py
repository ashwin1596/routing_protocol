import socket
import time
import json

from routinginfo import RoutingInfo


class UDPClientThread:
    """
    Runs as a thread and sends the routing table updates to the neighbours by calling send_update() of VirtualRouter
    """

    __slots__ = "routing_table", "sleep_time"

    def __init__(self, routing_table):
        self.routing_table = routing_table
        self.sleep_time = 1

    def send(self, sendToIP, sendToPort):
        """
        Sends the data to the server.
        :param sendToIP: destination ip
        :param sendToPort: destination port
        :return: None
        """

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            dict_data = routing_table_to_dict(self.routing_table)
            data_bytes = json.dumps(dict_data).encode('utf-8')
            udp_socket.sendto(data_bytes, (sendToIP, sendToPort))
            time.sleep(self.sleep_time)


def routing_table_to_dict(routing_table):
    routing_table_dict = {}

    for router in routing_table:
        routing_table_dict[router] = RoutingInfo.to_dict(routing_table[router])

    return routing_table_dict
