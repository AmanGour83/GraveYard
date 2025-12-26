from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Detect if we are in Docker or on Windows
if os.path.exists("/.dockerenv"):
    DATABASE_URL = "sqlite:////app/data/latent.db"
else:
    # Use a local file when testing with Uvicorn
    DATABASE_URL = "sqlite:///./local_latent.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()