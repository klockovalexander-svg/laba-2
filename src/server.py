from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import math

try:
    from matrix import calculate_diagonals
except ModuleNotFoundError as error:
    if error.name != "matrix":
        raise
    calculate_diagonals = None
    logging.error("Calculation module is missing")


class MatrixHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Server works")

    def do_POST(self):
        try:
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)
            matrix = data["matrix"]
        except (TypeError, ValueError, KeyError, UnicodeDecodeError):
            self.send_error(400, "Invalid JSON or missing matrix")
            return

        if type(data.get("version")) is not int or data["version"] != 1:
            self.send_error(409, "Unsupported request version")
            return

        if not isinstance(matrix, list):
            self.send_error(400, "Matrix must be an array")
            return
        if len(matrix) == 0:
            self.send_error(400, "Matrix must not be empty")
            return

        for row in matrix:
            if not isinstance(row, list) or len(row) != len(matrix):
                self.send_error(400, "Matrix must be square")
                return
            for value in row:
                try:
                    valid = (type(value) in (int, float) and
                             math.isfinite(value))
                except OverflowError:
                    valid = False
                if not valid:
                    self.send_error(400, "Matrix elements must be numbers")
                    return

        if calculate_diagonals is None:
            self.send_error(503, "Calculation module unavailable")
            return

        try:
            main_sum, side_sum = calculate_diagonals(matrix)
        except Exception:
            logging.exception("Calculation module failed")
            self.send_error(503, "Calculation module unavailable")
            return

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
