from pydantic import BaseModel, model_validator, ConfigDict
from typing import List, Optional
from datetime import date
from enum import Enum

class LocationEnum(str, Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"

class JobListingBase(BaseModel):
    title: str
    department: str
    description: str
    location: LocationEnum
    salary_min: int
    salary_max: int
    required_skills: List[str]
    max_applicants: Optional[int] = None
    deadline: date
    is_closed: bool = False

    @model_validator(mode='after')
    def check_salary(self) -> 'JobListingBase':
        if self.salary_min >= self.salary_max:
            raise ValueError('salary_min must be strictly less than salary_max')
        return self

class JobListingCreate(JobListingBase):
    pass

class JobListingResponse(JobListingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedJobListingResponse(BaseModel):
    total_count: int
    page: int
    per_page: int
    results: List[JobListingResponse]
    
    model_config = ConfigDict(from_attributes=True)