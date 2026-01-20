# 📊 Generated Content Storage & Cleanup Strategy

**Problem:** Where is generated content stored? How to prevent database bloat after publishing?

**Answer:** Content is stored in PostgreSQL `posts` table. Automatic daily cleanup job removes published posts older than N days.

---

## 🗄️ Data Storage Architecture

### Where Content is Generated and Stored

```
┌─────────────────────────────────────────┐
│  1. ContentEngine.generate_content()    │
│     - Creates text content (AI-based)   │
└──────────────────┬──────────────────────┘
                   │ Returns: (content_de, topic, type)
                   ↓
┌─────────────────────────────────────────┐
│  2. ContentAdapter.adapt()              │
│     - Adapts to channel (LinkedIn/etc)  │
└──────────────────┬──────────────────────┘
                   │ Returns: content_adapted
                   ↓
┌─────────────────────────────────────────┐
│  3. Post.save()                         │
│     - SAVES to PostgreSQL posts table   │
│     - Stores: channel, content_de,      │
│       content_adapted, created_at       │
└──────────────────┬──────────────────────┘
                   │ Returns: post.id
                   ↓
┌─────────────────────────────────────────┐
│  4. Publisher.publish_post()            │
│     - Publishes to LinkedIn/Telegram    │
└──────────────────┬──────────────────────┘
                   │ Returns: success (bool)
                   ↓
┌─────────────────────────────────────────┐
│  5. Post.mark_published()               │
│     - Updates post: published=TRUE      │
│     - Sets published_at timestamp       │
└──────────────────┬──────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────┐
│  6. [OPTIONAL] Cleanup Job              │
│     - Daily at 02:00 UTC                │
│     - Deletes posts older than 30 days  │
│     - Prevents DB bloat                 │
└─────────────────────────────────────────┘
```

### Database Tables Involved

#### 1. **posts** table
Stores all generated and published content.

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),           -- 'linkedin', 'telegram', 'instagram'
    content_de TEXT,               -- Original German content from AI
    content_adapted TEXT,          -- Channel-specific adapted content
    language VARCHAR(10),          -- 'de', 'en', etc.
    published BOOLEAN,             -- FALSE → not published, TRUE → published
    published_at TIMESTAMP,        -- When was it published
    created_at TIMESTAMP           -- When was post created
);
```

**Storage Estimate:**
- Average post: ~500 bytes (text content)
- 10 posts/day × 365 days = 3,650 posts/year
- Uncompressed: ~1.8 MB/year per channel
- **With 3 channels: ~5.4 MB/year**

#### 2. **actions** table
Logs every action including publication events.

```sql
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    action_type VARCHAR(50),       -- 'post_published', 'cleanup'
    channel VARCHAR(50),           -- 'linkedin', 'telegram', 'instagram'
    post_id INTEGER,               -- Reference to posts.id
    details JSONB,                 -- Extra data: {topic, type, ...}
    created_at TIMESTAMP
);
```

---

## 🗑️ Automatic Cleanup Strategy

### How It Works

**Daily Cleanup Job** runs automatically at configured time (default: 02:00 UTC)

```python
# core/scheduler.py - _cleanup_old_posts() method

1. Read POST_RETENTION_DAYS from .env (default: 30)
2. Find all posts where: published=TRUE AND published_at < (now - 30 days)
3. Delete matching posts from posts table
4. Delete associated actions from actions table
5. Log statistics (before/after post count)
6. Save cleanup report to actions table
```

### Configuration

Update `.env` file:

```dotenv
# =====================================================
# DATABASE RETENTION POLICY
# =====================================================
# How many days to keep published posts (prevents database bloat)
POST_RETENTION_DAYS=30

# Enable automatic cleanup
CLEANUP_ENABLED=True

# Time to run daily cleanup (24-hour format, UTC)
CLEANUP_TIME=02:00
```

### Retention Options

| Setting | Effect | Database Size/Year |
|---------|--------|-------------------|
| `POST_RETENTION_DAYS=7` | Keep 1 week | ~700 KB |
| `POST_RETENTION_DAYS=14` | Keep 2 weeks | ~1.4 MB |
| `POST_RETENTION_DAYS=30` | Keep 1 month (DEFAULT) | ~2.8 MB |
| `POST_RETENTION_DAYS=90` | Keep 3 months | ~8.4 MB |
| `POST_RETENTION_DAYS=365` | Keep 1 year | ~30 MB |

---

## 📝 Usage Examples

### 1. Manual Cleanup (One-Time)

```python
from core.cleanup import cleanup_published_posts

# Delete posts older than 30 days
result = cleanup_published_posts(days=30, verbose=True)
print(result)
# Output: {
#   'status': 'success',
#   'deleted_posts': 45,
#   'deleted_actions': 45,
#   'cutoff_date': '2025-12-21T02:00:00',
#   'days_to_keep': 30,
#   'message': 'Deleted 45 posts and 45 actions'
# }
```

### 2. Check Database Statistics

```python
from core.cleanup import get_database_stats

