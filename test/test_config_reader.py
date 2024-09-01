import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the directory containing config_reader.py to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Import the function or class you want to test
from config_reader import read_conf  # Adjust the import based on your module name

class TestYourFunction(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"port":443,"algo":0, "target_addr":"www.google.com","target_port":443}')
    def test_config_reader_function_success(self, mock_file):
        result = read_conf("config.json")
        self.assertEqual(result, {"port":443, "algo":0,  "target_addr":"www.google.com","target_port": 443})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_config_reader_file_not_found(self, mock_file):
        result = read_conf("config.json")
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data='Invalid JSON')
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "Invalid JSON", 0))
    def test_config_reader_invalid_json(self, mock_json_load, mock_file):
        result = read_conf("config.json")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()