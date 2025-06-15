import math
from typing import Dict, List, Tuple
import os

class Node:
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors: List[str] = []

    def add_neighbor(self, neighbor: str):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __str__(self):
        return f"Name: {self.name}\nLatitude: {self.latitude}\nLongitude: {self.longitude}\nNeighbours: {', '.join(self.neighbors)}"

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, name: str, latitude: float, longitude: float):
        self.nodes[name] = Node(name, latitude, longitude)

    def add_edge(self, node1: str, node2: str):
        if node1 in self.nodes:
            self.nodes[node1].add_neighbor(node2)
        if node2 in self.nodes:
            self.nodes[node2].add_neighbor(node1)

    def calculate_distance(self, node1: str, node2: str) -> float:
        if node1 not in self.nodes or node2 not in self.nodes:
            return float('inf')

        try:
            lat1, lon1 = math.radians(self.nodes[node1].latitude), math.radians(self.nodes[node1].longitude)
            lat2, lon2 = math.radians(self.nodes[node2].latitude), math.radians(self.nodes[node2].longitude)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            r = 6371  # km
            return c * r
        except Exception as e:
            print(f"Error calculating distance between {node1} and {node2}: {e}")
            return float('inf')

    def astar(self, start: str, end: str) -> Tuple[List[str], float, List[dict]]:
        """
        A* pathfinding algorithm implementation
        Uses heuristic function (straight-line distance) to guide search
        """
        if start not in self.nodes or end not in self.nodes:
            return [], 0, []

        open_set = {start}
        came_from = {}
        g_score = {node: float('inf') for node in self.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.nodes}
        f_score[start] = self.calculate_distance(start, end)

        while open_set:
            current = min(open_set, key=lambda node: f_score[node])
            if current == end:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()

                # Calculate segments and total distance
                segments = []
                total_distance = 0
                for i in range(len(path) - 1):
                    dist = self.calculate_distance(path[i], path[i+1])
                    total_distance += dist
                    segments.append({
                        'from': path[i],
                        'to': path[i+1],
                        'distance': dist
                    })

                return path, total_distance, segments

            open_set.remove(current)
            for neighbor in self.nodes[current].neighbors:
                tentative_g = g_score[current] + self.calculate_distance(current, neighbor)
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.calculate_distance(neighbor, end)
                    open_set.add(neighbor)

        return [], 0, []

    def load_from_file(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found!")

        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        node_blocks = content.split('\n\n')

        for block in node_blocks:
            if not block.strip():
                continue
            lines = block.strip().split('\n')
            if len(lines) < 4:
                continue
            try:
                name = lines[0].split('Name: ')[1].strip()
                latitude = float(lines[1].split('Latitude: ')[1].strip())
                longitude = float(lines[2].split('Longitude: ')[1].strip())
                neighbors_line = lines[3].split('Neighbours: ')[1].strip()
                neighbors = [n.strip() for n in neighbors_line.split(',') if n.strip()]
                self.add_node(name, latitude, longitude)
            except (IndexError, ValueError):
                continue

        for block in node_blocks:
            lines = block.strip().split('\n')
            if len(lines) < 4:
                continue
            try:
                name = lines[0].split('Name: ')[1].strip()
                neighbors_line = lines[3].split('Neighbours: ')[1].strip()
                neighbors = [n.strip() for n in neighbors_line.split(',') if n.strip()]
                for neighbor in neighbors:
                    if neighbor in self.nodes:
                        self.add_edge(name, neighbor)
            except (IndexError, ValueError):
                continue

    def display_nodes(self):
        print("Daftar Node:")
        for node in self.nodes.values():
            print(node)
            print()
