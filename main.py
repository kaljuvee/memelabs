import argparse
import logging
import sys
import time
from utils.db_pool import DatabasePool
from utils.scheduler import TaskScheduler
from utils.data_fetcher import fetch_migrated_coins, update_market_data
from utils.sentiment_analyzer import analyze_sentiment

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def init_database():
    db = DatabasePool()
    db.create_all_tables()
    logging.info("Database initialized")

def run_scheduler(duration=None):
    """Run the scheduler for a specified duration (in minutes) or indefinitely"""
    scheduler = TaskScheduler()
    scheduler.start()
    
    try:
        if duration:
            time.sleep(duration * 60)
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        logging.info("Scheduler stopped by user")

def run_single_task(task_name):
    """Run a single task once"""
    tasks = {
        'fetch': fetch_migrated_coins,
        'market': update_market_data,
        'sentiment': analyze_sentiment
    }
    
    if task_name not in tasks:
        logging.error(f"Unknown task: {task_name}")
        return
    
    logging.info(f"Running task: {task_name}")
    tasks[task_name]()

def main():
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description='Crypto Migration Monitor CLI')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Scheduler command
    scheduler_parser = subparsers.add_parser('scheduler', help='Run the task scheduler')
    scheduler_parser.add_argument(
        '--duration', 
        type=int,
        help='Duration to run in minutes (default: run indefinitely)'
    )
    
    # Task command
    task_parser = subparsers.add_parser('task', help='Run a single task')
    task_parser.add_argument(
        'name',
        choices=['fetch', 'market', 'sentiment'],
        help='Task to run (fetch: fetch migrated coins, market: update market data, sentiment: analyze sentiment)'
    )
    
    # Initialize command
    init_parser = subparsers.add_parser('init', help='Initialize the database')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'scheduler':
            logger.info("Starting scheduler...")
            run_scheduler(args.duration)
            
        elif args.command == 'task':
            logger.info(f"Running single task: {args.name}")
            run_single_task(args.name)
            
        elif args.command == 'init':
            logger.info("Initializing database...")
            init_database()
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 