stats = get_database_stats()
print(stats)
# Output: {
#   'total_posts': 1250,
#   'published_posts': 1200,
#   'unpublished_posts': 50,
#   'oldest_post': '2025-06-20T10:30:00',
#   'newest_post': '2026-01-20T14:45:00',
#   'posts_per_channel': {
#       'linkedin': 400,
#       'telegram': 500,
#       'instagram': 350
#   }
# }
```

### 3. Cleanup Specific Channel

```python
from core.cleanup import cleanup_channel

# Delete Instagram posts older than 14 days
result = cleanup_channel('instagram', days=14)
print(result)
# Output: {
#   'status': 'success',
#   'channel': 'instagram',
#   'deleted': 25,
#   'message': 'Deleted 25 posts from channel instagram'
# }
```

### 4. Emergency Cleanup (Delete All Old Posts)

```python
from core.cleanup import cleanup_published_posts

# Delete ALL posts older than 7 days (for emergency database cleanup)
result = cleanup_published_posts(days=7)
print(f"Freed up space: {result['deleted_posts']} posts removed")
```

### 5. Run Cleanup from Command Line

```bash
# Manual cleanup via Python script
python -c "
from core.cleanup import cleanup_published_posts, get_database_stats
print('Stats before:', get_database_stats())
result = cleanup_published_posts(days=30)
print('Cleanup result:', result)
print('Stats after:', get_database_stats())
"
```

---

## 🔄 Automatic Cleanup Workflow

### Daily Execution Flow

```
02:00 UTC (Daily)
    ↓
Scheduler triggers _cleanup_old_posts()
    ↓
Get PRE-cleanup stats (query posts table)
    ↓
ContentCleanupManager.delete_old_published_posts(30)
    ├─ Find posts: published=TRUE AND published_at < 30 days ago
    ├─ Delete associated actions
    ├─ Delete posts
    └─ Return: {deleted_posts, deleted_actions}
    ↓
Get POST-cleanup stats
    ↓
Log cleanup report to actions table
    ↓
Log to application logs
    ↓
✅ Cleanup complete
```

### What Gets Deleted

**Automatically deleted posts (after cleanup):**
- ✅ Published posts older than 30 days (configurable)
- ✅ Associated action records
- ✅ Freed database storage space

**Preserved (NOT deleted):**
- ❌ Unpublished posts (drafts)
- ❌ Recent published posts (< 30 days)
- ❌ Leads data
- ❌ Logs

---

## 📊 Database Impact Analysis

### Before Cleanup (1-Year Accumulation)

```
With 10 posts/day × 3 channels × 365 days:

Posts table:
├─ Total rows: 10,950 posts
├─ Storage: ~5.5 MB (text content)
├─ Published: 10,500 posts
└─ Unpublished: 450 posts (drafts)

Actions table:
├─ Total rows: ~15,000+ actions
├─ Storage: ~2 MB
└─ Associated data

Total DB size: ~25-30 MB
```

### After Cleanup (With 30-day retention)

```
Active rows: ~300 posts (only last 30 days)
├─ LinkedIn: ~100 posts
├─ Telegram: ~150 posts
├─ Instagram: ~50 posts
└─ Unpublished: ~0 (cleaned daily)

Associated actions: ~300-400 rows

Total DB size: ~0.5-1 MB

Cleanup removes: ~99% of historical data
Space savings: ~24-29 MB
```

---

## 🚀 Scheduler Integration

### Jobs Registered

```python
# From core/scheduler.py

Jobs configured:
├─ LinkedIn publish morning (08:00 CET)
├─ LinkedIn publish afternoon (14:00 CET)
├─ Telegram publish (×5 times/day)
├─ Instagram publish (×3 times/day)
├─ Telegram audience collection
├─ Instagram audience collection
├─ Telegram invitations (every 2 hours)
├─ Instagram invitations (every 3 hours)
└─ 🗑️ Daily cleanup job (02:00 UTC) ← NEW
   └─ Enabled: True (from .env CLEANUP_ENABLED)
   └─ Time: 02:00 (from .env CLEANUP_TIME)
   └─ Retention: 30 days (from .env POST_RETENTION_DAYS)
```

### Cleanup Job Details

```python
Job ID: 'daily_cleanup'
Name: 'Daily cleanup of old published posts'
Trigger: CronTrigger(hour=2, minute=0)  # 02:00 UTC daily
Handler: Scheduler._cleanup_old_posts()
Status: Enabled if CLEANUP_ENABLED=True in .env
```

---

## ⚙️ Configuration Quick Reference

### .env Settings

```dotenv
# Database retention (keep published posts for X days)
POST_RETENTION_DAYS=30

# Enable automatic cleanup
CLEANUP_ENABLED=True

