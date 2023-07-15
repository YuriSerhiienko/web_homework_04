from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import datetime
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html" 
        try:
            with open('.' + self.path, 'rb') as file:
                self.send_response(200)
                if self.path.endswith(".html"):
                    self.send_header('Content-type', 'text/html')
                elif self.path.endswith(".css"):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith(".png"):
                    self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == "/message.html":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data_dict = {
                "timestamp": str(datetime.datetime.now()),
                "message": post_data.decode("utf-8")
            }
            with open('storage/data.json', 'a') as file:
                file.write(json.dumps(data_dict) + '\n')

            self.send_response(302) 
            self.send_header('Location', '/')
            self.end_headers()


def start_http_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting HTTP server on port 3000...')
    httpd.serve_forever()


def start_socket_server():
    class SocketHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0].decode("utf-8")
            data_dict = {
                "timestamp": str(datetime.datetime.now()),
                "message": data
            }
            with open('storage/data.json', 'a') as file:
                file.write(json.dumps(data_dict) + '\n')

            response = "Message received!"
            self.request[1].sendto(response.encode("utf-8"), self.client_address)

    socket_server = socketserver.UDPServer(('localhost', 5000), SocketHandler)
    print('Starting Socket server on port 5000...')
    socket_thread = threading.Thread(target=socket_server.serve_forever)
    socket_thread.start()


if __name__ == '__main__':
    http_thread = threading.Thread(target=start_http_server)
    http_thread.start()
    start_socket_server()
