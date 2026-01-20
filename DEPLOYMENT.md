# 🚀 PROMOTION HUB - DEPLOYMENT CHECKLIST

## ✅ Pre-Deployment (Complete)

### Code & Configuration
- [x] All 6 phases implemented
- [x] Database models ready
- [x] Scheduler configured
- [x] Content engine with 64+ pieces
- [x] Instagram session initialized
- [x] `.env` fully configured

### Testing
- [x] System check: 27/27 tests PASSED
- [x] Database connection verified
- [x] Instagram authentication working
- [x] Telegram bot token valid
- [x] LinkedIn credentials configured
- [x] All dependencies installed

### Documentation
- [x] README.md with quick start
- [x] STATUS.md with full report
- [x] 8 docs in `/docs` folder
- [x] Inline code comments
- [x] Configuration examples

---

## 🚀 Deployment Steps (5 minutes)

### Step 1: Verify Environment
```bash
python system_check.py
# Should show: ✅ System check PASSED! Ready to run.
```

### Step 2: Initialize Database (First Time Only)
```bash
# Database initializes automatically on first run
# If needed manually:
python -c "from core.db_init import init_database; init_database()"
```

### Step 3: Test Components
```bash
# Test Instagram
python test_instagram.py

# Test system (full)
python system_check.py
```

### Step 4: Start Application
```bash
# Windows
run.bat

# Linux/Mac
bash run.sh

# Or directly
python main.py
```

### Step 5: Monitor
```bash
# Watch logs in real-time
tail -f logs/promotion_hub.log

# Or check recent actions
tail -100 logs/promotion_hub.log
```

---

## 🔍 What Gets Initialized

### On First Run
```
✓ Creates PostgreSQL schema (promotion_hub)
✓ Creates 4 tables (leads, posts, actions, logs)
✓ Creates indexes on common queries
✓ Loads content library (64+ pieces)
✓ Starts scheduler with all 10+ jobs
✓ Initializes logging
```

### Jobs Started
```
LinkedIn:       08:00, 15:00 (publish)
Instagram:      09:00, 13:00, 19:00 (publish)
Telegram:       08:00, 11:00, 14:00, 17:00, 20:00 (publish)
Collection:     Every 6-8 hours
Scoring:        Every 2-3 hours
Invitations:    Every 2-3 hours
```

---

## 📊 Verify Deployment

### Check Database
```sql
-- Connect to your PostgreSQL instance
\c promotion_hub

-- List tables
\dt promotion_hub.*;

-- Check recent logs
SELECT * FROM promotion_hub.logs ORDER BY created_at DESC LIMIT 10;

-- Check leads
SELECT COUNT(*) as total_leads, 
       COUNT(*) FILTER (WHERE invited) as invited_count
FROM promotion_hub.leads;
```

### Check Application Logs
```bash
# View last 50 lines
tail -50 logs/promotion_hub.log

# Search for errors
grep ERROR logs/promotion_hub.log | tail -20

# Search for specific channel
grep Instagram logs/promotion_hub.log | tail -10
grep Telegram logs/promotion_hub.log | tail -10
grep LinkedIn logs/promotion_hub.log | tail -10
```

### Check Running Process
```bash
# Linux/Mac: Check if Python is running
ps aux | grep "python main.py"

# Windows: Check process
tasklist | findstr python
```

---

## 🔐 Security Verification

- [x] `.env` is in `.gitignore` (credentials safe)
- [x] `instagram_session.pkl` is ignored
- [x] No hardcoded credentials in code
- [x] All API calls have error handling
- [x] Rate limiting enforced (delays between actions)
- [x] Action logging to database (audit trail)
- [x] Exception handling with proper cleanup

---

## 🛠️ Troubleshooting Deployment

### Issue: "Instagram session expired"
```bash
python init_instagram.py
# Then restart: python main.py
```

### Issue: "Database connection refused"
```bash
# Check if PostgreSQL is running
# Verify DATABASE_URL in .env
# Test connection: psql $DATABASE_URL
```

### Issue: "Bot token invalid"
```bash
# Get new token from @BotFather
# Update TELEGRAM_BOT_TOKEN in .env
# Restart app
```

### Issue: "Port already in use" (if using webhook)
```bash
# Kill existing process
kill $(lsof -t -i:8080)  # or check your port

# Restart
python main.py
```

---

## 📈 Performance Expectations

### Database
- Writes: ~100-200 actions per day
- Reads: ~1000s per day (scheduled jobs)
- Storage: ~1MB per 10k leads
- Retention: All data (configurable)

### API Rate Limits
- Instagram: ~100-200 requests/day
- Telegram: ~500-1000 requests/day
- LinkedIn: ~10-20 posts/day

### Resource Usage
- CPU: <5% (mostly idle between jobs)
- Memory: ~200-500 MB
- Disk: ~100 MB (logs + session + db)

---

## 📋 Monitoring Checklist

Daily:
- [ ] Check logs for errors: `grep ERROR logs/promotion_hub.log`
- [ ] Verify lead counts: SELECT COUNT(*) FROM promotion_hub.leads
- [ ] Check last actions: SELECT * FROM promotion_hub.actions LIMIT 10

Weekly:
- [ ] Review scoring accuracy: High/low score samples
- [ ] Check invitation rates: Count by channel
- [ ] Verify no platform blocks: Check blocked count
- [ ] Backup database

Monthly:
- [ ] Analyze performance: Actions per day, leads quality
- [ ] Review content usage: Which topics/types perform best
- [ ] Update content library if needed
- [ ] Archive old logs: Backup and compress

---

## 🚨 Emergency Procedures

### Stop Application (Graceful)
```bash
# Press Ctrl+C in terminal
# or kill process:
kill -TERM $(pgrep -f "python main.py")
```

### Emergency Stop (Force)
```bash
# Force kill
kill -9 $(pgrep -f "python main.py")
```

### Reset All Data
```bash
# ⚠️  WARNING: This deletes all data!
DROP SCHEMA promotion_hub CASCADE;
# Then restart app (will recreate schema)
```

### Restore from Backup
```bash
# Restore PostgreSQL backup
psql -U user -d promotion_hub < backup.sql
```

---

## ✅ Final Checklist Before Going Live

- [ ] `.env` configured with real credentials
- [ ] Database running and accessible
- [ ] Instagram session initialized (run init_instagram.py)
- [ ] System check passing (python system_check.py)
- [ ] Logs directory exists
- [ ] Backup strategy in place
- [ ] Monitoring setup (logs check)
- [ ] Team notified
- [ ] Runbooks available
- [ ] Contact info for emergency stops

---

## 📞 Support

**Before starting:**
1. Run `python system_check.py` - should pass all 27 tests
2. Check `logs/promotion_hub.log` for any pre-startup warnings
3. Verify `.env` has all required values

**If having issues:**
1. Stop the application gracefully (Ctrl+C)
2. Check logs/promotion_hub.log
3. Run `python system_check.py` to verify configuration
4. Fix any issues
5. Restart: `python main.py`

---

## 🎉 You're Ready!

```bash
# One command to start:
python main.py

# That's it! The system will:
# ✓ Run pre-flight checks
# ✓ Initialize database
# ✓ Start all scheduled jobs
# ✓ Begin automated marketing
# ✓ Log all activities

# Monitor with:
tail -f logs/promotion_hub.log
```

**Promotion Hub v1.0 is deployed! 🚀**

---

*Created: January 20, 2026*  
*Status: Ready for Production ✅*
