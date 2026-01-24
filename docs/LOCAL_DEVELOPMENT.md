# 🖥️ Local Development Guide - Promotion Hub

**Status:** ✅ Ready for local development  
**Database:** Shared PostgreSQL on Render (same for local + production)  
**Duration:** 5-minute setup

---

## Quick Start (5 minutes)

### 1. Clone & Setup

```bash
# Navigate to project
cd c:\Users\ПК\vat-verbung\promotion_hub

# Create Python virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

**Your `.env` file is already configured with:**
- ✅ `DATABASE_URL` - PostgreSQL on Render
- ✅ All social media credentials (LinkedIn, Telegram, Instagram)
- ✅ `TELEGRAM_API_ID` & `TELEGRAM_API_HASH` - For advanced Telegram features
- ✅ API keys (OpenAI, Gemini)
- ✅ `LOG_LEVEL=DEBUG` for development

**Optional: Add Telegram API credentials for group search:**
```bash
# Get from: https://my.telegram.org/auth
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

### 3. Start Local Development

```bash
python main.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║                  PROMOTION HUB v1.0                       ║
║          B2B Marketing Automation Platform                ║
╚═══════════════════════════════════════════════════════════╝

🔍 Running pre-flight checks...
✅ All systems ready!

📦 Initializing database...
✅ Database initialized

🚀 Starting scheduler...
✅ PROMOTION HUB STARTED SUCCESSFULLY!
```

---

## Understanding the System

### What's Running

**Scheduler with 13 automatic jobs:**

| Channel | Frequency | Job |
|---------|-----------|-----|
| **LinkedIn** | 2x daily | Publish post (08:00, 15:00) |
| **Instagram** | 3x daily | Publish post (09:00, 13:00, 19:00) |
| **Telegram** | 5x daily | Publish post (08:00, 11:00, 14:00, 17:00, 20:00) |
| **Telegram** | Every 6-8 hours | Collect audience |
| **Telegram** | Every 2-3 hours | Send invites to leads |
| **Daily** | 02:00 UTC | Cleanup old logs |

### Database Architecture

**PostgreSQL on Render (shared):**

```
Database: promotion_hub
├── posts
│   ├── id (PK)
│   ├── content_de (German content)
│   ├── content_adapted (Auto-adapted per channel)
│   ├── cta_template (Call-to-action)
│   ├── published_at
│   └── status
├── leads
│   ├── id (PK)
│   ├── username (Telegram/Instagram)
│   ├── score (0.0-1.0)
│   ├── invited_at
│   └── source (telegram/instagram)
├── actions
│   ├── id (PK)
│   ├── lead_id (FK)
│   ├── action_type
│   ├── timestamp
│   └── metadata (JSON)
└── logs
    ├── id (PK)
    ├── timestamp
    ├── level (INFO/DEBUG/ERROR)
    └── message
```

---

## Development Workflows

### 1. Testing Content Generation

```bash
# Add test posts to database
python scripts/add_test_leads.py

# Check generated content
# Look in logs/promotion_hub.log for content generation details
```

### 2. Testing Lead Scoring & Invites

```bash
# 1. Add test leads with various scores
python scripts/add_test_leads.py

# 2. Watch Telegram collection job (every 6-8 hours)
# OR trigger manually in scheduler (edit core/scheduler.py for testing)

# 3. Check database for leads and action logs
# SELECT * FROM leads WHERE score >= 0.5;
# SELECT * FROM actions WHERE action_type = 'invite';
```

### 3. Testing Telegram Group Search

```bash
# 1. Configure Telegram API credentials in .env
# TELEGRAM_API_ID=your_api_id
# TELEGRAM_API_HASH=your_api_hash

# 2. Test group search
python test_telegram_search.py

# 3. Expected output: List of German construction/renovation groups
#    - Baugruppen, Renovierung, Immobilien, Handwerker, etc.

# 4. Add found group IDs to scheduler for lead collection
# Edit core/scheduler.py: chat_ids = [-1001234567890, ...]
```

### 4. Testing Instagram Account Search

```bash
# 1. Ensure Instagram session is initialized
# INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_SESSION in .env

# 2. Test account discovery by keywords
python test_instagram_search.py

# 3. Expected output: List of German construction/renovation accounts
#    - Business accounts, bloggers, contractors, architects
#    - Accounts with >500 followers, verified status
#    - Keywords: Bau, Renovierung, Immobilien, Handwerker, etc.

# 4. Test deep follower analysis (optional)
# Edit test_instagram_search.py to call collect_from_found_accounts()
# Analyze followers of discovered accounts for B2B potential

# 5. Integration test: Feed results to analyzer
# python -c "from channels.instagram.analyzer import InstagramAnalyzer; analyzer = InstagramAnalyzer(); print('Analyzer ready')"
```

### 3. Testing Publishing

