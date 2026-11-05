from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from matrix import calculate_diagonals


class MatrixHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Server works")

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        data = json.loads(body)

        matrix = data["matrix"]
        if len(matrix) == 0:
            self.send_error(400, "Matrix must not be empty")
            return

        for row in matrix:
            if len(row) != len(matrix):
                self.send_error(400, "Matrix must be square")
                return

        main_sum, side_sum = calculate_diagonals(matrix)

        result = {
            "main_sum": main_sum,
            "side_sum": side_sum
        }
        response = json.dumps(result).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), MatrixHandler)
    print("Сервер запущен")
    server.serve_forever()
