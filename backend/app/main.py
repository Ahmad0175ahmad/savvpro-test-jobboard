from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobBoard Pro API")

@app.post("/api/jobs", response_model=schemas.JobListingResponse, status_code=201)
def create_job(job: schemas.JobListingCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_job_listing(db=db, job=job)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/jobs", response_model=schemas.PaginatedJobListingResponse)
def read_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    department: Optional[str] = None,
    location: Optional[schemas.LocationEnum] = None,
    skill: Optional[str] = None,
    include_closed: bool = False,
    db: Session = Depends(get_db)
):
    return crud.get_jobs(
        db=db,
        page=page,
        per_page=per_page,
        department=department,
        location=location.value if location else None,
        skill=skill,
        include_closed=include_closed
    )