import unittest
import requests
import os
import time
import subprocess


server = "http://127.0.0.1:5000"


class TestApi(unittest.TestCase):
    def test_corrupted(self):
        tmp = open("tests/bad.docx", "rb")
        files = {"file": tmp}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 400)
        tmp.close()

    def test_wrong_extension(self):
        tmp = open("tests/wrong.bin", "rb")
        files = {"file": tmp}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 400)
        tmp.close()

    def test_single_file(self):
        tmp = open("tests/good0.docx", "rb")
        files = {"file": tmp}
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 200)
        tmp.close()

    def test_multiple_files(self):
        tmp1 = open("tests/good0.docx", "rb")
        tmp2 = open("tests/good1.docx", "rb")
        files = [("file", tmp1), ("file", tmp2)]
        response = requests.post(server + "/convert", files=files)
        self.assertEqual(response.status_code, 200)
        tmp1.close()
        tmp2.close()


def setUpModule():
    subprocess.Popen(["./start_server", ">", "/dev/null", "2&>1"])
    # check if something is listening on port 5000
    while os.system("sudo lsof -i:5000") >> 8 != 0:
        time.sleep(1)
    print("Ready to run tests")
    time.sleep(3)
