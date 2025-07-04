import pandas as pd
import re
from fuzzywuzzy import process
from .config import EXCEL_PATH, KNOWN_TABLES

def is_table_heading(cell):
    if not isinstance(cell, str):
        return False
    cell_stripped = cell.strip()
    if cell_stripped.isupper() and re.search('[A-Z]', cell_stripped):
        return True
    match, score = process.extractOne(cell_stripped, KNOWN_TABLES)
    return score > 85

def row_contains_numeric(row):
    for cell in row:
        if cell == '':
            continue
        try:
            float(cell)
            return True
        except ValueError:
            continue
    return False

def is_alphabetic(text):
    return bool(re.search('[A-Za-z]', text))

def extract_tables_from_excel(file_path):
    df = pd.read_excel(file_path, header=None, dtype=str)
    df = df.fillna('')
    tables = {}

    for row_idx in range(2, df.shape[0]):
        row = df.iloc[row_idx]
        if row_contains_numeric(row):
            continue

        for col_idx, cell in row.items():
            if is_table_heading(cell):
                table_name = cell.strip()
                match, score = process.extractOne(table_name, KNOWN_TABLES)
                if score > 85:
                    table_name = match

                row_headings = []
                content_start = row_idx + 1
                while content_start < df.shape[0] and df.iat[content_start, col_idx].strip() == '':
                    content_start += 1

                while content_start < df.shape[0]:
                    heading_found = False
                    for left_col in range(col_idx, -1, -1):
                        cell_val = df.iat[content_start, left_col]
                        if cell_val.strip() != '' and is_alphabetic(cell_val):
                            row_headings.append((content_start, cell_val.strip()))
                            heading_found = True
                            break
                    if not heading_found:
                        break
                    content_start += 1

                if row_headings:
                    table_content = {}
                    table_width = 0

                    first_r_idx, _ = row_headings[0]
                    c_idx = col_idx + 1
                    while c_idx < df.shape[1] and df.iat[first_r_idx, c_idx].strip() == '':
                        c_idx += 1
                    last_data_col = c_idx
                    while last_data_col < df.shape[1] and df.iat[first_r_idx, last_data_col].strip() != '':
                        last_data_col += 1
                    last_data_col -= 1  # Adjust to last valid column

                    filtered_row_headings = []
                    for r_idx, heading in row_headings:
                        row_data = []
                        for data_col in range(col_idx + 1, last_data_col + 1):
                            val = df.iat[r_idx, data_col].strip()
                            if val != '':
                                try:
                                    float_val = float(val)
                                    if 0 < float_val < 1:
                                        val = f"{float_val * 100:.2f}%".rstrip('0').rstrip('.')
                                except ValueError:
                                    pass
                                row_data.append(val)
                        if len(row_data) > 0:
                            filtered_row_headings.append((r_idx, heading))
                            table_content[heading] = row_data
                            table_width = max(table_width, len(row_data))

                    # Only add the first occurrence of each table
                    if filtered_row_headings:
                        if table_name not in tables:
                            tables[table_name] = [{
                                "row_headings": [h for _, h in filtered_row_headings],
                                "content": table_content,
                                "start_row": row_idx,
                                "start_col": col_idx,
                                "width": table_width
                            }]
                        # else: do nothing (skip duplicates)

    return tables

# Load tables once at startup for performance
TABLES_CACHE = extract_tables_from_excel(EXCEL_PATH)

def get_table_matches(table_name: str):
    # Fuzzy match to support case-insensitive and partial matches
    matches = []
    for tname in TABLES_CACHE.keys():
        if table_name.lower() == tname.lower():
            matches.append(tname)
        elif process.extractOne(table_name, [tname])[1] > 85:
            matches.append(tname)
    return matches

TABLES_CACHE = extract_tables_from_excel(EXCEL_PATH)
