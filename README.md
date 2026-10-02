# 24124966_calculator_backend

Front-End and Back-End Separation Calculator System — **Backend Project**

## Project Introduction

This is the backend part of the "Front-End and Back-End Separation Calculator System", the first assignment of the Software Engineering course.

The backend is responsible for:
- Receiving calculation requests from the front end (HTTP API)
- Validating input and parsing mathematical expressions
- Performing expression calculation (supports arithmetic operations, parentheses, unary signs, decimals)
- Handling exceptions (invalid expressions, division by zero)
- Persisting calculation history into the SQLite database
- Providing query and deletion APIs for history records
- Returning standardized JSON API responses

All calculation logic is completed in the backend and **does not rely on the front end**, satisfying the "front-end and back-end separation" requirement of the assignment.

## Tech Stack

| Module | Technology |
| --- | --- |
| Backend Framework | Python 3 + Flask |
| Database | SQLite (built into Python) |
| Expression Calculation | Self-implemented recursive descent parser (no eval) |

## Runtime Environment

- Python 3.8 or above (developed and tested on Python 3.14)
- OS: Windows / macOS / Linux

## Installation

```bash
# Enter the backend project directory
cd 24124966_calculator_backend

# (Recommended) Create a virtual environment
python -m venv venv

# Activate the virtual environment on Windows
venv\Scripts\activate
# Activate the virtual environment on macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## How to Start

```bash
python app.py
```

After startup, the service runs at `http://127.0.0.1:5000`, and the console shows:
`Running on http://0.0.0.0:5000`

## Configuration

All configuration is at the top of `app.py`; you can adjust the arguments of `app.run()`:
- `port=5000`: service port
- `host="0.0.0.0"`: allows LAN access (change to `127.0.0.1` for local-only access)
- `PORT` environment variable: if set (e.g., by a cloud platform), it overrides the default port

## Database Initialization

No manual initialization is required. On first startup, `database.py` automatically creates the `calculator.db` file and the `calculation_history` table in the project directory:

```sql
CREATE TABLE calculation_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    expression  TEXT    NOT NULL,   -- the expression
    result      TEXT    NOT NULL,   -- the result
    created_at  TEXT    NOT NULL    -- the calculation time
);
```

To reset the database, delete the `calculator.db` file and restart the service.

## How the Front End Connects

The front end accesses the backend through HTTP requests; see the `24124966_calculator_frontend` repository. The default backend address configured in the front end is:

```
https://zlin05.pythonanywhere.com
```

For local development, use `http://127.0.0.1:5000`.

## API Documentation

### 1. Calculate an Expression

```
POST /api/calculate
Content-Type: application/json
```

Request body:

```json
{
  "expression": "12+8"
}
```

Success response (HTTP 200):

```json
{
  "success": true,
  "id": 1,
  "expression": "12+8",
  "result": 20
}
```

Error response (HTTP 400, invalid expression):

```json
{
  "success": false,
  "message": "Invalid expression"
}
```

Error response (HTTP 400, division by zero):

```json
{
  "success": false,
  "message": "Division by zero"
}
```

### 2. Get All Calculation History

```
GET /api/history
```

Success response (HTTP 200):

```json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "expression": "(2+3)*4",
      "result": "20",
      "created_at": "2026-10-01 10:22:00"
    }
  ]
}
```

### 3. Delete One History Record by ID

```
DELETE /api/history/{id}
```

Success response (HTTP 200):

```json
{
  "success": true
}
```

Record not found (HTTP 404):

```json
{
  "success": false,
  "message": "Record not found"
}
```

### 4. Clear All History Records (Extra Feature)

```
DELETE /api/history
```

Success response (HTTP 200):

```json
{
  "success": true
}
```

### 5. Health Check

```
GET /api/health
```

## Directory Structure

```
24124966_calculator_backend/
├── app.py            # Flask main program, defines all API endpoints
├── calculator.py     # Expression parsing and calculation module (recursive descent parser)
├── database.py       # SQLite database operations module
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
└── codestyle.md      # Code style guide
```

## Code Style

The code follows [PEP 8](https://peps.python.org/pep-0008/). See [codestyle.md](codestyle.md).
