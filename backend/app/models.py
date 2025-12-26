from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
# CRITICAL FIX: Import 'Base' from database.py. Do not create a new one!
from .database import Base 

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True) 
    docker_image = Column(String, nullable=False)
    internal_port = Column(Integer, default=3000)
    
    sessions = relationship("DemoSession", back_populates="project")

class DemoSession(Base):
    __tablename__ = "demo_sessions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    session_token = Column(String, unique=True, index=True)
    container_id = Column(String, unique=True)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    project = relationship("Project", back_populates="sessions")