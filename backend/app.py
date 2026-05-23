from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class ImageAPIServer(BaseHTTPRequestHandler):


    def handle_images(self):
        self.send_response(200)
        
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response_data = {"status": "success", "message": "Hello from Python!"}
        json_string = json.dumps(response_data)

        self.wfile.write(json_string.encode('utf-8'))
    
    def handle_image(self):
        ...


    def handle_upload(self):
        ...


    def do_GET(self):
        self.path = self.path.rstrip("/")

        if self.path == "/images":
            self.handle_images()
        elif "/images/" in self.path: # FIXME
            self.handle_image()
        

    def do_POST(self):
        if self.path == "/upload":
            self.handle_upload()
            
    
if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), ImageAPIServer)
    
    try:
        print("Сервер запущено...")
        server.serve_forever()
    except Exception as e:
        print(f"Трапилась помилка: {e}")