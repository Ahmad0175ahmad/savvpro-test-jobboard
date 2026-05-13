from sqlalchemy import Column, Integer, String, Boolean, Date, Enum as SQLAlchemyEnum, JSON
import enum
from .database import Base

class LocationEnum(str, enum.Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    department = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    location = Column(SQLAlchemyEnum(LocationEnum), nullable=False)
    salary_min = Column(Integer, nullable=False)
    salary_max = Column(Integer, nullable=False)
    required_skills = Column(JSON, nullable=False) # Stored as JSON/Text in SQLite
    max_applicants = Column(Integer, nullable=True)
    deadline = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=False)