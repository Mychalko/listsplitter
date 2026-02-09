# ESP List Processing - Backend

FastAPI backend for ESP list processing application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /api/upload
Upload a CSV or XLSX file for ESP column detection.

**Response:**
- `confidence`: "high" | "low" | "none"
- `detected_column`: ESP column name (if confidence is high)
- `candidates`: List of possible ESP columns
- `preview_data`: Sample rows (if user input needed)
- `total_rows`: Total number of rows
- `all_columns`: All column names

### POST /api/confirm-column
Confirm the user's ESP column selection.

**Parameters:**
- `file`: The uploaded file
- `column_name`: The selected column name
