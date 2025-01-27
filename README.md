# Memelabs - Crypto Migration Monitor

A comprehensive tool for monitoring and analyzing cryptocurrency migrations, market data, and social sentiment.

## Overview

Memelabs is a Python-based system that:
- Tracks cryptocurrency migrations and market data
- Analyzes social media sentiment
- Provides scheduled data collection and analysis
- Stores data in PostgreSQL database
- Visualizes data through a Streamlit dashboard

## Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
Copy `.env.sample` to `.env` and set your credentials:
```bash
DB_URL='postgresql://user:password@host:port/dbname'
```

3. **Initialize Database**
```bash
python main.py init
```

## Command Line Usage

### Run Individual Tasks
```bash
# Fetch new migrated coins data
python main.py task fetch

# Update market data
python main.py task market

# Run sentiment analysis
python main.py task sentiment
```

### Run Scheduler
```bash
# Run indefinitely
python main.py scheduler

# Run for specific duration (in minutes)
python main.py scheduler --duration 60
```

### Dashboard
```bash
streamlit run Home.py
```

## Project Structure

```
memelabs/
├── utils/
│   ├── __init__.py
│   ├── db_pool.py        # Database connection pool
│   ├── models.py         # Database models
│   ├── scheduler.py      # Task scheduler
│   ├── data_fetcher.py   # Data collection
│   └── sentiment_analyzer.py  # Sentiment analysis
├── main.py              # CLI entry point
├── Home.py             # Streamlit dashboard
├── requirements.txt    # Dependencies
└── .env               # Configuration
```

## Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| Market Data | Every 15 min | Updates price and volume data |
| Sentiment | Every hour | Analyzes social media sentiment |
| Migrations | Every 6 hours | Fetches new coin migrations |

## Development

### Adding New Tasks

1. Create task function in appropriate module
2. Add to task registry in `main.py`:
```python
tasks = {
    'new_task': your_new_function,
    ...
}
```
3. Update scheduler if needed

### Database Models

Models are defined in `utils/models.py`:
- `MigratedCoin`: Stores coin migration data
- `Tweet`: Stores social media data and sentiment

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## License

MIT License