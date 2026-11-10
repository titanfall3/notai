import http.server, urllib.request

API_SECRET = "$MySecretKey99"  # Set your secret token here

class AuthProxy(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Reject immediately if missing the secret header
        if self.headers.get("X-API-Key") != API_SECRET:
            self.send_response(401)
            self.end_headers()
            return
        
        # Forward valid requests to Ollama
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else None
        req = urllib.request.Request(f"http://127.0.0.1:11434{self.path}", data=body, method="POST")
        for k, v in self.headers.items():
            if k.lower() not in ['host', 'content-length']:
                req.add_header(k, v)
        with urllib.request.urlopen(req) as resp:
            self.send_response(resp.status)
            for k, v in resp.headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(resp.read())

http.server.HTTPServer(('127.0.0.1', 11435), AuthProxy).serve_forever()
