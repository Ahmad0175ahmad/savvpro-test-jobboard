# AI Tool Usage Documentation

**AI Assistant Used:** [Gemini, ChatGPT,Claude]

## Documented Prompts
*(Verbatim prompts used during development)*

1. **Prompt 1:** "**Prompt 1 (Setup & Feature 1):**
> Act as an expert Python developer using FastAPI. We are building the backend for JobBoard Pro using Python 3.14, `uv` for dependency management, and SQLite. 
> 1. Set up the basic FastAPI structure in a `/backend/app` folder (main.py, models.py, schemas.py, crud.py, database.py).
> 2. Create the SQLAlchemy model and Pydantic schemas for Feature 1: A "JobListing" with title, department, description, location (enum: remote, hybrid, onsite), salary_min, salary_max, required_skills (store as JSON/Text in SQLite), max_applicants (optional), deadline (date), and is_closed (boolean, default False). 
> 3. Enforce server-side validation in Pydantic so `salary_min` is strictly less than `salary_max`.
> 4. Create the `POST /api/jobs` endpoint to create a job.
> 5. Write a `pytest` file in `/tests/test_jobs.py` using `TestClient` to verify job creation and verify the salary validation fails correctly.
"
2. **Prompt 2:** "[Paste prompt]"
3. **Prompt 3:** "[Paste prompt]"
4. **Prompt 4:** "[Paste prompt]"
5. **Prompt 5:** "[Paste prompt]"

## AI Errors & Corrections

1. **Error:** The AI generated a Pydantic schema that allowed `salary_min` to be greater than `salary_max`.
   **Correction:** Prompted the AI to add a `@model_validator(mode='after')` in Pydantic to strictly enforce `salary_min < salary_max` at the schema level before database insertion.

2. **Error:** [Document another error, e.g., AI forgot to include the status history note in the DB, or used Postgres specific JSON syntax instead of SQLite compatible text fields]
   **Correction:** [Document how you fixed it]