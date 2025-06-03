import math
import heapq
from typing import Dict, List, Tuple, Optional

def heuristic_distance(node1: Tuple[int, int], node2: Tuple[int, int]) -> float:
    """Menghitung jarak heuristik menggunakan jarak Euclidean"""
    x1, y1 = node1
    x2, y2 = node2
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance * 10  # 10 meter per grid

def hitung_semua_jarak(pasangan_titik: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]):
    """Menghitung dan menampilkan semua jarak heuristik"""
    print("=== JARAK HEURISTIK SEMUA PASANGAN TITIK ===")
    for label, (start, goal) in pasangan_titik.items():
        jarak = heuristic_distance(start, goal)
        print(f"Jarak dari {label}: {jarak:.2f} meter")
    print()

class AStar:
    def __init__(self):
        self.graph = {}
        self.coordinates = {}
        self.f_values = []

    def build_graph(self, pasangan: Dict[str, List[List[int]]], f_values: List[float]):
        """Membangun graf dari data koordinat dan nilai f(n)"""
        self.f_values = f_values
        for index, (edge, coords) in enumerate(pasangan.items()):
            start_coord, end_coord = coords
            start_name, end_name = edge.split(' ke ')

            self.coordinates[start_name] = tuple(start_coord)
            self.coordinates[end_name] = tuple(end_coord)

            if start_name not in self.graph:
                self.graph[start_name] = []
            if end_name not in self.graph:
                self.graph[end_name] = []

            cost = f_values[index] if index < len(f_values) else heuristic_distance(start_coord, end_coord)

            self.graph[start_name].append({'node': end_name, 'cost': cost})
            self.graph[end_name].append({'node': start_name, 'cost': cost})

    def a_star_search(self, start: str, goal: str) -> Optional[Dict]:
        if start not in self.coordinates or goal not in self.coordinates:
            return None

        open_set = []
        heapq.heappush(open_set, (0, start, 0, [start]))

        closed_set = set()
        best_g_score = {start: 0}

        while open_set:
            current_f, current_node, current_g, current_path = heapq.heappop(open_set)

            if current_node == goal:
                return {
                    'path': current_path,
                    'total_cost': current_g,
                    'steps': len(current_path) - 1,
                    'f_score': current_f
                }

            if current_node in closed_set:
                continue
            closed_set.add(current_node)

            if current_node in self.graph:
                for neighbor_info in self.graph[current_node]:
                    neighbor = neighbor_info['node']
                    edge_cost = neighbor_info['cost']

                    if neighbor in closed_set:
                        continue

                    tentative_g = current_g + edge_cost

                    if neighbor not in best_g_score or tentative_g < best_g_score[neighbor]:
                        best_g_score[neighbor] = tentative_g
                        h_score = heuristic_distance(self.coordinates[neighbor], self.coordinates[goal])
                        f_score = tentative_g + h_score
                        new_path = current_path + [neighbor]
                        heapq.heappush(open_set, (f_score, neighbor, tentative_g, new_path))

        return None

    def display_route_details(self, result: Dict):
        if not result:
            return

        print("📋 DETAIL LANGKAH-LANGKAH:")
        path = result['path']
        total_distance = 0

        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            from_coord = self.coordinates[from_node]
            to_coord = self.coordinates[to_node]
            distance = heuristic_distance(from_coord, to_coord)
            total_distance += distance

            print(f"{i + 1}. {from_node} {from_coord} → {to_node} {to_coord} | Jarak: {distance:.2f} meter")

        print(f"\nTotal jarak heuristik: {total_distance:.2f} meter")

def main():
    pasangan = {
        "A ke B": [[40, 5], [38, 5]],
        "B ke C": [[38, 5], [38, 12]],
        "B ke D": [[38, 5], [34, 5]],
        "D ke F": [[34, 5], [34, 11]],
        "C ke E": [[38, 12], [36, 12]],
        "E ke G": [[36, 12], [36, 14]],
        "E ke F": [[36, 12], [34, 11]],
        "F ke H": [[34, 11], [34, 14]],
        "I ke J": [[35, 14], [35, 17]],
        "J ke K": [[35, 17], [35, 24]],
        "H ke V": [[34, 14], [27, 13]],
        "J ke N": [[35, 17], [29, 16]],
        "N ke O": [[29, 16], [24, 16]],
        "O ke P": [[24, 16], [20, 16]],
        "U ke O": [[24, 13], [24, 16]],
        "V ke U": [[27, 13], [24, 13]],
        "U ke T": [[24, 13], [21, 13]],
        "D ke Y": [[34, 5], [28, 4]],
        "Y ke W": [[28, 4], [27, 9]],
        "Y ke Z": [[28, 4], [20, 3]],
        "W ke X": [[27, 9], [21, 10]],
        "Z ke X": [[20, 3], [21, 10]],
        "X ke T": [[21, 10], [21, 13]],
        "T ke P": [[21, 13], [20, 16]],
        "K ke L": [[35, 24], [29, 24]],
        "L ke R": [[29, 24], [25, 24]],
        "R ke S": [[25, 24], [25, 25]],
        "S ke Q": [[25, 25], [19, 24]],
        "P ke Q": [[20, 16], [19, 24]],
        "Z ke AA": [[20, 4], [16, 2]],
        "AA ke AB": [[16, 5], [10, 10]],
        "AB ke AC": [[10, 10], [3, 17]],
        "AC ke AD": [[3, 17], [7, 20]],
        "AB ke M": [[10, 10], [11, 23]],
        "AD ke M": [[7, 20], [11, 23]],
        "Q ke M": [[19, 24], [11, 23]],
        "G ke I": [[36, 14], [35, 14]],
        "I ke H": [[35, 14], [34, 14]],
    }

    f_values = [22, 77, 44, 66, 22, 22, 25.36, 33, 33, 77, 77.71, 66.83, 55, 44, 33, 33, 33, 66.83, 56.99, 88.62,
                67.83, 77.71, 33, 34.62, 66, 44, 11, 66.83, 88.62, 48.72, 84.1, 105.99, 54, 143.38, 54, 88.62]

    print("🔍 IMPLEMENTASI ALGORITMA A* UNTUK PENCARIAN RUTE TERPENDEK")
    print("=" * 60)

    hitung_semua_jarak(pasangan)

    a_star = AStar()
    a_star.build_graph(pasangan, f_values)

    print("📊 INFORMASI GRAF:")
    print(f"Total nodes: {len(a_star.coordinates)}")
    print(f"Total edges: {len(pasangan)}\n")

    print("📍 KOORDINAT SEMUA TITIK:")
    for node, coord in sorted(a_star.coordinates.items()):
        print(f"{node}: {coord}")
    print()

    print("🎯 PENCARIAN RUTE TERPENDEK DARI A KE M")
    print("-" * 40)
    result = a_star.a_star_search('A', 'M')

    if result:
        print("✅ RUTE TERPENDEK DITEMUKAN!")
        print(f"📍 Path: {' → '.join(result['path'])}")
        print(f"💰 Total Cost (f(n)): {result['total_cost']:.2f}")
        print(f"📏 Jumlah Langkah: {result['steps']}")
        print(f"🎯 F-Score: {result['f_score']:.2f}\n")
        a_star.display_route_details(result)
        print("\n🏁 KESIMPULAN:")
        print(f"Rute terpendek dari titik A ke titik M adalah: {' → '.join(result['path'])}")
        print(f"dengan total cost {result['total_cost']:.2f} unit.")
    else:
        print("❌ Tidak ada rute yang ditemukan dari A ke M")

if __name__ == "__main__":
    main()
