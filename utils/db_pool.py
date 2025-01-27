from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL based on environment selection"""
    env = getattr(st.session_state, 'db_environment', 'LIVE')  # Default to LIVE if not set
    if env == 'LIVE':
        return os.getenv('LIVE_DB_URL')
    return os.getenv('DEV_DB_URL')

# Create engine with dynamic DATABASE_URL
def create_db_engine():
    DATABASE_URL = get_database_url()
    return create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# Create session factory with dynamic engine
engine = create_db_engine()
session_factory = sessionmaker(bind=engine)

# Create thread-safe session
Session = scoped_session(session_factory)

def get_db():
    """Get a new database session"""
    db = Session()
    try:
        yield db
    finally:
        db.close()
