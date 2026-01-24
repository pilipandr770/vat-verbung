# Docker Setup for Promotion Hub

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- Your `.env` file with all credentials

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env .env.docker
   ```

2. **Edit `.env.docker` with your credentials:**
   Make sure all API keys and credentials are set.

3. **Build and run:**
   ```bash
   # Build the application
   docker-compose build

   # Start all services
   docker-compose up -d

   # View logs
   docker-compose logs -f app
   ```

## Services

### Application (app)
- **Port:** None (internal only)
- **Logs:** `docker-compose logs -f app`
- **Restart:** Automatic on failure

### Database (db)
- **Port:** 5432 (PostgreSQL)
- **Data:** Persistent in `postgres_data` volume
- **Health Check:** Automatic

### PgAdmin (pgadmin) - Optional
- **Port:** 8080
- **URL:** http://localhost:8080
- **Credentials:** admin@promotionhub.com / admin123
- **Profile:** Only runs with `docker-compose --profile debug up`

## Environment Variables

Copy your existing `.env` file and ensure these are set:

```bash
# Database (auto-configured in docker-compose)
DATABASE_URL=postgresql://promotion_user:promotion_password@db:5432/promotion_hub

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

# Instagram
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
INSTAGRAM_SESSION=your_session_string

# LinkedIn
LINKEDIN_USERNAME=your_email
LINKEDIN_PASSWORD=your_password
LINKEDIN_COMPANY_ID=your_company_id

# AI
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

## Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
docker-compose logs -f db

# Rebuild application
docker-compose build --no-cache app

# Run database migrations (if needed)
docker-compose exec app python core/db_init.py

# Access database directly
docker-compose exec db psql -U promotion_user -d promotion_hub

# Debug with PgAdmin
docker-compose --profile debug up pgadmin
```

## Troubleshooting

### Application won't start
```bash
# Check logs
docker-compose logs app

# Check if database is ready
docker-compose ps

# Restart application
docker-compose restart app
```

### Database connection issues
```bash
# Check database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up -d db
```

### Memory issues
```bash
# Increase Docker memory limit to 4GB+
# Or run with limited concurrency
docker-compose exec app python main.py --max-workers 2
```

## Production Deployment

For production, consider:

1. **Use external PostgreSQL** instead of container
2. **Add reverse proxy** (nginx/caddy)
3. **Enable SSL/TLS**
4. **Set up monitoring** (Prometheus/Grafana)
5. **Configure backups**
6. **Use Docker secrets** for sensitive data

## File Structure

```
promotion_hub/
├── Dockerfile              # Application container
├── docker-compose.yml      # Multi-service setup
├── .dockerignore          # Files to exclude
├── scripts/
│   └── init_db.sql        # Database initialization
├── client_config/         # Client configuration
├── logs/                  # Application logs (mounted)
└── data/                  # Data storage (mounted)
```