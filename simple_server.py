from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        path = self.path
        protocol = "HTTP" # Simple server only supports HTTP
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>HTTP Test</title>
        </head>
        <body>
            <h1>Simple HTTP Server Test</h1>
            <p>Path requested: {path}</p>
            <p>Protocol: {protocol}</p>
            <p>This page is served by a simple HTTP server, not Django.</p>
            <p>If you're seeing this page, it means your browser can connect via HTTP.</p>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running at http://127.0.0.1:8080/")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 