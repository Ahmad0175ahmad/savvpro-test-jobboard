from sqlalchemy.orm import Session
from . import models, schemas

def create_job_listing(db: Session, job: schemas.JobListingCreate):
    db_job = models.JobListing(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job