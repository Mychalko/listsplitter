# ESP List Processing Application

A web application for processing and filtering ESP (Email Service Provider) lists. This application allows users to upload CSV or XLSX files, automatically identify ESP columns, filter out specific providers (Barracuda and Outlook), and split large lists into manageable chunks.

## Project Structure

```
esp-list-processing/
├── backend/          # FastAPI Python backend
│   ├── main.py      # Main API endpoints
│   ├── requirements.txt
│   └── README.md
├── frontend/         # Next.js TypeScript frontend
│   ├── src/
│   │   ├── app/     # Next.js app directory
│   │   └── components/  # React components
│   ├── package.json
│   └── README.md
└── README.md        # This file
```

## Features Implemented

### Part 1: ESP Column Identification ✓

- **Automatic ESP Column Detection**: Intelligently detects ESP columns using common naming variants:
  - esp
  - email service provider
  - email provider
  - provider
  - mail provider

- **Smart Confidence System**:
  - **High Confidence**: Single match found → automatic selection
  - **Low Confidence**: Multiple matches found → user selection required
  - **No Confidence**: No matches found → user selects from all columns

- **User-Friendly Interface**:
  - Drag-and-drop file upload
  - File type validation (CSV, XLSX)
  - Data preview for column selection
  - Clean, modern UI with Tailwind CSS

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.local.example .env.local
```

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Endpoints

### POST /api/upload
Upload a CSV or XLSX file for ESP column detection.

**Response:**
```json
{
  "confidence": "high|low|none",
  "detected_column": "ESP",
  "candidates": ["ESP", "Provider"],
  "preview_data": [...],
  "total_rows": 1000,
  "all_columns": ["Email", "ESP", "Name"],
  "filename": "example.csv"
}
```

### POST /api/confirm-column
Confirm the user's ESP column selection (for future use in processing).

## Architecture

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **Data Processing**: Pandas for CSV/XLSX handling
- **File Support**: CSV and XLSX (via openpyxl)

## Roadmap

- ✅ Part 1: ESP Column Identification
- ⏳ Part 2: Filter rows containing Barracuda or Outlook
- ⏳ Part 3: Split into files with max 49,000 rows each
- ⏳ Part 4: Download as CSV (or ZIP for multiple files)

## Contributing

This project is built according to the specifications in `ESP_LIST_PROCESSING_BUILDING_PLAN.md`.

## License

Proprietary
