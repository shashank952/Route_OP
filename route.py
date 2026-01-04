import heapq

# ================= Vehicle fixed costs =================
VEHICLE_COSTS = {
    "Bike": 50,
    "Car": 200,
    "MiniVan": 300,
    "SUV": 400,
    "Pickup Truck": 500
}

# ================= Graph & K-shortest paths (Yen-like) =================
class Graph:
    def __init__(self, matrix):
        self.V = len(matrix)
        self.adj = matrix

    def dijkstra(self, source, destination):
        """Return shortest path as list of node indices, or [] if unreachable."""
        dist = [float('inf')] * self.V
        parent = [-1] * self.V
        visited = [False] * self.V
        dist[source] = 0

        for _ in range(self.V):
            u = -1
            u_min = float('inf')
            for i in range(self.V):
                if not visited[i] and dist[i] < u_min:
                    u_min = dist[i]
                    u = i
            if u == -1:
                break
            visited[u] = True
            if u == destination:
                break

            for v in range(self.V):
                w = self.adj[u][v]
                if not visited[v] and w > 0 and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u

        if dist[destination] == float('inf'):
            return []  # unreachable

        # Reconstruct path
        path = []
        v = destination
        while v != -1:
            path.append(v)
            v = parent[v]
        return path[::-1]

    def get_total_distance(self, path):
        if not path or len(path) < 2:
            return 0
        return sum(self.adj[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def k_shortest_paths(self, source, destination, k=3):
        """Simple Yen-like approach on an adjacency matrix (undirected)."""
        shortest_paths = []
        first_path = self.dijkstra(source, destination)
        if not first_path:
            return []

        shortest_paths.append(first_path)
        candidates = []

        for i in range(len(first_path) - 1):
            spur_node = first_path[i]
            root_path = first_path[:i + 1]

            removed_edges = []
            # Remove edges that would recreate the same root_path
            for p in shortest_paths:
                if len(p) > i and p[:i + 1] == root_path:
                    u, v = p[i], p[i + 1]
                    if self.adj[u][v] != 0:
                        removed_edges.append((u, v, self.adj[u][v]))
                        # Temporarily remove both directions (treat as undirected)
                        self.adj[u][v] = 0
                        self.adj[v][u] = 0

            spur_path = self.dijkstra(spur_node, destination)
            if spur_path and spur_path[0] == spur_node:
                total_path = root_path[:-1] + spur_path
                # Avoid duplicates
                if all(total_path != s for s in shortest_paths):
                    heapq.heappush(
                        candidates,
                        (self.get_total_distance(total_path), total_path)
                    )

            # Restore removed edges
            for u, v, w in removed_edges:
                self.adj[u][v] = w
                self.adj[v][u] = w

        # Pop the next-best candidates until we have k paths
        while candidates and len(shortest_paths) < k:
            _, path = heapq.heappop(candidates)
            shortest_paths.append(path)

        return shortest_paths

# ================= Cost Calculator =================
class CostCalculator:
    @staticmethod
    def fuel_cost(distance, mileage, petrol_price):
        return (distance / mileage) * petrol_price if mileage > 0 else 0

    @staticmethod
    def passenger_cost(passengers, rate):
        return passengers * rate

    @staticmethod
    def toll_charges(segments, rate):
        return segments * rate

    @staticmethod
    def maintenance_cost(distance, rate_per_km):
        return distance * rate_per_km

# ================= Data =================
places = [
    "Central Bus Stand", "Belagavi Railway Station", "KLE University",
    "Tilakwadi", "Camp Area", "Fort Lake", "Shivaji Garden",
    "Ramdev Hotel", "RPD College", "Military Mahadev Temple"
]

matrix = [
    [0, 2, 5, 0, 3, 6, 7, 0, 8, 9],
    [2, 0, 0, 6, 0, 3, 7, 9, 0, 8],
    [5, 0, 0, 3, 7, 0, 5, 8, 2, 6],
    [0, 6, 3, 0, 4, 5, 3, 7, 0, 5],
    [3, 0, 7, 4, 0, 2, 4, 6, 5, 7],
    [6, 3, 0, 5, 2, 0, 3, 5, 4, 6],
    [7, 7, 5, 3, 4, 3, 0, 4, 6, 8],
    [0, 9, 8, 7, 6, 5, 4, 0, 7, 9],
    [8, 0, 2, 0, 5, 4, 6, 7, 0, 4],
    [9, 8, 6, 5, 7, 6, 8, 9, 4, 0]
]

# ================= Main API =================
def calculate_route_with_alternatives(
    source_name,
    dest_name,
    passengers,
    fuel_available,
    mileage,
    vehicle_type
):
    # Validate inputs
    location_index = {name: idx for idx, name in enumerate(places)}
    if source_name not in location_index or dest_name not in location_index:
        return {"error": "Invalid source or destination"}

    if source_name == dest_name:
        return {"error": "Source and destination cannot be the same"}

    graph = Graph([row[:] for row in matrix])

    source_idx = location_index[source_name]
    dest_idx = location_index[dest_name]

    paths = graph.k_shortest_paths(source_idx, dest_idx, k=3)
    if not paths:
        return {"error": "No path found between the selected locations"}

    results = []
    # Use default mileage if invalid
    effective_mileage = mileage if mileage and mileage > 0 else 15.0
    petrol_price = 90  # ₹/liter
    pax_rate = 10      # ₹ per passenger (flat)
    toll_rate = 15     # ₹ per segment
    maintenance_rate = 1.5  # ₹ per km
    vehicle_cost = VEHICLE_COSTS.get(vehicle_type, 0)

    for path in paths:
        total_distance = graph.get_total_distance(path)

        fuel_cost = CostCalculator.fuel_cost(total_distance, effective_mileage, petrol_price)
        passenger_cost = CostCalculator.passenger_cost(passengers, pax_rate)
        toll = CostCalculator.toll_charges(len(path) - 1, toll_rate)
        maintenance = CostCalculator.maintenance_cost(total_distance, maintenance_rate)

        total_cost = fuel_cost + passenger_cost + toll + maintenance + vehicle_cost

        results.append({
            "route": [places[i] for i in path],          # list of stop names, for vertical display
            "total_distance": round(total_distance, 2),
            "fuel_cost": round(fuel_cost, 2),
            "passenger_cost": round(passenger_cost, 2),
            "toll": round(toll, 2),
            "maintenance": round(maintenance, 2),
            "vehicle_cost": round(vehicle_cost, 2),
            "total_cost": round(total_cost, 2)
        })

    return results
