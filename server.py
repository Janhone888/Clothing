from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
import time


class ClothingHandler(BaseHTTPRequestHandler):
    # 内存数据库 (barcode -> clothing_data)
    clothing_db = {}

    def log_message(self, format, *args):
        """重写日志输出格式"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {self.address_string()} - {format % args}")

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.log_message("GET %s", self.path)
        parsed_path = urlparse.urlparse(self.path)

        # 处理根路径
        if parsed_path.path == '/':
            self._set_headers(200)
            response = {
                "status": "success",
                "message": "Clothing Inventory API is running",
                "endpoints": {
                    "GET /clothing": "List all clothing items",
                    "GET /clothing/{barcode}": "Get clothing details",
                    "POST /clothing": "Add a new clothing item",
                    "DELETE /clothing/{barcode}": "Remove a clothing item"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # 处理 /clothing 路径
        if parsed_path.path == '/clothing':
            self._set_headers(200)
            response = {
                "status": "success",
                "count": len(self.clothing_db),
                "items": list(self.clothing_db.keys())
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # 处理 /clothing/{barcode} 路径
        if parsed_path.path.startswith('/clothing/'):
            barcode = parsed_path.path.split('/')[2]

            if barcode in self.clothing_db:
                self._set_headers(200)
                response = {
                    "status": "success",
                    "item": self.clothing_db[barcode]
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self._set_headers(404)
                response = {
                    "status": "error",
                    "code": "ITEM_NOT_FOUND",
                    "message": f"Clothing item with barcode {barcode} does not exist"
                }
                self.wfile.write(json.dumps(response).encode())
            return

        # 处理未知路径
        self._set_headers(404)
        response = {
            "status": "error",
            "code": "ENDPOINT_NOT_FOUND",
            "message": "The requested endpoint does not exist"
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self.log_message("POST %s", self.path)

        # 检查路径
        if self.path != '/clothing':
            self._set_headers(404)
            response = {
                "status": "error",
                "code": "ENDPOINT_NOT_FOUND",
                "message": "The requested endpoint does not exist"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode())
        except json.JSONDecodeError:
            self._set_headers(400)
            response = {
                "status": "error",
                "code": "INVALID_JSON",
                "message": "Invalid JSON data"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # 验证必需字段
        required_fields = ['barcode', 'category', 'size', 'color']
        for field in required_fields:
            if field not in data:
                self._set_headers(400)
                response = {
                    "status": "error",
                    "code": "MISSING_FIELD",
                    "message": f"Missing required field: {field}"
                }
                self.wfile.write(json.dumps(response).encode())
                return

        barcode = data['barcode']

        # 检查是否已存在
        if barcode in self.clothing_db:
            self._set_headers(409)
            response = {
                "status": "error",
                "code": "ITEM_EXISTS",
                "message": f"Clothing item with barcode {barcode} already exists"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # 存储服装信息
        self.clothing_db[barcode] = {
            "category": data["category"],
            "size": data["size"],
            "color": data["color"]
        }
        self.log_message("Added clothing item: %s", barcode)

        self._set_headers(201)
        response = {
            "status": "success",
            "message": "Clothing item added successfully",
            "barcode": barcode
        }
        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        self.log_message("DELETE %s", self.path)
        parsed_path = urlparse.urlparse(self.path)

        if parsed_path.path.startswith('/clothing/'):
            barcode = parsed_path.path.split('/')[2]

            if barcode in self.clothing_db:
                del self.clothing_db[barcode]
                self.log_message("Removed clothing item: %s", barcode)
                self._set_headers(200)
                response = {
                    "status": "success",
                    "message": "Clothing item removed successfully"
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self._set_headers(404)
                response = {
                    "status": "error",
                    "code": "ITEM_NOT_FOUND",
                    "message": f"Clothing item with barcode {barcode} does not exist"
                }
                self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            response = {
                "status": "error",
                "code": "ENDPOINT_NOT_FOUND",
                "message": "The requested endpoint does not exist"
            }
            self.wfile.write(json.dumps(response).encode())


def run(server_class=HTTPServer, handler_class=ClothingHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting Clothing Inventory Server on port {port}...')
    print('Press Ctrl+C to stop the server')
    print('Open another terminal and run: python client.py')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.shutdown()


if __name__ == '__main__':
    run()