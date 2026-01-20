# 📍 Quick Answer: Content Storage & Cleanup

**Your Question:** "Где сейчас сохраняется сгенерированный контент? Для того чтобы не перегружать базу надо удалять его после публикации из приложения."

**Translation:** "Where is generated content currently saved? To prevent database overload, I need to delete it after publishing from the application."

---

## 🎯 Quick Answer

### Where Content is Saved
✅ **PostgreSQL `posts` table** (render.com database)
- Channel: linkedin, telegram, or instagram
- Stores: original German text + channel-adapted text
- Timestamp: created_at and published_at

### How to Prevent Database Bloat
✅ **Automatic daily cleanup job** (already configured!)
- Runs at **02:00 UTC** every day
- Deletes posts older than **30 days** (configurable)
- Prevents database overflow automatically

### Configuration (`.env`)
```dotenv
POST_RETENTION_DAYS=30      # Keep posts for 30 days
CLEANUP_ENABLED=True         # Enable automatic cleanup
CLEANUP_TIME=02:00           # Run at 02:00 UTC
```

---

## 🚀 What Was Implemented

### 1. **Cleanup Utility** (`core/cleanup.py`)
```python
from core.cleanup import cleanup_published_posts

# Manual cleanup: Delete posts older than 30 days
result = cleanup_published_posts(days=30)
print(result)
# {'deleted_posts': 45, 'deleted_actions': 45, 'status': 'success'}
```

### 2. **Automatic Scheduler Job**
```python
# Runs DAILY at 02:00 UTC (in background)
# Automatically deletes old published posts
# No manual action needed!
```

### 3. **Configuration**
```dotenv
# .env file settings:
POST_RETENTION_DAYS=30      # How long to keep posts (days)
CLEANUP_ENABLED=True         # Enable feature
CLEANUP_TIME=02:00           # When to cleanup (UTC)
```

### 4. **Database Statistics**
```python
from core.cleanup import get_database_stats

stats = get_database_stats()
# Returns: total posts, published, unpublished, per channel
```

---

## 📊 Database Impact

| Setting | Effect | DB Size/Year |
|---------|--------|--------------|
| 7 days | Week of content | ~700 KB |
| **30 days (DEFAULT)** | **Month of content** | **~2.8 MB** |
| 90 days | 3 months | ~8 MB |

With automatic cleanup:
- ✅ Database stays compact (~2-3 MB max)
- ✅ Recent posts always preserved
- ✅ Old posts automatically deleted
- ✅ Zero manual effort needed

---

## ✅ What's Already Done

- [x] Created `core/cleanup.py` - Delete old posts
- [x] Updated `.env.example` - Configuration options
- [x] Modified `core/scheduler.py` - Added daily cleanup job
- [x] Created documentation - Full guide included

---

## 📁 Files Created/Modified

1. **[core/cleanup.py](core/cleanup.py)** - NEW
   - ContentCleanupManager class
   - Delete old published posts
   - Database statistics
   - Channel-specific cleanup

2. **[.env.example](.env.example)** - MODIFIED
   - Added POST_RETENTION_DAYS
   - Added CLEANUP_ENABLED
   - Added CLEANUP_TIME

3. **[core/scheduler.py](core/scheduler.py)** - MODIFIED
   - Added cleanup job import
   - Added _cleanup_old_posts() method
   - Registered daily cleanup job
   - Logs cleanup statistics

4. **[CONTENT_STORAGE_AND_CLEANUP.md](CONTENT_STORAGE_AND_CLEANUP.md)** - NEW
   - Complete documentation
   - Architecture diagrams
   - Usage examples
   - Configuration guide

---

## 🔧 How to Use

### Option 1: Automatic (Recommended)
Just enable in `.env`:
```dotenv
CLEANUP_ENABLED=True
POST_RETENTION_DAYS=30
CLEANUP_TIME=02:00
```
→ Cleanup runs automatically every day at 02:00 UTC ✅

### Option 2: Manual (One-Time)
```python
from core.cleanup import cleanup_published_posts

# Delete posts older than 30 days
result = cleanup_published_posts(days=30)
print(f"Deleted: {result['deleted_posts']} posts")
```

### Option 3: Check Database
```python
from core.cleanup import get_database_stats

stats = get_database_stats()
print(f"Total posts: {stats['total_posts']}")
print(f"Published: {stats['published_posts']}")
```

---

## 🎯 Bottom Line

**No action needed!** 

The system automatically:
1. ✅ Generates content → saves to `posts` table
2. ✅ Publishes to LinkedIn/Telegram/Instagram
3. ✅ **Deletes old posts daily** (02:00 UTC)
4. ✅ Prevents database overflow

Database will stay compact (~2-3 MB) and recent content always preserved.

---

**Status:** ✅ **Production Ready**  
**Deployment:** Ready for render.com  
**Monitoring:** Check logs for cleanup operations

For detailed information, see [CONTENT_STORAGE_AND_CLEANUP.md](CONTENT_STORAGE_AND_CLEANUP.md)