**LinkedIn (requires Playwright headless browser):**
```bash
# Requires LinkedIn account credentials in .env
# LINKEDIN_EMAIL and LINKEDIN_PASSWORD

# Job runs: 08:00 and 15:00 UTC
# Or manually trigger in scheduler.py for testing
```

**Telegram (API-based, no credentials needed):**
```bash
# Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env
# Optional: TELEGRAM_API_ID and TELEGRAM_API_HASH for advanced features
#   - Group search by keywords (Bau, Renovierung, Immobilien)
#   - Lead collection from chats and channels
#   - Automated group discovery and joining
# Job runs: 08:00, 11:00, 14:00, 17:00, 20:00 UTC
# Watch logs for publication success
```

**Instagram (requires residential IP for VPS):**
```bash
# Works locally but may hit IP blocks from Render
# For production: Deploy to VPS with residential IP (see VPS_DEPLOYMENT.md)
# Job runs: 09:00, 13:00, 19:00 UTC

# NEW: Account Discovery Testing
# 1. Test account search: python test_instagram_search.py
# 2. Discover construction/renovation accounts automatically
# 3. Analyze followers for B2B leads
# 4. Feed to analyzer for scoring and invitations
```

---

## Monitoring & Debugging

### Real-time Logs

```bash
# Terminal 1: Run main system
python main.py

# Terminal 2: Follow logs in real-time
Get-Content logs/promotion_hub.log -Wait
```

### Log Levels

```bash
# Edit .env to change log level
LOG_LEVEL=DEBUG    # Most verbose (for development)
LOG_LEVEL=INFO     # Standard info messages
LOG_LEVEL=ERROR    # Only errors
```

### Common Log Patterns

**Successful LinkedIn post:**
```
2025-01-21 08:00:15 - LinkedInPublisher - INFO - ✅ Posted on LinkedIn
```

**Lead scoring in action:**
```
2025-01-21 09:30:45 - LeadScorer - INFO - Scored lead @username: 0.72/1.0 (B2B match)
```

**Telegram invitation sent:**
```
2025-01-21 10:15:30 - TelegramPublisher - INFO - ✅ Invited @username with score 0.72
```

**Database issues:**
```
2025-01-21 11:00:00 - DatabaseConnection - ERROR - Failed to connect: connection refused
```

---

## Database Access

### Direct PostgreSQL Access (Optional)

If you want to query the database directly:

```bash
# Install PostgreSQL client
# Then use:
psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.frankfurt-postgres.render.com/ittoken_db"

# Useful queries:
SELECT COUNT(*) FROM posts;                    # How many posts generated?
SELECT COUNT(*) FROM leads WHERE score > 0.5; # How many good leads?
SELECT * FROM actions ORDER BY timestamp DESC LIMIT 10; # Recent actions
SELECT COUNT(*) FROM logs WHERE level = 'ERROR'; # Error count
```

---

## Troubleshooting

### "No module named 'X'"

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "PostgreSQL connection refused"

```bash
# Check .env DATABASE_URL is correct
# Should be: postgresql://ittoken_db_user:...@dpg-...render.com/ittoken_db

# Verify database is online
# Go to: https://dashboard.render.com → PostgreSQL → Status
```

### "Scheduler not triggering jobs"

```bash
# Check timezone in logs (should be UTC)
# Check job times match your timezone:
#   08:00 UTC = depends on your local timezone

# Jobs are scheduled in UTC, adjust for your timezone
# Example: 08:00 UTC = 09:00 CET = 16:00 JST
```

### "Telegram API credentials incomplete"

```bash
# Required for advanced Telegram features (group search, etc.)
# Get credentials from: https://my.telegram.org/auth

# 1. Go to https://my.telegram.org/auth
# 2. Log in with your phone number
# 3. Go to "API development tools"
# 4. Create application to get:
#    - api_id: TELEGRAM_API_ID
#    - api_hash: TELEGRAM_API_HASH

# Add to .env:
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
```

### "Instagram IP blocked"

```bash
# Expected behavior from Render datacenter IP
# Solution: Deploy to VPS with residential IP

# For local testing: Skip Instagram, focus on LinkedIn/Telegram
# Instagram will work on VPS (see docs/VPS_DEPLOYMENT.md)
```

### "Playwright browser not found"

```bash
# Required for LinkedIn publishing
# Install Chromium browser:
python -m playwright install
```

---

## Development Tips

### 1. Modify Job Schedules (Temporary)

Edit `core/scheduler.py` in the `start()` method:

```python
# Change from 08:00 UTC to every 5 minutes for testing:
# OLD: self.scheduler.add_job(self._publish_linkedin, 'cron', hour=8, minute=0)
# NEW:
self.scheduler.add_job(self._publish_linkedin, 'interval', minutes=5)
```

### 2. Add Debug Logging

```python
# In any class, add logging:
import logging
logger = logging.getLogger(__name__)

logger.debug(f"Debug info: {variable}")
logger.info(f"Info: {message}")
logger.error(f"Error: {exception}")
```

### 3. Test Content Quality

