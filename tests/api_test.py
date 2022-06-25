import unittest
import requests

server = "http://127.0.0.1:5000"

class TestApi(unittest.TestCase):
    def test_corrupted(self):
        files = {"file": open("tests/bad.docx", "rb")}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 400)

    def test_wrong_extension(self):
        files = {"file": open("tests/wrong.bin", "rb")}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 400)

    def test_single_file(self):
        files = {"file": open("tests/good0.docx", "rb")}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 200)

    def test_multiple_files(self):
        files = [("file", open("tests/good0.docx", "rb")), ("file", open("tests/good1.docx", "rb"))]
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 200)

