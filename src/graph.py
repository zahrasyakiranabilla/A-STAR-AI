import math
from typing import Dict, List, Tuple, Optional
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
        """Calculate distance between two nodes using Haversine formula"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return float('inf')
        
        try:
            lat1, lon1 = math.radians(self.nodes[node1].latitude), math.radians(self.nodes[node1].longitude)
            lat2, lon2 = math.radians(self.nodes[node2].latitude), math.radians(self.nodes[node2].longitude)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            r = 6371  # Earth's radius in kilometers
            
            return c * r
        except Exception as e:
            print(f"Error calculating distance between {node1} and {node2}: {e}")
            return float('inf')
    
    def dijkstra(self, start: str, end: str) -> Tuple[List[str], float]:
        """Find shortest path using Dijkstra's algorithm"""
        if start not in self.nodes or end not in self.nodes:
            print(f"Start or end node not found: {start}, {end}")
            return [], 0
        
        try:
            distances = {node: float('inf') for node in self.nodes}
            distances[start] = 0
            previous = {}
            unvisited = set(self.nodes.keys())
            
            while unvisited:
                current = min(unvisited, key=lambda node: distances[node])
                
                if current == end:
                    break
                
                if distances[current] == float('inf'):
                    break
                
                unvisited.remove(current)
                
                for neighbor in self.nodes[current].neighbors:
                    if neighbor in unvisited and neighbor in self.nodes:
                        distance = distances[current] + self.calculate_distance(current, neighbor)
                        if distance < distances[neighbor]:
                            distances[neighbor] = distance
                            previous[neighbor] = current
            
            # Reconstruct path
            path = []
            current = end
            while current in previous:
                path.append(current)
                current = previous[current]
            path.append(start)
            path.reverse()
            
            return path, distances[end] if distances[end] != float('inf') else 0
        except Exception as e:
            print(f"Error in dijkstra algorithm: {e}")
            return [], 0
    
    def load_from_file(self, filename: str):
        """Load graph data from file"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found!")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            
            if not content:
                raise ValueError("File is empty")
            
            # Split by double newlines to separate nodes
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
                    
                except (IndexError, ValueError) as e:
                    print(f"Error parsing node block: {block}")
                    print(f"Error: {e}")
                    continue
            
            # Add edges after all nodes are created
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
                    neighbors_line = lines[3].split('Neighbours: ')[1].strip()
                    neighbors = [n.strip() for n in neighbors_line.split(',') if n.strip()]
                    
                    for neighbor in neighbors:
                        if neighbor in self.nodes:
                            self.add_edge(name, neighbor)
                
                except (IndexError, ValueError):
                    continue
                    
        except Exception as e:
            raise Exception(f"Error loading file {filename}: {str(e)}")
    
    def display_nodes(self):
        """Display all nodes information"""
        print("Daftar Node:")
        for node in self.nodes.values():
            print(node)
            print()
