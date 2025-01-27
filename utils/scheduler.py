import schedule
import time
from threading import Thread
import logging
from datetime import datetime
from utils.data_fetcher import fetch_migrated_coins, update_market_data
from utils.sentiment_analyzer import analyze_sentiment

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self._running = False
        self._thread = None
        self.last_run = {
            'market_data': None,
            'sentiment': None,
            'migrations': None
        }

    def start(self):
        if not self._running:
            self._running = True
            self._thread = Thread(target=self._run_scheduler, daemon=True)
            self._thread.start()
            logger.info("Scheduler started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
            logger.info("Scheduler stopped")

    def _run_scheduler(self):
        # Schedule jobs
        schedule.every(15).minutes.do(self._run_market_update)
        schedule.every(1).hours.do(self._run_sentiment_analysis)
        schedule.every(6).hours.do(self._run_fetch_migrations)
        
        while self._running:
            schedule.run_pending()
            time.sleep(1)

    def _run_market_update(self):
        update_market_data()
        self.last_run['market_data'] = datetime.now()

    def _run_sentiment_analysis(self):
        analyze_sentiment()
        self.last_run['sentiment'] = datetime.now()

    def _run_fetch_migrations(self):
        fetch_migrated_coins()
        self.last_run['migrations'] = datetime.now()

    def get_task_status(self):
        return {
            'Update Market Data': {
                'schedule': 'Every 15 min',
                'last_run': self.last_run['market_data'],
                'status': 'Active' if self._running else 'Inactive'
            },
            'Sentiment Analysis': {
                'schedule': 'Every hour',
                'last_run': self.last_run['sentiment'],
                'status': 'Active' if self._running else 'Inactive'
            },
            'Fetch Migrations': {
                'schedule': 'Every 6 hours',
                'last_run': self.last_run['migrations'],
                'status': 'Active' if self._running else 'Inactive'
            }
        } 