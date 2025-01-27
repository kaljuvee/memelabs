from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Boolean, Text
from utils.db_pool import DatabasePool
from utils.log_util import setup_logging
import datetime

Base = DatabasePool.Base
logger = setup_logging(__name__)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    level = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    trace = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Log {self.timestamp} {self.level} {self.name}: {self.message}>"

class MigratedCoin(Base):
    __tablename__ = 'migrated_coins'
    id = Column(Integer, primary_key=True)
    coin_name = Column(String, nullable=False)
    coin_symbol = Column(String, nullable=False, index=True)
    migration_date = Column(DateTime, default=datetime.datetime.utcnow)
    market_cap = Column(Float)
    volume = Column(Float)
    developer_id = Column(String)
    twitter_handle = Column(String)
    contract_status = Column(String, nullable=True)
    supply_bundled = Column(Boolean, default=False)
    contract_address = Column(String, nullable=True)

    __table_args__ = (
        Index('idx_coin_symbol', 'coin_symbol'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"Created new MigratedCoin entry: {self.coin_symbol}")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_value = getattr(self, key)
                setattr(self, key, value)
                logger.info(f"Updated {self.coin_symbol} {key}: {old_value} -> {value}")

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('migrated_coins.id'), nullable=False)
    tweet_id = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    sentiment = Column(Float)
    created_at = Column(DateTime, nullable=False)
    likes = Column(Integer)
    retweets = Column(Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"Created new Tweet entry: {self.tweet_id}")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_value = getattr(self, key)
                setattr(self, key, value)
                logger.info(f"Updated Tweet {self.tweet_id} {key}: {old_value} -> {value}") 