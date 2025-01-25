import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Function to load student data from the JSON file
def load_student_data():
    try:
        with open('q-vercel-python.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters safely using urlparse
        parsed_url = urlparse(self.path)
        query_components = parse_qs(parsed_url.query)
        names = query_components.get("name", [])

        if not names:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No 'name' query parameter provided"}).encode('utf-8'))
            return

        # Load student data from the JSON file
        student_marks = load_student_data()

        if "error" in student_marks:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Failed to load student data"}).encode('utf-8'))
            return

        # Fetch marks for each student
        marks = [student_marks.get(name, "Not Found") for name in names]

        # Prepare JSON response
        response = {"marks": marks}

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        self.wfile.write(json.dumps(response).encode)
