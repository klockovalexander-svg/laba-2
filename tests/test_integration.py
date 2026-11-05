import json
import sys
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from server import MatrixHandler  # noqa: E402


class TestIntegration(unittest.TestCase):
    def test_server_calculates_diagonals(self):
        server = HTTPServer(("127.0.0.1", 0), MatrixHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        try:
            port = server.server_address[1]
            data = json.dumps({"matrix": [[2, 4], [3, 1]]})
            request = Request(
                f"http://127.0.0.1:{port}/compare",
                data=data.encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urlopen(request, timeout=5) as response:
                result = json.loads(response.read())

            self.assertEqual(result["main_sum"], 3)
            self.assertEqual(result["side_sum"], 7)
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def check_invalid_matrix(self, matrix):
        server = HTTPServer(("127.0.0.1", 0), MatrixHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        try:
            port = server.server_address[1]
            data = json.dumps({"matrix": matrix})
            request = Request(
                f"http://127.0.0.1:{port}/compare",
                data=data.encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with self.assertRaises(HTTPError) as error:
                urlopen(request, timeout=5)

            self.assertEqual(error.exception.code, 400)
            error.exception.close()
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_empty_matrix(self):
        self.check_invalid_matrix([])

    def test_non_square_matrix(self):
        self.check_invalid_matrix([[2, 4]])


if __name__ == "__main__":
    unittest.main()
