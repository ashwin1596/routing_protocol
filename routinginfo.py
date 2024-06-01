class RoutingInfo:
    __slots__ = 'dest_ip', 'subnet_mask', 'next_hop', 'intf', 'cost_to_dest', 'time_elapsed'

    def __init__(self, dest_ip, subnet_mask, cost_to_dest, next_hop, intf=None, time_elapsed=1):
        self.dest_ip = dest_ip
        self.subnet_mask = subnet_mask
        self.next_hop = next_hop
        self.intf = intf
        self.cost_to_dest = cost_to_dest
        self.time_elapsed = time_elapsed

    @classmethod
    def to_dict(cls, dict_data):
        return {"dest_ip": dict_data.dest_ip,
                "subnet_mask": dict_data.subnet_mask,
                "next_hop": dict_data.next_hop,
                "intf": dict_data.intf,
                "cost_to_dest": dict_data.cost_to_dest,
                "time_elapsed": dict_data.time_elapsed}

    @classmethod
    def from_dict(cls, dict_data):
        dest_ip = dict_data.get("dest_ip")
        subnet_mask = dict_data.get("subnet_mask")
        next_hop = dict_data.get("next_hop")
        intf = dict_data.get("intf")
        cost_to_dest = dict_data.get("cost_to_dest")
        time_elapsed = dict_data.get("time_elapsed")

        return cls(dest_ip=dest_ip, subnet_mask=subnet_mask, next_hop=next_hop,
                   intf=intf, cost_to_dest=cost_to_dest, time_elapsed=time_elapsed)

    def get_cost(self):
        return self.cost_to_dest

    def set_next_hop(self, next_hop):
        self.next_hop = next_hop

    def set_intf(self, intf):
        self.intf = intf

    def set_cost(self, cost):
        self.cost_to_dest = cost
