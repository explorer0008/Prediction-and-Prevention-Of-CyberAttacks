#!/usr/bin/env python3
"""
Minimal HTTP server to serve the frontend files locally.
Run from the Dataset directory: python server.py
Then open http://localhost:8000/index.html in your browser.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

# Change to the script's directory so relative paths work
os.chdir(Path(__file__).parent)

print(f"Starting HTTP server on http://localhost:{PORT}")
print(f"Serving files from: {os.getcwd()}")
print("Press Ctrl+C to stop the server.\n")
print(f"Open http://localhost:{PORT}/index.html in your browser.")

with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
