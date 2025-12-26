from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import threading
import time

from .database import engine, Base, get_db
from .models import Project
from .schemas import ProjectCreate, ProjectResponse 
from .container_manager import launch_demo_session
from .reaper import reap_zombies

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background Cleanup Thread
def start_reaper():
    while True:
        try:
            reap_zombies()
        except:
            pass
        time.sleep(60)

threading.Thread(target=start_reaper, daemon=True).start()

# --- API Endpoints ---

@app.post("/projects/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(
        name=project.name, 
        description=project.description,
        docker_image=project.docker_image,
        internal_port=project.internal_port
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=List[ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def read_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/projects/{project_id}/launch")
def launch_project(project_id: int, db: Session = Depends(get_db)):
    assigned_port = launch_demo_session(db, project_id)
    if not assigned_port:
        raise HTTPException(status_code=500, detail="Failed to launch container")
    
    return {
        "url": f"http://localhost:{assigned_port}", 
        "expires_in": "15 minutes"
    }