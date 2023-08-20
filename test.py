import unittest
import socket
import datetime
import os
import xml.etree.ElementTree as ET
import time

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = 'echo-server'
        cls.port = 7070

        cls.results = []

    @classmethod
    def tearDownClass(cls):
        cls.save_results_to_xml()

    def test_server_echo(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        try:
            messages = ["Hello", "World", "Test", ".quit"]
            expected_responses = ["ECHO: Hello (Counter: 0)", "ECHO: World (Counter: 1)", "ECHO: Test (Counter: 2)"]
            for msg, expected_response in zip(messages, expected_responses):
                client_socket.send(msg.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                self.assertEqual(response, expected_response)

        finally:
            client_socket.close()

    @classmethod
    def save_results_to_xml(cls):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"test_log/server_test_{timestamp}.xml"

        root = ET.Element("test_results")

        for result in cls.results:
            test_case = ET.SubElement(root, "test_case")
            test_case.set("name", result['name'])

            result_element = ET.SubElement(test_case, "result")
            result_element.text = result['result']

            if 'error' in result:
                error = ET.SubElement(test_case, "error")
                error.text = result['error']

        tree = ET.ElementTree(root)
        tree.write(file_name, encoding="utf-8")

    def record_result(self, name, result, error=None):
        self.results.append({'name': name, 'result': result, 'error': error})

if __name__ == "__main__":
    unittest.main()
