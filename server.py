import http.server
import socketserver
import configparser

def get_port():
    config = configparser.ConfigParser()
    try:
        config.read('capwin.ini')
        return int(config['Server']['server_port'])
    except:
        print("Couldn't get server_port from capwin.ini...")
        return 8000

Handler = http.server.SimpleHTTPRequestHandler

PORT = get_port()

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("Serving at localhost:" + str(PORT))
    httpd.serve_forever()