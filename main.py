from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# Database setup (SQLite)
engine = create_engine("sqlite:///jobs.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Database model
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    role = Column(String)
    status = Column(String)

Base.metadata.create_all(bind=engine)

# API schema
class JobCreate(BaseModel):
    company: str
    role: str
    status: str

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Create job application
@app.post("/jobs")
def create_job(job: JobCreate):
    db = SessionLocal()
    new_job = Job(
        company=job.company,
        role=job.role,
        status=job.status
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    db.close()
    return new_job

# List all job applications
@app.get("/jobs", response_model=List[JobCreate])
def list_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()
    return jobs
