from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from graph import Graph
except ImportError as e:
    print(f"Error importing graph module: {e}")
    sys.exit(1)

app = Flask(__name__, template_folder='../templates')
app.config['DEBUG'] = True

# Initialize graph
graph = Graph()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/load_data', methods=['POST'])
def load_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data received'
            })
        
        filename = data.get('filename', 'semarang.txt')
        
        # Check if file exists
        if not os.path.exists(filename):
            return jsonify({
                'success': False,
                'message': f'File {filename} not found'
            })
        
        graph.load_from_file(filename)
        nodes_data = []
        for node in graph.nodes.values():
            nodes_data.append({
                'name': node.name,
                'latitude': node.latitude,
                'longitude': node.longitude,
                'neighbors': node.neighbors
            })
        
        return jsonify({
            'success': True,
            'nodes': nodes_data,
            'message': f'Data loaded from {filename}. Found {len(nodes_data)} nodes.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading data: {str(e)}'
        })

@app.route('/find_path', methods=['POST'])
def find_path():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data received'
            })
        
        start = data.get('start')
        end = data.get('end')
        
        if not start or not end:
            return jsonify({
                'success': False,
                'message': 'Start and end locations are required'
            })
        
        if start not in graph.nodes or end not in graph.nodes:
            return jsonify({
                'success': False,
                'message': f'Location not found. Available locations: {list(graph.nodes.keys())}'
            })
        
        path, distance = graph.dijkstra(start, end)
        
        if not path:
            return jsonify({
                'success': False,
                'message': 'No path found between the locations'
            })
        
        # Get coordinates for the path
        path_coordinates = []
        for location in path:
            if location in graph.nodes:
                node = graph.nodes[location]
                path_coordinates.append({
                    'name': location,
                    'lat': node.latitude,
                    'lng': node.longitude
                })
        
        return jsonify({
            'success': True,
            'path': path,
            'distance': distance,
            'coordinates': path_coordinates
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error finding path: {str(e)}'
        })

@app.route('/get_nodes')
def get_nodes():
    try:
        nodes = list(graph.nodes.keys())
        return jsonify(nodes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    return "Flask is working!"

if __name__ == '__main__':
    print("Starting Semarang Pathfinder...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Template folder: {app.template_folder}")
    
    # Check if semarang.txt exists
    if os.path.exists('semarang.txt'):
        print("semarang.txt found")
        try:
            graph.load_from_file('semarang.txt')
            print(f"Loaded {len(graph.nodes)} nodes from semarang.txt")
            graph.display_nodes()
        except Exception as e:
            print(f"Error loading semarang.txt: {e}")
    else:
        print("semarang.txt not found in current directory")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
