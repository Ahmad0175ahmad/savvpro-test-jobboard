from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import cast, String
from datetime import date
from typing import Optional
def create_job_listing(db: Session, job: schemas.JobListingCreate):
    db_job = models.JobListing(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(
    db: Session,
    page: int = 1,
    per_page: int = 10,
    department: Optional[str] = None,
    location: Optional[str] = None,
    skill: Optional[str] = None,
    include_closed: bool = False
):
    query = db.query(models.JobListing)

    # Filter out closed and expired listings by default
    if not include_closed:
        query = query.filter(
            models.JobListing.is_closed == False,
            models.JobListing.deadline >= date.today()
        )

    # Apply simultaneous filtering if provided
    if department:
        query = query.filter(models.JobListing.department.ilike(f"%{department}%"))
    
    if location:
        query = query.filter(models.JobListing.location == location)
        
    if skill:
        # Cast the JSON array to a string to check if the skill exists inside it
        query = query.filter(cast(models.JobListing.required_skills, String).ilike(f"%\"{skill}\"%"))

    total_count = query.count()
    offset = (page - 1) * per_page
    results = query.offset(offset).limit(per_page).all()

    return {
        "total_count": total_count,
        "page": page,
        "per_page": per_page,
        "results": results
    }