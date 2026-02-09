# Quick Start Guide

This guide will help you get the ESP List Processing application up and running quickly.

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Part 1: ESP Column Identification

This is the first completed part of the application that handles automatic ESP column detection.

### Backend Setup & Testing

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (if not already created)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run automated tests**
   ```bash
   python test_esp_detection.py
   ```

   This will run 7 comprehensive tests covering:
   - High confidence detection (single match)
   - Case-insensitive matching
   - Whitespace trimming
   - Low confidence (multiple matches)
   - No confidence (no matches)
   - All ESP column variants
   - Large datasets (1000+ rows)

5. **Start the backend server**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

6. **Test the API with sample files**
   
   Test with high confidence file (single ESP column):
   ```bash
   curl -X POST "http://localhost:8000/api/upload" \
     -F "file=@sample_data/test_high_confidence.csv"
   ```

   Expected response:
   ```json
   {
     "confidence": "high",
     "detected_column": "ESP",
     "candidates": ["ESP"],
     "preview_data": null,
     "total_rows": 5,
     "all_columns": ["Email", "ESP", "Name", "Company"],
     "filename": "test_high_confidence.csv"
   }
   ```

   Test with low confidence file (multiple ESP columns):
   ```bash
   curl -X POST "http://localhost:8000/api/upload" \
     -F "file=@sample_data/test_low_confidence.csv"
   ```

   Expected response includes preview_data for user selection:
   ```json
   {
     "confidence": "low",
     "detected_column": null,
     "candidates": ["ESP", "Provider"],
     "preview_data": [...],
     "total_rows": 3,
     ...
   }
   ```

### Frontend Setup

1. **Navigate to frontend directory** (open a new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   cp .env.local.example .env.local
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open the application**
   
   Navigate to [http://localhost:3000](http://localhost:3000) in your browser

### Using the Application

1. **Upload a file**
   - Drag and drop a CSV or XLSX file
   - Or click "Browse Files" to select a file

2. **Automatic ESP Detection**
   - If a single ESP column is found (high confidence):
     - The column is automatically detected
     - You'll see a success screen with the detected column
   
   - If multiple ESP columns are found (low confidence):
     - You'll see a preview of your data
     - Select the correct ESP column from the dropdown
   
   - If no ESP column matches are found (no confidence):
     - You'll see a preview of your data
     - Select the ESP column from all available columns

3. **View Results**
   - See the detected/selected ESP column
   - View file statistics (rows, columns)
   - Option to process another file

## ESP Column Detection Logic

The application detects ESP columns using these case-insensitive variants:
- `esp`
- `email service provider`
- `email provider`
- `provider`
- `mail provider`

### Confidence Levels

- **High Confidence**: Exactly one column matches → automatic selection
- **Low Confidence**: Multiple columns match → user must choose
- **No Confidence**: No columns match → user selects from all columns

## Testing with Your Own Files

You can test with your own CSV or XLSX files. The application will:
1. Parse your file (supports CSV and XLSX)
2. Normalize column headers (trim whitespace, case-insensitive)
3. Search for ESP column variants
4. Present results based on confidence level

## Sample Test Files

Three sample CSV files are provided in `backend/sample_data/`:

1. **test_high_confidence.csv** - Contains single "ESP" column (high confidence)
2. **test_low_confidence.csv** - Contains both "ESP" and "Provider" columns (low confidence)
3. **test_no_confidence.csv** - Contains "MailService" column (no confidence)

## API Documentation

### GET /
Health check endpoint

**Response:**
```json
{
  "message": "ESP List Processing API",
  "status": "running"
}
```

### POST /api/upload
Upload and analyze a CSV or XLSX file

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (CSV or XLSX)

**Response:**
```json
{
  "confidence": "high|low|none",
  "detected_column": "ESP" | null,
  "candidates": ["ESP", "Provider"],
  "preview_data": [...] | null,
  "total_rows": 1000,
  "all_columns": ["Email", "ESP", "Name"],
  "filename": "example.csv"
}
```

### POST /api/confirm-column
Confirm user's column selection (for future processing)

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: 
  - file (CSV or XLSX)
  - column_name (string)

**Response:**
```json
{
  "status": "success",
  "message": "ESP column 'ESP' confirmed",
  "column_name": "ESP"
}
```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Check what's using port 8000
lsof -i :8000
# Kill the process or use a different port
PORT=8001 python main.py
```

**Module not found errors:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Next.js will automatically try port 3001
# Or manually specify:
PORT=3001 npm run dev
```

**API connection errors:**
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local

## Next Steps

Part 1 (ESP Column Identification) is now complete! 

Future parts will include:
- Part 2: Filter rows containing Barracuda or Outlook
- Part 3: Split into files with max 49,000 rows each
- Part 4: Download as CSV or ZIP

## Support

For issues or questions, refer to:
- Main README: `/README.md`
- Building Plan: `/ESP_LIST_PROCESSING_BUILDING_PLAN.md`
- Backend README: `/backend/README.md`
- Frontend README: `/frontend/README.md`
