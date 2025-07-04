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
```
# OR
```
uvicorn app.main:app --host 0.0.0.0 --port 9090
```
