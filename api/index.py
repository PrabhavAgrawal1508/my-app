class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api"):
            # Your code for handling API requests
            self.handle_api_request()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def handle_api_request(self):
        # Parse query parameters
        query_components = parse_qs(self.path[5:])  # Skip '/api?' part
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
