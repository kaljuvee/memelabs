from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from utils.log_util import setup_logging
import os

# Load environment variables
load_dotenv()

# Create declarative base
Base = declarative_base()

class DatabasePool:
    _instance = None
    _engine = None
    _Session = None
    _logger = None
    Base = Base  # Add Base as a class attribute

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabasePool, cls).__new__(cls)
            cls._instance._logger = setup_logging(__name__)
        return cls._instance

    def __init__(self):
        if not self._engine:
            self._initialize_engine()

    def _initialize_engine(self):
        """Initialize database engine with URL from environment variables"""
        database_url = os.getenv('DB_URL')
        if not database_url:
            raise ValueError("DB_URL environment variable is not set")
        
        self._engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=10
        )
        self._Session = scoped_session(sessionmaker(bind=self._engine))
        self._logger.info("Database engine initialized")

    def get_session(self):
        """Get a new database session"""
        if not self._Session:
            self._initialize_engine()
        return self._Session()

    def create_all_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self._engine)
        self._logger.info("Database tables created")

    @property
    def engine(self):
        """Get the SQLAlchemy engine"""
        if not self._engine:
            self._initialize_engine()
        return self._engine

# Global instance for convenience
db_pool = DatabasePool()

def get_db():
    """Get a new database session"""
    db = db_pool.get_session()
    try:
        yield db
    finally:
        db.close()
