import http.server
import socketserver
import json

PORT = 8080
JSON_FILE = "data.json"

# Load the JSON file once before starting the server
try:
    with open(JSON_FILE, "r") as file:
        buffered_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    buffered_data = {"error": "Invalid or missing JSON file"}


class JSONHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(buffered_data).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())


if __name__ == "__main__":
    print(f"Loaded data from {JSON_FILE}: {buffered_data}")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), JSONHTTPRequestHandler) as httpd:
        print(f"Serving JSON on port {PORT}")
        httpd.serve_forever()
