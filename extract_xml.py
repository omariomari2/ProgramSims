
import zipfile
import os

filepath = "Delinquency_prediction_dataset.xlsx"

def extract_xml():
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            with z.open('xl/workbook.xml') as f:
                print(f.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if os.path.exists(filepath):
        extract_xml()
