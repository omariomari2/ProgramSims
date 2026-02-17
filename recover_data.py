
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import os
import re

filepath = "Delinquency_prediction_dataset.xlsx"

def strip_namespace(tag):
    return re.sub(r'\{.*\}', '', tag)

def col_letter_to_index(col_letter):
    """Convert column letter (e.g., 'A', 'AA') to 0-based index."""
    col_letter = col_letter.upper()
    idx = 0
    for char in col_letter:
        idx = idx * 26 + (ord(char) - ord('A') + 1)
    return idx - 1

def parse_cell_ref(ref):
    """Parse 'A1' into (0, 0). Returns (row_idx, col_idx)."""
    match = re.match(r"([A-Z]+)([0-9]+)", ref)
    if match:
        col_str, row_str = match.groups()
        return int(row_str) - 1, col_letter_to_index(col_str)
    return None, None

def parse_shared_strings(z):
    try:
        with z.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            strings = []
            for elem in root.iter():
                if strip_namespace(elem.tag) == 't':
                    strings.append(elem.text)
            return strings
    except KeyError:
        return []
    except Exception as e:
        print(f"Error parsing shared strings: {e}")
        return []

def parse_sheet(z, shared_strings):
    data = {} # Map (row, col) -> value
    max_row = 0
    max_col = 0
    
    try:
        with z.open('xl/worksheets/sheet1.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            rows = []
            for elem in root.iter():
                if strip_namespace(elem.tag) == 'row':
                    rows.append(elem)
            
            for row in rows:
                cells = []
                for child in row:
                    if strip_namespace(child.tag) == 'c':
                        cells.append(child)
                
                for cell in cells:
                    r_attr = cell.get('r') # e.g. "A1"
                    if not r_attr:
                        continue
                        
                    row_idx, col_idx = parse_cell_ref(r_attr)
                    max_row = max(max_row, row_idx)
                    max_col = max(max_col, col_idx)
                    
                    val = None
                    t = cell.get('t')
                    
                    v_node = None
                    for child in cell:
                        if strip_namespace(child.tag) == 'v':
                            v_node = child
                            break
                    
                    if v_node is not None:
                        val = v_node.text
                        if t == 's':
                            try:
                                idx = int(val)
                                if idx < len(shared_strings):
                                    val = shared_strings[idx]
                            except ValueError:
                                pass
                        elif t != 'str':
                            try:
                                val = float(val)
                                if val.is_integer():
                                    val = int(val)
                            except ValueError:
                                pass
                    
                    data[(row_idx, col_idx)] = val

        # Construct list of lists
        # Determine columns from the first row (header) if possible, or just max_col
        # Usually header is row 0
        header_cols = []
        for c in range(max_col + 1):
            header_cols.append(data.get((0, c), f"Col_{c}"))
            
        final_data = []
        for r in range(1, max_row + 1):
            row_data = []
            for c in range(max_col + 1):
                row_data.append(data.get((r, c), None))
            final_data.append(row_data)
            
        return header_cols, final_data

    except Exception as e:
        # import traceback
        print(f"Error parsing sheet: {e}")
        return [], []

def recover_data():
    if not os.path.exists(filepath):
        print("File not found.")
        return

    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            shared_strings = parse_shared_strings(z)
            print(f"Found {len(shared_strings)} shared strings.")
            headers, rows = parse_sheet(z, shared_strings)
            
            if headers:
                df = pd.DataFrame(rows, columns=headers)
                print("Data recovered successfully.")
                print("Shape:", df.shape)
                print(df.head())
                df.to_csv("recovered_data.csv", index=False)
            else:
                print("No data extracted.")
    except Exception as e:
        print(f"Error during recovery: {e}")

if __name__ == "__main__":
    recover_data()