```bash
# Generate content without publishing:
python
>>> from core.content_generator import ContentGenerator
>>> gen = ContentGenerator()
>>> content = gen.generate_post()
>>> print(content['content_de'])
>>> print(content['content_adapted'])
```

### 4. Test Lead Scoring

```bash
# Check how leads are scored:
python
>>> from core.lead_analyzer import LeadScorer
>>> scorer = LeadScorer()
>>> score = scorer.score_username('@b2b_company')
>>> print(f"Score: {score}")
```

---

## Workflow: From Local to VPS

### Phase 1: Local Development ✅ (You are here)

1. ✅ Run `python main.py` locally
2. ✅ Monitor logs in `logs/promotion_hub.log`
3. ✅ Test content generation, lead scoring, Telegram/LinkedIn
4. ✅ Skip Instagram testing (IP blocking on Render connection)
5. ✅ Fix any issues found in testing

### Phase 2: Deploy to VPS (When ready)

```bash
# 1. Follow docs/VPS_DEPLOYMENT.md or QUICKSTART_VPS.md
# 2. Choose VPS provider (Hetzner €5/month recommended)
# 3. Deploy code with full Instagram support
# 4. Monitor from Render PostgreSQL (same database)
```

### Phase 3: Production Monitoring

```bash
# Monitor from local machine:
# - Logs: Check logs/promotion_hub.log on VPS
# - Database: Query same Render PostgreSQL from local
# - Notifications: Set up alerts for errors
```

---

## Key Files for Development

```
promotion_hub/
├── main.py                          # Entry point (python main.py)
├── core/
│   ├── scheduler.py                 # APScheduler with 13 jobs
│   ├── content_generator.py         # Content generation logic
│   ├── db_init.py                   # Database initialization
│   └── db.py                        # Database connection pool
├── channels/
│   ├── linkedin/publisher.py        # LinkedIn publishing
│   ├── telegram/publisher.py        # Telegram publishing
│   └── instagram/publisher.py       # Instagram publishing
├── models.py                        # SQLAlchemy ORM models
├── scripts/
│   └── add_test_leads.py            # Add test data
├── logs/
│   └── promotion_hub.log            # All logs (watch this!)
├── requirements.txt                 # Python dependencies
├── .env                             # Configuration (DATABASE_URL, etc)
└── docs/
    ├── LOCAL_DEVELOPMENT.md         # ← You are here
    ├── VPS_DEPLOYMENT.md            # Full VPS setup guide
    └── QUICKSTART_VPS.md            # 5-minute VPS setup
```

---

## Next Steps

1. **Run locally:**
   ```bash
   python main.py
   ```

2. **Watch logs:**
   ```bash
   Get-Content logs/promotion_hub.log -Wait
   ```

3. **Add test leads:**
   ```bash
   python scripts/add_test_leads.py
   ```

4. **Monitor results:**
   - Check database for posts, leads, actions
   - Verify scheduler jobs trigger on schedule
   - Fix any errors in logs

5. **When ready for production:**
   - Follow [VPS_DEPLOYMENT.md](VPS_DEPLOYMENT.md) or [QUICKSTART_VPS.md](QUICKSTART_VPS.md)
   - Deploy to Hetzner/DigitalOcean/Linode for €3-5/month
   - Keep using same Render PostgreSQL database
   - Get residential IP for Instagram (no more IP blocking)

---

## Support

**Common Questions:**

- **Q: Why Render PostgreSQL instead of local SQLite?**  
  **A:** Shared database between local dev and VPS production. Easy testing.

- **Q: Can I run without the scheduler?**  
  **A:** Yes, comment out `scheduler.run()` in main.py for testing individual components.

- **Q: Do I need all social media credentials?**  
  **A:** Not for local testing. Focus on Telegram (no credentials), test others when ready.

- **Q: How to reset database for fresh testing?**  
  **A:** All tables auto-create from models. Drop tables manually in PostgreSQL if needed.

---

## 📱 Telegram API Credentials Setup

**For advanced Telegram features (group search, lead collection):**

### 1. Get API Credentials
```bash
# Go to: https://my.telegram.org/auth
# 1. Log in with your phone number
# 2. Go to "API development tools"
# 3. Create new application
# 4. Copy api_id and api_hash
```

### 2. Add to .env
```bash
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
```

### 3. Test Group Search
```bash
python test_telegram_search.py
```

### 4. What You Get
- 🔍 **Group Search:** Find German construction/renovation groups
- 👥 **Lead Collection:** Extract contacts from chats and channels  
- 🤖 **Auto Discovery:** Find and join relevant groups automatically
- 📊 **B2B Targeting:** Focus on business contacts in construction sector

**Keywords for German market:**
- `Bau` (Construction)
- `Renovierung` (Renovation) 
- `Immobilien` (Real Estate)
- `Handwerker` (Tradesmen)
- `Baufirma` (Construction Company)
- `Sanierung` (Refurbishment)

---

**Happy developing! 🚀**
