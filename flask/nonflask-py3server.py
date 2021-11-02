import http.server, socketserver, os

handler = http.server.SimpleHTTPRequestHandler
PORT = int(os.getenv("PORT", 8012))
print("starting server at port " + str(PORT))
with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

