import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Function to load student data from the JSON file
def load_student_data():
    with open('q-vercel-python.json', 'r') as f:
        return json.load(f)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(self.path[2:])
        names = query_components.get("name", [])

        # Load student data from the JSON file
        student_marks = load_student_data()

        # Fetch marks for each student
        marks = [student_marks.get(name, "Not Found") for name in names]

        # Prepare JSON response
        response = {"marks": marks}

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
