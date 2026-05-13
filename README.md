# JobBoard Pro

A full-stack job listing and application management platform built with FastAPI and Next.js.

## Prerequisites
- Python 3.14 (managed via `uv`)
- Node.js (v18+)

## Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Initialize the environment: `uv init --python 3.14`
3. Add dependencies: `uv add fastapi uvicorn sqlalchemy pydantic pytest httpx`
4. Run the server: `uv run uvicorn app.main:app --reload`

The API will be available at `http://localhost:8000`. 
API Documentation available at `http://localhost:8000/docs`.

## Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

The UI will be available at `http://localhost:3000`.

## Testing
Run tests from the root directory:
```bash
cd backend
uv run pytest ../tests/ -v