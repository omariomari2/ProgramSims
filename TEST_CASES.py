import unittest
import os
import json
import csv
from unittest.mock import patch
from process_data import DataProcessor

class TestProcessData(unittest.TestCase):
    def setUp(self):
        self.customers_file = "test_customers.csv"
        self.transactions_file = "test_transactions.csv"
        self.output_csv = "test_output.csv"
        self.output_json = "test_output.json"


        with open(self.customers_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["customer_id", "name", "email", "join_date"])
            writer.writeheader()
            writer.writerow({"customer_id": "C001", "name": "Alice", "email": "alice@example.com", "join_date": "2023-01-01"})
            writer.writerow({"customer_id": "C002", "name": "Bob", "email": "bob@example.com", "join_date": "2023-01-02"})

    def tearDown(self):
        for f in [self.customers_file, self.transactions_file, self.output_csv, self.output_json]:
            if os.path.exists(f):
                os.remove(f)

    def test_export_customer_data_json_success(self):
        """Test that JSON export works with valid data."""
        processor = DataProcessor(self.customers_file)
        processor.load_data()
        success = processor.export_customer_data(self.output_json, "json")
        self.assertTrue(success, "JSON Export should succeed")
        

        with open(self.output_json, "r") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertIn("C001", data)

    def test_export_customer_data_json_failure_handled(self):
        """Test that export_customer_data handles unexpected errors gracefully."""
        processor = DataProcessor(self.customers_file)
        processor.load_data()
        

        with patch("json.dump", side_effect=AttributeError("'dict' object has no attribute 'keys'")):
             success = processor.export_customer_data(self.output_json, "json")
             self.assertFalse(success, "Should return False (handled) when exception occurs")

    def test_export_customer_data_csv_success(self):
        """Test CSV export robustness."""
        processor = DataProcessor(self.customers_file)
        processor.load_data()
        success = processor.export_customer_data(self.output_csv, "csv")
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
