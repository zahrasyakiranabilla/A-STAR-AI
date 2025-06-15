from flask import Flask, render_template, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graph import Graph

app = Flask(__name__, template_folder='../templates')
app.config['DEBUG'] = True

graph = Graph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.get_json()
    filename = data.get('filename', 'semarang.txt')
    if not os.path.exists(filename):
        return jsonify({'success': False, 'message': f'File {filename} not found'})
    try:
        graph.load_from_file(filename)
        nodes_data = [{
            'name': n.name,
            'latitude': n.latitude,
            'longitude': n.longitude,
            'neighbors': n.neighbors
        } for n in graph.nodes.values()]
        return jsonify({
            'success': True,
            'nodes': nodes_data,
            'message': f'Data loaded from {filename}. Found {len(nodes_data)} nodes.'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    if not start or not end:
        return jsonify({'success': False, 'message': 'Start and end required'})
    if start not in graph.nodes or end not in graph.nodes:
        return jsonify({'success': False, 'message': 'Node not found'})
    path, total_distance, segments = graph.astar(start, end)
    if not path:
        return jsonify({'success': False, 'message': 'No path found with A*'})
    coordinates = [{'name': p, 'lat': graph.nodes[p].latitude, 'lng': graph.nodes[p].longitude} for p in path]
    return jsonify({
        'success': True,
        'path': path,
        'total_distance': total_distance,
        'segments': segments,
        'coordinates': coordinates
    })

@app.route('/get_nodes')
def get_nodes():
    return jsonify(list(graph.nodes.keys()))

@app.route('/test')
def test():
    return "Flask is working!"

if __name__ == '__main__':
    print("Starting Semarang Pathfinder with A* Algorithm...")
    if os.path.exists('semarang.txt'):
        try:
            graph.load_from_file('semarang.txt')
            print(f"Loaded {len(graph.nodes)} nodes from semarang.txt")
        except Exception as e:
            print(f"Error loading semarang.txt: {e}")
    else:
        print("semarang.txt not found")
    app.run(debug=True, host='127.0.0.1', port=5000)
