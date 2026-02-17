
import zipfile
import os

filepath = "Delinquency_prediction_dataset.xlsx"

def extract_sheet_xml():
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            with z.open('xl/worksheets/sheet1.xml') as f:
                content = f.read(1000).decode('utf-8')
                print(content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if os.path.exists(filepath):
        extract_sheet_xml()
