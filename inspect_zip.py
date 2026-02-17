
import zipfile
import os

filepath = "Delinquency_prediction_dataset.xlsx"

def inspect_zip():
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            print("Files in ZIP:")
            for name in z.namelist():
                print(name)
    except zipfile.BadZipFile:
        print("Error: Bad ZIP file.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if os.path.exists(filepath):
        inspect_zip()
