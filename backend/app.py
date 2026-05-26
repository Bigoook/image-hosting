from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from utils.encoders import AppJSONEncoder
from logger import logger
from database import ImageRepository



class ImageAPIServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.repo = ImageRepository()
        self.add_images()
        
    def add_images(self):
        if self.repo.list():
            logger.info("Images already exist in the database, skipping seeding")
            return  
        
        images = [
            {
                "filename": "image1.jpg",
                "original_name": "photo1.jpg",
                "size": 1024,
                "file_type": "image/jpeg"
            },
            {
                "filename": "image2.png",
                "original_name": "photo2.png",
                "size": 2048,
                "file_type": "image/png"
            },
            {
                "filename": "image3.png",
                "original_name": "photo3.png",
                "size": 150,
                "file_type": "image/png"
            },
            {
                "filename": "image3.png",
                "original_name": "photo3.png",
                "size": 200,
                "file_type": "image/jpeg"
            },
        ]
        
        for image in images:
            image_id = self.repo.create(
                filename=image["filename"],
                original_name=image["original_name"],
                size=image["size"],
                file_type=image["file_type"]
            )
            logger.info(f"Added image with ID {image_id} to the database")


    def handle_images(self): # /api/images
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        images = self.repo.list()
        
        self.wfile.write(json.dumps(images, cls=AppJSONEncoder).encode('utf-8'))

        self.rfile.read()

    def handle_upload(self):
        ...
        
        
    def delete_image(self):
        ...


    def do_GET(self):
        logger.info(f"Received GET request for {self.path}")
        self.path = self.path.rstrip("/")

        if self.path == "/images":
            self.handle_images()
        

    def do_POST(self):
        logger.info(f"Received POST request for {self.path}")
        
        if self.path == "/upload":
            self.handle_upload()
            
    
    def do_DELETE(self):
        logger.info(f"Received DELETE request for {self.path}")
        if self.path.startswith("/images/"):
            self.delete_image()
            
    
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), ImageAPIServer)
    
    try:
        print("Сервер запущено...")
        server.serve_forever()
    except Exception as e:
        print(f"Трапилась помилка: {e}")