from fastapi import FastAPI, Depends, HTTPException
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