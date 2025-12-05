from api.predict import handler
from http.server import HTTPServer

if __name__ == '__main__':
    port = 5328
    print(f"Starting local API server on http://127.0.0.1:{port}")
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Server stopped.")
