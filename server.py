import http.server
import socketserver
Handler = http.server.SimpleHTTPRequestHandler

PORT = 8000

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("Serving at localhost:" + str(PORT))
    httpd.serve_forever()