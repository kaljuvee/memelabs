import logging
import sys
from functools import wraps
from datetime import datetime
import traceback

class DatabaseLogHandler(logging.Handler):
    def __init__(self, session_maker):
        super().__init__()
        self.session_maker = session_maker

    def emit(self, record):
        # Import here to avoid circular imports
        from utils.models import Log

        try:
            # Create new session for this log entry
            with self.session_maker() as session:
                log_entry = Log(
                    timestamp=datetime.fromtimestamp(record.created),
                    level=record.levelname,
                    name=record.name,
                    message=record.getMessage(),
                    trace=record.exc_text if record.exc_text else None
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            # Fallback to sys.stderr if database logging fails
            sys.stderr.write(f"Failed to log to database: {str(e)}\n")

def setup_logging(name=__name__, level=logging.INFO, db_session_maker=None):
    """
    Configure logging with console and database output
    
    Args:
        name (str): Logger name (usually __name__)
        level (int): Logging level (default: logging.INFO)
        db_session_maker: SQLAlchemy session maker for database logging
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handlers if they don't exist
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Database handler
        if db_session_maker:
            db_handler = DatabaseLogHandler(db_session_maker)
            db_handler.setLevel(level)
            logger.addHandler(db_handler)

    return logger

def log_exceptions(logger):
    """
    Decorator to log exceptions
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Exception in {func.__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        return wrapper
    return decorator

def get_logger(name):
    """
    Get an existing logger or create a new one
    """
    return logging.getLogger(name) 