import sys
import os
import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Dynamically add the /backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# 2. Now Python knows where to find 'app'
from app.main import app
from app.database import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Helper function to get a future date
def future_date(days=30):
    return (datetime.date.today() + datetime.timedelta(days=days)).isoformat()

def test_create_job_success():
    response = client.post(
        "/api/jobs",
        json={
            "title": "Senior AI Engineer",
            "department": "Engineering",
            "description": "Build multi-agent systems.",
            "location": "remote",
            "salary_min": 120000,
            "salary_max": 160000,
            "required_skills": ["Python", "FastAPI", "LangGraph"],
            "max_applicants": 50,
            "deadline": future_date()
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Senior AI Engineer"
    assert "id" in data

def test_create_job_invalid_salary():
    response = client.post(
        "/api/jobs",
        json={
            "title": "Data Scientist",
            "department": "Data",
            "description": "Analyze things.",
            "location": "hybrid",
            "salary_min": 150000,  # Min is higher than Max
            "salary_max": 100000,
            "required_skills": ["Python", "SQL"],
            "deadline": future_date()
        },
    )
    assert response.status_code == 422
    assert "salary_min must be strictly less than salary_max" in response.text