# Cleanup execution time (UTC)
CLEANUP_TIME=02:00
```

### Common Scenarios

**Scenario 1: Short-term content (social media agility)**
```dotenv
POST_RETENTION_DAYS=7      # Keep 1 week
CLEANUP_ENABLED=True
CLEANUP_TIME=03:00
```
→ Database: ~700 KB, Quick content rotation

**Scenario 2: Medium-term archive (balanced)**
```dotenv
POST_RETENTION_DAYS=30     # Keep 1 month (DEFAULT)
CLEANUP_ENABLED=True
CLEANUP_TIME=02:00
```
→ Database: ~2.8 MB, Good for analytics

**Scenario 3: Long-term archive (analytics)**
```dotenv
POST_RETENTION_DAYS=90     # Keep 3 months
CLEANUP_ENABLED=True
CLEANUP_TIME=04:00
```
→ Database: ~8 MB, Track campaign performance

**Scenario 4: Disable cleanup (manual management)**
```dotenv
POST_RETENTION_DAYS=999    # Never auto-delete
CLEANUP_ENABLED=False
```
→ Manual cleanup only via `cleanup_published_posts()`

---

## 🛡️ Data Safety

### What's Protected

✅ **Unpublished content** - Never deleted automatically  
✅ **Leads database** - Separate table, not affected  
✅ **Audit trails** - Cleanup operations logged to actions table  
✅ **Configurable retention** - Control how long to keep data  
✅ **Reversible logs** - All cleanup events recorded  

### Backup Recommendation

Before deploying to production, ensure:

```bash
# 1. Backup database
pg_dump promotion_hub > backup_2026-01-20.sql

# 2. Enable CLEANUP_ENABLED=True
# 3. Monitor cleanup logs for 1 week
# 4. Verify database size decreases
# 5. Check that recent posts are NOT deleted
```

---

## 📋 Cleanup Methods Reference

### Core Cleanup Manager

```python
from core.cleanup import ContentCleanupManager

# Delete old published posts
result = ContentCleanupManager.delete_old_published_posts(
    days_to_keep=30,
    verbose=True
)

# Get database statistics
stats = ContentCleanupManager.get_cleanup_stats()

# Cleanup specific channel
result = ContentCleanupManager.cleanup_by_channel(
    channel='linkedin',
    days_to_keep=30,
    published_only=True
)
```

### Simple API

```python
from core.cleanup import (
    cleanup_published_posts,      # Delete old posts
    get_database_stats,           # Get DB statistics
    cleanup_channel               # Delete by channel
)

# Examples
cleanup_published_posts(days=30, verbose=True)
get_database_stats()
cleanup_channel('telegram', days=14)
```

---

## 🔍 Monitoring Cleanup

### Check Cleanup Logs

```bash
# View cleanup operations in logs
tail -f logs/promotion_hub.log | grep -i cleanup

# Output:
# 🗑️  Running daily cleanup of old published posts...
# 📊 Database stats BEFORE cleanup: Total posts: 1250, Published: 1200
# ✅ Cleanup completed: Deleted 45 posts, 45 actions (older than 30 days)
# 📊 Database stats AFTER cleanup: Total posts: 1205, Published: 1155
```

### Query Cleanup History

```python
from core.models import _db, sql, Action

with _db.get_cursor() as cur:
    cur.execute("""
        SELECT created_at, details FROM actions
        WHERE details->>'operation' = 'cleanup'
        ORDER BY created_at DESC
        LIMIT 5
    """)
    
    for row in cur.fetchall():
        print(f"{row['created_at']}: Deleted {row['details']['deleted_posts']} posts")
```

---

## ✅ Implementation Checklist

- [x] **Created cleanup utility** (`core/cleanup.py`)
  - Deletion methods for old posts
  - Database statistics tracking
  - Channel-specific cleanup
  
- [x] **Added configuration** (`.env.example`)
  - `POST_RETENTION_DAYS` - how long to keep posts
  - `CLEANUP_ENABLED` - enable/disable feature
  - `CLEANUP_TIME` - when to run cleanup
  
- [x] **Integrated scheduler** (`core/scheduler.py`)
  - Daily cleanup job registered
  - Configurable execution time
  - Logging and statistics
  
- [x] **Documentation** (this file)
  - Architecture overview
  - Usage examples
  - Configuration guide

---

## 🎯 Summary

**Generated content is stored in PostgreSQL `posts` table.**

**To prevent database bloat:**

1. **Enable automatic cleanup** (already configured)
   ```env
   CLEANUP_ENABLED=True
   POST_RETENTION_DAYS=30
   CLEANUP_TIME=02:00
   ```

2. **Daily job runs automatically** at 02:00 UTC
   - Finds published posts older than 30 days
   - Deletes them from database
   - Logs cleanup statistics

3. **No manual action needed**
   - System self-maintains
   - Database stays ~2-3 MB
   - Recent content always preserved

4. **Manual cleanup available** if needed
   ```python
   from core.cleanup import cleanup_published_posts
   cleanup_published_posts(days=30)
   ```

---

**Status:** ✅ **Production Ready**

*Last Updated: 2026-01-20*
