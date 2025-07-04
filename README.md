# FastAPI Excel Processor Assignment

## Overview

This application is built using **FastAPI** to process and extract structured data from a given Excel sheet with irregular layout formats. The goal is to demonstrate:

- API development using FastAPI
- Logical parsing of semi-structured Excel data
- Clean code organization and documentation

The application reads a financial Excel file located at `/data/capbudg.xls`, identifies multiple semantically distinct tables within it (e.g., *Initial Investment*, *Growth Rates*, *Cashflow Details*, etc.), and exposes RESTful endpoints to list tables, explore row headings, and compute numeric summaries.

---

## Project Structure
fastapi_excel_processor/
│
├── app/
│ ├── main.py # FastAPI app definition
│ ├── config.py # Constants and configuration
│ ├── parser.py # Table extraction and helper logic
│ ├── endpoints.py # API endpoint route definitions
│
├── data/
│ └── capbudg.xls # Input Excel file (provided)
│
├── postman/
│ └── ExcelProcessor.postman_collection.json # Postman collection for testing
│
├── requirements.txt # Python dependencies
├── run.sh # Startup script for the API
└── README.md # Documentation

---

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone https://github.com/AKP271003/fastapi_excel_processor
cd fastapi_excel_processor
```

### 2. Create a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate          # Linux/Mac

venv\Scripts\activate             # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Make sure xlrd is installed to support .xls file parsing.

### 4. Run the FastAPI Application
```bash
chmod +x run.sh         # Only for Linux/Mac
./run.sh

# OR

uvicorn app.main:app --host 0.0.0.0 --port 9090
```

### API Base URL

http://localhost:9090


### API Endpoints

#### 1. GET /list_tables
Description: Lists all detected table names in the Excel sheet.

Response Example:
```json
{
  "tables": [
    "Initial Investment",
    "Cashflow Details",
    "Discount Rate"
  ]
}
```

#### 2. GET /get_table_details
Query Parameters:

- table_name (str): Name of the table to fetch row headings for.

Description: Returns the row names from the specified table.

Example Request:
```
GET /get_table_details?table_name=Initial Investment
```

Response Example:
```json
{
  "table_name": "Initial Investment",
  "row_names": [
    "Initial Investment=",
    "Opportunity cost (if any)=",
    "Lifetime of the investment",
    "Salvage Value at end of project=",
    "Deprec. method(1:St.line;2:DDB)=",
    "Tax Credit (if any )=",
    "Other invest.(non-depreciable)="
  ]
}
```

#### 3. GET /row_sum
Query Parameters:

- table_name (str): Name of the table

- row_name (str): Row heading whose values you want to sum

Description: Computes and returns the sum of all numeric values found in the specified row.

Example Request:
```
GET /row_sum?table_name=Initial Investment&row_name=Tax Credit (if any )=
```

Response Example:
```json
{
  "table_name": "Initial Investment",
  "row_name": "Tax Credit (if any )=",
  "sum": 10
}
```
Note: Percent values like "5%" are interpreted as 5.0. Percent symbols are stripped before summing.

---

### Postman Collection
To test the API quickly:

1. Open Postman

2. Import → "Raw Text" → Paste contents from postman/ExcelProcessor.postman_collection.json

3. Hit send on endpoints:

    - /list_tables

    - /get_table_details?table_name=Initial Investment

    - /row_sum?table_name=Initial Investment&row_name=Tax Credit (if any )=

---

## Features and Design Choices
1. Fuzzy Matching: Handles minor typos in table or row names.

2. One-Time Parsing: Excel file is parsed once at app startup and cached for fast responses.

3. Smart Detection: Table headers are detected via ALL CAPS heuristic and fuzzy string matching.

4. Value Normalization: Converts 0.05 → 5% for clarity.

---

## Potential Improvements
1. Support for .xlsx and Google Sheets using openpyxl or gspread.

2. Dynamic file upload via multipart/form-data.

3. UI integration using React/Vue or Swagger Try-It console.

4. Use ML/NLP techniques to infer table boundaries beyond rule-based methods.

5. Authentication for sensitive financial data.

---

## Missed Edge Cases
- Empty Excel files (graceful error messaging not fully implemented)

- Tables with no numeric cells (e.g., purely textual data)

- Duplicate table headers are ignored silently

- Malformed cell contents (e.g., 'N/A', 'five') may affect summation

- Mixed-language (non-English) content is not supported for heading detection

---

## Testing
You can manually test using:

1. http://localhost:9090 (FastAPI Swagger UI)

2. Postman (see postman/ExcelProcessor.postman_collection.json)

---

Author
Aniket Kumar Pandey
