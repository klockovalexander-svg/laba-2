import io
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError


class TestClientTimeout(unittest.TestCase):
    def check_timeout(self, error):
        output = io.StringIO()
        path = Path(__file__).resolve().parents[1] / "src" / "main.py"
        with patch("builtins.input", side_effect=["1", "5"]):
            with patch("urllib.request.urlopen", side_effect=error) as urlopen:
                with redirect_stdout(output):
                    with self.assertRaises(SystemExit):
                        runpy.run_path(str(path), run_name="__main__")
        self.assertIn("сервер не ответил за 5 секунд", output.getvalue())
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 5)

    def test_timeout(self):
        self.check_timeout(TimeoutError())

    def test_wrapped_timeout(self):
        self.check_timeout(URLError(TimeoutError()))

    def test_version_conflict(self):
        output = io.StringIO()
        path = Path(__file__).resolve().parents[1] / "src" / "main.py"
        error = HTTPError("http://localhost", 409, "Conflict", {}, None)
        with patch("builtins.input", side_effect=["1", "5"]):
            with patch("urllib.request.urlopen", side_effect=error):
                with redirect_stdout(output):
                    with self.assertRaises(SystemExit):
                        runpy.run_path(str(path), run_name="__main__")
        self.assertIn("версия клиента не поддерживается", output.getvalue())

    def test_successful_response(self):
        output = io.StringIO()
        path = Path(__file__).resolve().parents[1] / "src" / "main.py"
        response = io.BytesIO(b'{"main_sum": 5, "side_sum": 5}')
        with patch("builtins.input", side_effect=["1", "5"]):
            with patch("urllib.request.urlopen", return_value=response):
                with redirect_stdout(output):
                    runpy.run_path(str(path), run_name="__main__")
        self.assertIn("Диагонали равны", output.getvalue())
        self.assertIn("Введённая матрица:\n5.000", output.getvalue())
        self.assertIn("Сумма главной диагонали: 5", output.getvalue())
        self.assertIn("Сумма побочной диагонали: 5", output.getvalue())


if __name__ == "__main__":
    unittest.main()
