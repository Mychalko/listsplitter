from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Any
import pandas as pd
import io
import os
from dataclasses import dataclass
from enum import Enum

app = FastAPI(title="ESP List Processing API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DetectionConfidence(str, Enum):
    HIGH = "high"
    LOW = "low"
    NONE = "none"


@dataclass
class ESPColumnDetectionResult:
    confidence: DetectionConfidence
    detected_column: Optional[str]
    candidates: List[str]
    preview_data: Optional[List[Dict[str, Any]]]
    total_rows: int
    all_columns: List[str]


# ESP column detection variants (normalized to lowercase)
ESP_COLUMN_VARIANTS = [
    "esp",
    "email service provider",
    "email provider",
    "provider",
    "mail provider",
]


def normalize_header(header: str) -> str:
    """Normalize header for matching: lowercase and trim whitespace."""
    return str(header).strip().lower()


def detect_esp_column(df: pd.DataFrame) -> ESPColumnDetectionResult:
    """
    Detect the ESP column in the dataframe using header name matching.
    
    Returns:
        ESPColumnDetectionResult with confidence level and detected column info
    """
    # Normalize all column headers
    columns = df.columns.tolist()
    normalized_columns = {col: normalize_header(col) for col in columns}
    
    # Find matches for ESP variants
    candidates = []
    for original_col, normalized_col in normalized_columns.items():
        if normalized_col in ESP_COLUMN_VARIANTS:
            candidates.append(original_col)
    
    # Determine confidence and result
    total_rows = len(df)
    preview_rows = min(50, total_rows)
    
    if len(candidates) == 1:
        # Single match - high confidence
        return ESPColumnDetectionResult(
            confidence=DetectionConfidence.HIGH,
            detected_column=candidates[0],
            candidates=candidates,
            preview_data=None,  # No need for preview with high confidence
            total_rows=total_rows,
            all_columns=columns,
        )
    elif len(candidates) > 1:
        # Multiple matches - low confidence, need user input
        preview_df = df.head(preview_rows)
        preview_data = preview_df.to_dict(orient="records")
        
        return ESPColumnDetectionResult(
            confidence=DetectionConfidence.LOW,
            detected_column=None,
            candidates=candidates,
            preview_data=preview_data,
            total_rows=total_rows,
            all_columns=columns,
        )
    else:
        # No matches - need user to select from all columns
        preview_df = df.head(preview_rows)
        preview_data = preview_df.to_dict(orient="records")
        
        return ESPColumnDetectionResult(
            confidence=DetectionConfidence.NONE,
            detected_column=None,
            candidates=columns,  # All columns are candidates
            preview_data=preview_data,
            total_rows=total_rows,
            all_columns=columns,
        )


def read_file_to_dataframe(file_content: bytes, filename: str) -> pd.DataFrame:
    """
    Read uploaded file content into a pandas DataFrame.
    Supports CSV and XLSX formats.
    """
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension == ".csv":
        # Try different encodings
        try:
            df = pd.read_csv(io.BytesIO(file_content))
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(file_content), encoding="latin-1")
    elif file_extension in [".xlsx", ".xls"]:
        # Read first sheet by default
        df = pd.read_excel(io.BytesIO(file_content), engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    return df


@app.get("/")
async def root():
    return {"message": "ESP List Processing API", "status": "running"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV or XLSX file and detect the ESP column.
    
    Returns:
        - confidence: high/low/none
        - detected_column: the ESP column name if confidence is high
        - candidates: list of possible ESP columns
        - preview_data: sample rows if user input needed
        - total_rows: total number of rows in the file
        - all_columns: list of all column names
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".csv", ".xlsx", ".xls"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Please upload CSV or XLSX files."
            )
        
        # Read file content
        content = await file.read()
        
        # Parse file into DataFrame
        df = read_file_to_dataframe(content, file.filename)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Detect ESP column
        detection_result = detect_esp_column(df)
        
        # Prepare response
        response = {
            "confidence": detection_result.confidence.value,
            "detected_column": detection_result.detected_column,
            "candidates": detection_result.candidates,
            "preview_data": detection_result.preview_data,
            "total_rows": detection_result.total_rows,
            "all_columns": detection_result.all_columns,
            "filename": file.filename,
        }
        
        return JSONResponse(content=response)
    
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty or invalid")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}"
        )


@app.post("/api/confirm-column")
async def confirm_column(
    file: UploadFile = File(...),
    column_name: str = None,
):
    """
    Confirm the ESP column selection by the user.
    This endpoint will be used when confidence is not high.
    
    For now, it just validates the column exists.
    Later, this will be used to proceed with the filtering and splitting.
    """
    try:
        if not column_name:
            raise HTTPException(status_code=400, detail="Column name is required")
        
        # Read file content
        content = await file.read()
        df = read_file_to_dataframe(content, file.filename)
        
        # Validate column exists
        if column_name not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{column_name}' not found in the file"
            )
        
        return JSONResponse(content={
            "status": "success",
            "message": f"ESP column '{column_name}' confirmed",
            "column_name": column_name,
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
