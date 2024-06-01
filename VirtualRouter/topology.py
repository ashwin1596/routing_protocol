from router import Router


def get_router_by_ip(ip):
    if ip == "129.21.30.37":
        return Router.QUEEG
    elif ip == "129.21.34.80":
        return Router.COMET
    elif ip == "129.21.37.49":
        return Router.RHEA
    elif ip == "129.21.22.196":
        return Router.GLADOS


def get_router_value_by_ip(ip):
    if ip == "129.21.30.37":
        return Router.QUEEG.value
    elif ip == "129.21.34.80":
        return Router.COMET.value
    elif ip == "129.21.37.49":
        return Router.RHEA.value
    elif ip == "129.21.22.196":
        return Router.GLADOS.value


class Topology:
    __slots__ = "router_ips", "ring_topology", "subnet_masks", "network_address"

    def __init__(self, costs):
        self.router_ips = {}
        self.ring_topology = {}
        self.subnet_masks = {}
        self.network_address = {}

        # setting the data
        self.initialize(list(map(int, costs)))

    def initialize(self, costs):
        self.set_router_ips()
        self.set_topology(costs)
        self.set_subnet_masks()
        self.set_network_address()

    def set_router_ips(self):
        self.router_ips[Router.QUEEG] = "129.21.30.37"
        self.router_ips[Router.COMET] = "129.21.34.80"
        self.router_ips[Router.RHEA] = "129.21.37.49"
        self.router_ips[Router.GLADOS] = "129.21.22.196"

    def set_subnet_masks(self):
        self.subnet_masks[Router.QUEEG] = "255.255.255.0"
        self.subnet_masks[Router.COMET] = "255.255.255.0"
        self.subnet_masks[Router.RHEA] = "255.255.255.0"
        self.subnet_masks[Router.GLADOS] = "255.255.255.0"

    def set_network_address(self):
        self.network_address[Router.QUEEG] = "129.21.30.0"
        self.network_address[Router.COMET] = "129.21.34.0"
        self.network_address[Router.RHEA] = "129.21.37.0"
        self.network_address[Router.GLADOS] = "129.21.22.0"

    def set_topology(self, costs):
        self.ring_topology[Router.QUEEG] = {
            Router.COMET: costs[0],
            Router.GLADOS: costs[3],
            Router.RHEA: 16
        }
        self.ring_topology[Router.COMET] = {
            Router.QUEEG: costs[0],
            Router.RHEA: costs[1],
            Router.GLADOS: 16
        }
        self.ring_topology[Router.RHEA] = {
            Router.COMET: costs[1],
            Router.GLADOS: costs[2],
            Router.QUEEG: 16
        }
        self.ring_topology[Router.GLADOS] = {
            Router.RHEA: costs[2],
            Router.QUEEG: costs[3],
            Router.COMET: 16
        }

    # def set_router_ports(self):
    #     self.router_ports[Router.COMET] = {Router.QUEEG: 12345, Router.RHEA: 12346}
    #     self.router_ports[Router.QUEEG] = {Router.COMET: 12345, Router.GLADOS: 12347}
    #     self.router_ports[Router.RHEA] = {Router.COMET: 12346, Router.GLADOS: 12348}
    #     self.router_ports[Router.GLADOS] = {Router.QUEEG: 12347, Router.RHEA: 12348}
