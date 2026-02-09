# ESP List Processing App — Building Plan

## Summary

Build a web app that allows a user to upload a `.csv` or `.xlsx` file, then:

- **Deletes rows** whose Email Service Provider (ESP) contains **Barracuda** or **Outlook**
- **Splits** the remaining rows into multiple output files, with **a maximum of 49,000 rows per file**
- Provides the **final downloadable output(s) in CSV format** (even if the input was XLSX)

## Requirements (MVP)

### Inputs
- Supported uploads: **CSV**, **XLSX**
- XLSX support:
  - Default to the **first sheet**
  - If multiple sheets exist, optionally let the user pick a sheet (Milestone 2 if needed)

### Processing rules

#### 1) Identify the ESP column
Every uploaded list contains an Email Service Provider field (ESP) “or any variation of that”.

Implement ESP column selection as:
- **Auto-detect by header name** (case-insensitive, trimmed), using these common variants:
  - `esp`
  - `email service provider`
  - `email provider`
  - `provider`
  - `mail provider`
- If multiple candidates are found or no confident match:
  - Show a small **preview** (first ~50 rows)
  - Ask the user to **choose the ESP column**

#### 2) Delete rows containing Barracuda or Outlook
Remove a row if the ESP cell (normalized) contains either of these values:
- `Barracuda`
- `Outlook`

Normalization for matching:
- Trim leading/trailing whitespace
- Case-insensitive comparison
- Use **substring “contains”** matching (recommended) so values like `Microsoft Outlook` are removed.

Example match logic:
- Remove if `lower(esp_value)` contains `barracuda` OR `outlook`

#### 3) Split into smaller lists (max 49,000 rows)
After filtering:
- Split the remaining dataset into multiple files.
- **Maximum rows per output file**: **49,000 data rows** (header not counted).
- Preserve:
  - Same columns and their order
  - Same cell values for all kept rows

### Outputs
- Output file format: **CSV only**
  - If input is XLSX, convert output to CSV.
- Naming convention (example):
  - `output_part001.csv`
  - `output_part002.csv`
  - ...
- Download packaging:
  - If multiple parts, return a **single ZIP** containing all CSV parts
  - If only one part, allow direct download of that CSV (optionally still offer ZIP)
- Include a lightweight **processing report** (optional but recommended), e.g. `report.json`:
  - Original row count
  - Rows removed (Barracuda)
  - Rows removed (Outlook)
  - Rows kept
  - Number of output parts
  - Chosen ESP column name

## UX / Screens
- **Upload screen**: drag & drop, browse, file type validation
- **Column selection step**: only if ESP column is ambiguous
- **Processing screen**: progress indicator (upload → cleaning → splitting → packaging)
- **Results screen**: summary + download button(s)

## Architecture (recommended)

### Option A: Simple synchronous API (fastest MVP)
- Frontend: Next.js (or any SPA)
- Backend: FastAPI (Python) or Node/Express
- Run processing on the request thread for small/medium files

### Option B: Job queue for large lists (recommended for 200k+ rows)
- API:
  - Accept upload
  - Create a job record
  - Return a job id
- Worker:
  - Processes file asynchronously
  - Writes output CSV parts and ZIP
- UI:
  - Poll job status / receive websocket updates
  - Provide download link(s) when complete

## Implementation notes

### Performance
- Use **streaming parsing** to avoid loading the entire file into memory:
  - CSV: stream reader → stream writer
  - XLSX: streaming worksheet reader if available; otherwise enforce a file size cap for MVP
- Filtering + splitting can be done in a single pass:
  - For each row:
    - Evaluate ESP value
    - If kept, write to current output part
    - Rotate to the next part when part row count reaches 49,000

### Data correctness
- Preserve column order and headers exactly (except optional whitespace normalization of header matching for ESP detection).
- Ensure CSV output:
  - Proper escaping/quoting for commas, quotes, newlines
  - UTF-8 encoding

### Security & privacy
- TLS/HTTPS in production
- Don’t log uploaded data or row contents
- Auto-delete uploads and generated outputs after a retention period (e.g., 1–24 hours)

## Testing plan
- Unit tests:
  - ESP column detection across header variants
  - Barracuda/Outlook filtering (case, whitespace, substring)
  - Splitting boundaries (0 rows, 1 row, 49,000 rows, 49,001 rows, 200,000 rows)
- Integration tests:
  - End-to-end CSV upload → ZIP download with correct parts and counts
  - End-to-end XLSX upload → CSV outputs

## Milestones
- **Milestone 1 (MVP)**:
  - Upload CSV/XLSX
  - ESP column auto-detect + fallback selection
  - Filter Barracuda/Outlook
  - Split to <=49,000 rows/part
  - Download CSV (ZIP if multiple)
- **Milestone 2**:
  - Multi-sheet XLSX selection
  - Better progress reporting and job status page
- **Milestone 3**:
  - Background worker, object storage (S3), authentication, configurable retention

