from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_request_info()
        self.respond()

    def do_POST(self):
        self.log_request_info()
        self.respond()

    def do_PUT(self):
        self.log_request_info()
        self.respond()

    def do_DELETE(self):
        self.log_request_info()
        self.respond()

    def log_request_info(self):
        print("=== New Request ===")
        print(f"Client IP: {self.client_address[0]}")
        print(f"Method: {self.command}")
        print(f"Path: {self.path}")
        print("Headers:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")

        if 'Content-Length' in self.headers:
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode('utf-8', errors='ignore')
            print("Body:")
            print(body)

    def respond(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Request received\n")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[*] Starting test server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
