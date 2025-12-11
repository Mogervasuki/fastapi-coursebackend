cat > README.md <<'EOF'
# Course API (Enrollment, Progress, Rating, Access Control)

## Overview
This is a simple FastAPI project implementing:
- Enroll users into courses
- Mark lessons completed (idempotent)
- Get user progress in a course
- Submit / retrieve course ratings (only enrolled users)
- Access control: only enrolled users can fetch lessons

## Files
- `main.py` — FastAPI application (single-file implementation)
- `requirements.txt` — Python dependencies

## Run locally
1. Create and activate a virtual environment:
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate
     ```
    - To run main.py file:
     uvicorn main:app --reload 

2. Install dependencies:
```bash
pip install -r requirements.txt
