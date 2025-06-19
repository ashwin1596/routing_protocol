# RIP Routing: Intelligent Network Pathfinding (https://youtu.be/ftX1EpgKN1s)

A dynamic network routing protocol that optimizes path selection and prevents routing inefficiencies in complex network environments.

## Problem Solved

Traditional routing mechanisms struggle with adapting to network changes, creating inefficient and potentially unstable communication paths.

## Implementation Highlights
- Implemented the RIP distance-vector routing protocol to enable dynamic routing and shortest path computation using Python 
and UDP. 
- Developed periodic route updates, CIDR support, and dynamic routing table adjustments for efficient network routing. 
- Applied 'split-horizon' with poisoned reverse to prevent routing loops and the count-to-infinity problem. 

## 🔄 Core Features

### 1. Periodic Route Updates
- Automatic update broadcasts every 30 seconds
- Immediate updates on topology changes
- Configurable update intervals

### 2. Dynamic Routing Table
- Real-time route computation
- Path cost calculation
- Next-hop determination
- Route invalidation and cleanup

### 3. CIDR Support
- Classless Inter-Domain Routing
- Subnet mask handling
- Network aggregation
- Variable-length subnet masks

### 4. Split-Horizon with Poisoned Reverse
- Loop prevention mechanism
- Infinite metric for poisoned routes
- Split-horizon rule implementation
- Count-to-infinity prevention

## 🛠️ Implementation Details

### Router (`router.py`)
```python
class Router:
    def __init__(self, router_id, neighbors):
        self.router_id = router_id
        self.neighbors = neighbors
        self.routing_table = RoutingTable()
        self.update_interval = 30  # seconds

    def start(self):
        """Initializes router and starts UDP threads"""
        self.server_thread.start()
        self.client_thread.start()
```

### Routing Information (`routinginfo.py`)
```python
class RoutingTable:
    def __init__(self):
        self.routes = {}
        self.invalid_timeout = 180  # seconds
        self.flush_timeout = 240    # seconds

    def update_route(self, destination, next_hop, metric):
        """Updates routing table entry with new information"""
        if metric + 1 >= 16:  # RIP infinite metric
            self.invalidate_route(destination)
        else:
            self.routes[destination] = Route(next_hop, metric + 1)
```

### Virtual Router (`virtualrouter.py`)
```python
class VirtualRouter:
    def __init__(self, config_file):
        self.topology = Topology(config_file)
        self.router = Router(self.topology.router_id)
        
    def process_update(self, update):
        """Processes received routing updates"""
        for route in update.routes:
            if self.apply_split_horizon(route):
                continue
            self.update_routing_table(route)
```

## 🚀 Usage

### Starting a Router
```bash
python virtualrouter.py --config router1.conf
```

### Configuration File Format
```ini
router_id = 1
neighbors = 2,3,4
networks = 192.168.1.0/24,10.0.0.0/8
update_interval = 30
```

## 📊 Network Features

### Route Processing
```python
def process_route_update(self, route):
    """
    Process incoming route updates
    Implements split-horizon with poisoned reverse
    """
    if route.next_hop == self.router_id:
        route.metric = 16  # Poison reverse
    elif route.metric + 1 < 16:
        self.routing_table.update(route)
```

### CIDR Implementation
```python
class NetworkAddress:
    def __init__(self, address, mask):
        self.address = address
        self.mask = mask

    def matches(self, ip):
        """Check if IP matches network address with mask"""
        return (ip & self.mask) == self.address
```

## 🔧 Configuration Options

```python
DEFAULT_CONFIG = {
    'UPDATE_INTERVAL': 30,    # seconds
    'INVALID_TIMEOUT': 180,   # seconds
    'FLUSH_TIMEOUT': 240,     # seconds
    'MAX_METRIC': 16,         # RIP infinite metric
    'POISON_METRIC': 16,      # Metric for poisoned routes
}
```

## 🧪 Testing

```bash
# Start test network
python test_network.py --routers 4

# Simulate link failure
python test_network.py --fail-link 1-2

# Monitor convergence
python test_network.py --monitor
```

## 📈 Performance Analysis

The implementation has been tested for:
- Convergence time
- CPU and memory usage
- Network overhead
- Route stability

## 🔍 Key Skills Demonstrated

- Python Programming
- Socket Programming
- Concurrent Programming
- UDP Implementation
- Object-Oriented Design
- Network Protocol Implementation

## 📁 Project Structure

```
.
├── router.py           # Core router implementation
├── routinginfo.py     # Routing table and route information
├── topology.py        # Network topology management
├── udpclientthread.py # UDP client for sending updates
├── udpserverthread.py # UDP server for receiving updates
└── virtualrouter.py   # Virtual router simulation
```
