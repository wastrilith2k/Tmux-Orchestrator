#!/usr/bin/env python3
"""
Simple Mock API Server for Tmux Orchestrator
Provides basic endpoints without external dependencies
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime
import uuid

class MockAPIHandler(http.server.BaseHTTPRequestHandler):

    # Simple in-memory storage
    projects = {}
    agents = {}

    def do_GET(self):
        """Handle GET requests"""
        path = urllib.parse.urlparse(self.path).path

        if path == "/health":
            self.send_json_response(200, {"status": "healthy", "timestamp": datetime.now().isoformat()})

        elif path == "/api/projects":
            self.send_json_response(200, list(self.projects.values()))

        elif path.startswith("/api/projects/"):
            project_id = path.split("/")[-1]
            if project_id in self.projects:
                self.send_json_response(200, self.projects[project_id])
            else:
                self.send_json_response(404, {"error": "Project not found"})

        elif path == "/api/agents":
            self.send_json_response(200, list(self.agents.values()))

        else:
            self.send_json_response(404, {"error": "Not found"})

    def do_POST(self):
        """Handle POST requests"""
        path = urllib.parse.urlparse(self.path).path
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0

        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}
        else:
            data = {}

        if path == "/api/projects":
            project_id = str(uuid.uuid4())
            project = {
                "id": project_id,
                "name": data.get("name", "unnamed-project"),
                "description": data.get("description", ""),
                "project_type": data.get("project_type", "unknown"),
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.projects[project_id] = project
            self.send_json_response(201, project)

        else:
            self.send_json_response(404, {"error": "Not found"})

    def do_PUT(self):
        """Handle PUT requests"""
        path = urllib.parse.urlparse(self.path).path
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0

        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}
        else:
            data = {}

        if path.startswith("/api/projects/"):
            project_id = path.split("/")[-1]
            if project_id in self.projects:
                project = self.projects[project_id]
                project.update(data)
                project["updated_at"] = datetime.now().isoformat()
                self.projects[project_id] = project
                self.send_json_response(200, project)
            else:
                # Create new project if it doesn't exist
                project = {
                    "id": project_id,
                    "name": data.get("name", "unnamed-project"),
                    "status": data.get("status", "pending"),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                project.update(data)
                self.projects[project_id] = project
                self.send_json_response(200, project)

        else:
            self.send_json_response(404, {"error": "Not found"})

    def send_json_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        if "GET /health" not in args[0]:
            super().log_message(format, *args)

if __name__ == "__main__":
    PORT = 8080

    # Pre-populate with test projects
    handler = MockAPIHandler
    handler.projects = {
        "5b19bd91-a75c-4a23-b482-c036b4277672": {
            "id": "5b19bd91-a75c-4a23-b482-c036b4277672",
            "name": "python-ml-pipeline",
            "description": "Machine learning data processing pipeline",
            "project_type": "python",
            "project_path": "/home/james/test-projects/ml-pipeline",
            "status": "running",
            "created_at": "2025-09-12T18:47:47.998011Z",
            "updated_at": datetime.now().isoformat()
        },
        "3a7b36df-3b9d-4807-886f-89432129ff2a": {
            "id": "3a7b36df-3b9d-4807-886f-89432129ff2a",
            "name": "node-ecommerce-app",
            "description": "A full-stack e-commerce application built with Node.js",
            "project_type": "nodejs",
            "project_path": "/home/james/test-projects/ecommerce-app",
            "status": "running",
            "created_at": "2025-09-12T18:47:43.861802Z",
            "updated_at": datetime.now().isoformat()
        }
    }

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🚀 Mock Hub API Server running at http://localhost:{PORT}")
        print("📊 Pre-loaded with 2 test projects")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 API Server stopped")
            httpd.shutdown()