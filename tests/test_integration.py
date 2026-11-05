import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import patch
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
            data = json.dumps({"version": 1, "matrix": [[2, 4], [3, 1]]})
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

    def check_invalid_matrix(self, matrix, raw=None, version=1, status=400):
        server = HTTPServer(("127.0.0.1", 0), MatrixHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        try:
            port = server.server_address[1]
            data = raw if raw is not None else json.dumps(
                {"version": version, "matrix": matrix})
            request = Request(
                f"http://127.0.0.1:{port}/compare",
                data=data.encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with self.assertRaises(HTTPError) as error:
                urlopen(request, timeout=5)

            self.assertEqual(error.exception.code, status)
            error.exception.close()
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_empty_matrix(self):
        self.check_invalid_matrix([])

    def test_non_square_matrix(self):
        self.check_invalid_matrix([[2, 4]])

    def test_non_numeric_element(self):
        self.check_invalid_matrix([["a"]])

    def test_invalid_matrix_type(self):
        self.check_invalid_matrix(None)

    def test_malformed_json(self):
        self.check_invalid_matrix(None, raw="{invalid")

    def test_unsupported_version(self):
        self.check_invalid_matrix([[1]], version=2, status=409)

    def test_calculation_module_failure(self):
        with patch("server.calculate_diagonals", side_effect=RuntimeError):
            with patch("server.logging.exception"):
                self.check_invalid_matrix([[1]], status=503)

    def test_missing_calculation_module(self):
        with patch("server.calculate_diagonals", None):
            self.check_invalid_matrix([[1]], status=503)

    def test_server_import_when_matrix_file_missing(self):
        source = Path(__file__).resolve().parents[1] / "src" / "server.py"
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "server.py"
            shutil.copyfile(source, target)
            script = (
                "import runpy, sys; "
                "module = runpy.run_path(sys.argv[1]); "
                "assert module['calculate_diagonals'] is None"
            )
            result = subprocess.run(
                [sys.executable, "-I", "-c", script, str(target)],
                capture_output=True, text=True, timeout=10
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
