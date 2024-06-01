import threading
import sys
import json
import time

from topology import Topology, get_router_by_ip, get_router_value_by_ip
from router import Router, get_router_by_name, get_enum_from_value
from routinginfo import RoutingInfo
from udpclienthread import UDPClientThread
from udpserverthread import UDPServerThread


class VirtualRouter:
    __slots__ = "name", "topology", "routing_table", "neighbours", "port"

    def __init__(self, name, topology):
        self.name = name
        self.topology = topology
        self.routing_table = {}
        self.neighbours = []
        self.port = 12345
        self.init_routing_table()

    def init_routing_table(self):
        """
        Initialize routing table based on local link costs for immediate neighbors; otherwise set cost to 16(infinite)
        And extracts immediate neighbouring routers
        :return: None
        """
        costs = self.topology.ring_topology[self.name]

        for router in Router:
            if router != self.name:
                next_hop = None
                if costs[router] != 16:
                    next_hop = self.topology.router_ips[router]
                else:
                    next_hop = "unavailable"
                # set routing table
                self.routing_table[router.value] = RoutingInfo(dest_ip=self.topology.network_address[router],
                                                               subnet_mask=self.topology.subnet_masks[router],
                                                               cost_to_dest=costs[router],
                                                               intf=self.port if
                                                               costs[router] != 16 else None,
                                                               next_hop=next_hop)

                # set neighbours
                if costs[router] != 16:
                    self.neighbours.append(router)

        self.routing_table[self.name.value] = RoutingInfo(dest_ip=self.topology.network_address[self.name],
                                                          subnet_mask=self.topology.subnet_masks[self.name],
                                                          cost_to_dest=0,
                                                          intf=None,
                                                          next_hop="0.0.0.0")

    def update_routing_table(self, received_update, sender):
        """
        Update the routing table based on update received from neighbors
        :param received_update: routing table of one of the neighbors
        :param sender: name or ip of routing table's sender
        :return: None
        """

        for router in received_update:
            if router != self.name.value:
                current_dis_to_dest = self.routing_table[router].get_cost()
                neighbour_cost_to_dest = received_update[router].get_cost()
                cost_to_neighbour = self.routing_table[get_router_value_by_ip(sender)].get_cost()

                if current_dis_to_dest > (cost_to_neighbour + neighbour_cost_to_dest):
                    self.routing_table[router].set_next_hop(sender)  # next_hop
                    self.routing_table[router].set_cost(cost_to_neighbour + neighbour_cost_to_dest)  # new cost to dest
                    self.routing_table[router].set_intf(self.port)

    def receive_update(self, data, address):
        """
        Receive table updates from neighbours and process it.
        :return: None
        """

        # convert bytes to RoutingInfo
        data_received = json.loads(data.decode('utf-8'))
        routing_table = routing_table_from_dict(data_received)
        self.update_routing_table(routing_table, address[0])

    def start_clients(self):
        udp_client = UDPClientThread(self.routing_table)
        t1 = threading.Thread(target=udp_client.send, args=(self.topology.router_ips[self.neighbours[0]],
                                                            self.port,))
        t2 = threading.Thread(target=udp_client.send, args=(self.topology.router_ips[self.neighbours[1]],
                                                            self.port,))

        t1.start()
        t2.start()

    def start_server(self):
        udp_server = UDPServerThread(self.topology.router_ips[self.name])

        t1 = threading.Thread(target=udp_server.receive,
                              args=(self, self.port))
        t1.start()

    def start_print_routing_table(self):
        t = threading.Thread(target=print_routing_table, args=(self.routing_table,))
        t.start()


def print_routing_table(routing_table):
    while True:
        print("=" * 76)
        print('{0: <16} | {1: <16} | {2: <16} | {3: <16}'.format("Destination IP", "Subnet Mask",
                                                                 "Next Hop", "Distance"))
        print("-" * 76)
        for _, details in routing_table.items():
            print('{0: <19}{1: <19}{2: <19}{3: <19} '.format(details.dest_ip, details.subnet_mask, details.next_hop,
                                                             details.cost_to_dest))

        print("")
        time.sleep(1)


def routing_table_from_dict(routing_table_dict):
    routing_table = {}

    for router in routing_table_dict:
        routing_table[int(router)] = RoutingInfo.from_dict(routing_table_dict[router])

    return routing_table


def main():
    if len(sys.argv) != 6:
        raise RuntimeError("Missing arguments for  this router's name and costs")

    topo = Topology(sys.argv[2:])
    router_name = get_router_by_name(sys.argv[1])
    router = VirtualRouter(router_name, topo)
    router.start_clients()
    router.start_server()
    router.start_print_routing_table()


if __name__ == '__main__':
    main()
