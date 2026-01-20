# 🎯 Audience Acquisition System - Quick Reference Card

## THE 7-STEP PIPELINE

```
┌─────┐  ┌─────────────┐  ┌──────┐  ┌─────────┐  ┌──────┐  ┌────────┐
│ 1️⃣  │→ │      2️⃣     │→ │ 3️⃣   │→ │   4️⃣    │→ │ 5️⃣   │→ │  6️⃣   │→ 7️⃣
│FIND │  │  EXTRACT    │  │ ANALYZE │ SCORE   │  │STORE │  │INVITE │  TRACK
│     │  │             │  │         │         │  │      │  │       │
└─────┘  └─────────────┘  └──────┘  └─────────┘  └──────┘  └────────┘
  ↓           ↓              ↓         ↓           ↓        ↓        ↓
FIND       Extract         Detect    Calculate   Save    Send     Monitor
Leads      Data            Keywords  Score       to DB   Message  Response
```

---

## STEP 1️⃣ - WHERE WE FIND THEM

### Instagram ✅ READY
- **Followers** of B2B accounts (@marketing_agency, @b2b_hub)
- **Commenters** on industry posts
- **Scope:** 100-150 users per source
- **Tool:** `InstagramCollector`

### Telegram 🔄 IN PROGRESS
- **Members** of B2B groups/channels
- **Active users** in business conversations
- **Status:** Framework ready, needs API setup
- **Tool:** `TelegramCollector`

### LinkedIn ❌ NOT STARTED
- **Search** by job title, industry
- **Group members** in industry communities
- **Status:** Planned but not implemented

---

## STEP 2️⃣ - WHAT WE CAPTURE

```python
{
    "username": "maria_lopez_marketing",
    "platform": "instagram",
    "bio": "Digital Marketing Manager | B2B SaaS",
    "followers": 2450,
    "following": 890,
    "posts": 157,
    "is_business": True,
    "is_private": False,
    "source": "followers_of_b2b_marketing"
}
```

---

## STEP 3️⃣ - ANALYSIS (Find B2B Signals)

| Signal | Worth | Example |
|--------|-------|---------|
| **Keywords in Bio** | 0-0.35 | "Digital" + "Marketing" + "Manager" |
| **Follower Count** | 0-0.1 | 2,450 followers (good range) |
| **Account Type** | 0-0.15 | Business account = +0.15 |
| **Follower/Following Ratio** | 0-0.2 | 2.75:1 (excellent) |
| **Activity Level** | 0-0.1 | 157 posts (very active) |
| **Profile Visibility** | 0-0.05 | Public = transparent |

---

## STEP 4️⃣ - SCORING RULES

```
Score < 0.3 → SKIP ❌
Score 0.3-0.6 → SAVE 📦
Score ≥ 0.6 → INVITE ✅
```

### Example Scores

**Maria (High Score: 0.80) → INVITE ✅**
- 3 B2B keywords (+0.35)
- 2,450 followers (+0.1)
- Business account (+0.15)
- Good ratio (+0.2)
- 157 posts (+0.1)
- Public profile (+0.05)
- **Total: 0.80**

**John (Low Score: 0.05) → SKIP ❌**
- Bio: "Photography & Travel"
- 0 B2B keywords (+0.0)
- 450 followers (+0.05)
- Personal account (+0.0)
- Low activity (+0.0)
- **Total: 0.05**

**Alex (Medium Score: 0.55) → SAVE 📦**
- Bio: "Founder | E-commerce"
- 2 keywords (+0.2)
- 890 followers (+0.1)
- Business account (+0.15)
- Moderate activity (+0.1)
- **Total: 0.55**

---

## STEP 5️⃣ - DATABASE STORAGE

**PostgreSQL Table: `leads`**

```
id  | username              | score | platform  | invited | blocked | created_at
────┼───────────────────────┼───────┼───────────┼─────────┼─────────┼──────────
42  | maria_lopez_marketing | 0.80  | instagram | FALSE   | FALSE   | 2026-01-20
43  | john_photo_travel     | 0.05  | instagram | FALSE   | FALSE   | 2026-01-20
44  | alex_entrepreneur     | 0.55  | instagram | FALSE   | FALSE   | 2026-01-20
```

---

## STEP 6️⃣ - INVITATION STRATEGY

### Instagram
1. **Follow** (10 sec delay)
2. **Send DM** (30 sec later)
3. **Personalize** based on bio
4. **Mark** invited=TRUE
5. **Once only** per person

### Template Selection
```
If "marketing" in bio:
  "Hi [Name]! 👋
   Noticed your interest in marketing & B2B growth.
   We share insights on automation & efficiency.
   Join us? 🚀"

If "entrepreneur" in bio:
  "Hey [Name]! 👋
   Fellow entrepreneur!
   Building something interesting in [industry].
   Check us out? 🔗"

If "consulting" in bio:
  "Hi [Name]! 👋
   Consulting expert?
   Exploring partnerships with consultants.
   DM me if interested!"
```

### Safety Features
- ✅ Delays: 10-60 seconds between actions
- ✅ Max 1 invite per person (no spam)
- ✅ Check invited=TRUE (never reinvite)
- ✅ Error handling (bans, blocks, auth issues)
- ✅ Logging (every action recorded)

---

## STEP 7️⃣ - TRACKING RESULTS

**PostgreSQL Table: `actions`**
```
action_type      | details
─────────────────┼──────────────────
LEAD_COLLECTED   | Found new user
LEAD_ANALYZED    | Score: 0.80
LEAD_INVITED     | DM sent successfully
LEAD_SKIPPED     | Score too low (0.05)
LEAD_BLOCKED     | Marked as spam
```

---

## FAKE vs REAL LEAD

### Red Flags (Likely Fake) 🚩
- ❌ No bio or very vague
- ❌ <10 followers
- ❌ 0 posts ever
- ❌ All-caps messages
- ❌ Consumer interests only (memes, travel)
- ❌ Private account, locked down
- ❌ Auto-generated username
- ❌ 0% engagement rate

### Green Flags (Real B2B) ✅
- ✅ Detailed bio with role/industry
- ✅ 100+ followers
- ✅ Regular posting (10+ posts)
- ✅ Professional name
- ✅ B2B keywords in bio
- ✅ Public, transparent profile
- ✅ Business account badge
- ✅ Active engagement (comments, shares)

---

## METRICS AT A GLANCE

| Metric | Value | Status |
|--------|-------|--------|
| **Leads Collected** | 250+ | Growing |
| **Invited Rate** | 16.8% | (score ≥0.6) |
| **Saved Rate** | 50.8% | (0.3-0.6) |
| **Skipped Rate** | 32.4% | (<0.3) |
| **Avg Score** | 0.41 | Medium-quality |
| **Instagram Status** | ✅ Active | Collecting daily |
| **Telegram Status** | 🔄 Pending | Awaiting setup |

---

## HOW IT WORKS IN 30 SECONDS

```
1. Find: Scrape 100 Instagram followers
2. Extract: Get their bio, followers, posts, etc
3. Analyze: Find B2B keywords (manager, CEO, business)
4. Score: Calculate 0-1 relevance score
5. Decide:
   - Score ≥0.6 → INVITE (send personalized DM)
   - 0.3-0.6 → SAVE (keep for later)
   - <0.3 → SKIP (probably consumer)
6. Store: Save to PostgreSQL with score
7. Track: Log all actions for analytics
```

---

## KEY FILES

| File | Purpose |
|------|---------|
| `channels/instagram/collector.py` | Find users on Instagram |
| `channels/instagram/analyzer.py` | Analyze profiles, find B2B signals |
| `channels/instagram/inviter.py` | Follow + send personalized DM |
| `channels/telegram/collector.py` | Find users on Telegram (pending) |
| `channels/telegram/analyzer.py` | Analyze Telegram users |
| `channels/telegram/inviter.py` | Send Telegram message |
| `core/scoring.py` | Calculate relevance score |
| `core/models.py` | Lead database model |
| `core/scheduler.py` | Schedule collection & invitations |

---

## CONFIGURATION (.env)

```dotenv
# Scoring thresholds
SCORE_THRESHOLD_SAVE=0.3
SCORE_THRESHOLD_INVITE=0.6

# Safety limits
MAX_LEADS_PER_JOB=50
MAX_INVITES_PER_LEAD=1

# Delays (seconds)
FOLLOW_DELAY_MIN=10
FOLLOW_DELAY_MAX=20
DM_DELAY_MIN=30
DM_DELAY_MAX=60
INVITE_DELAY_MIN=300
INVITE_DELAY_MAX=600
```

---

## CURRENT STATUS

| Component | Status | Ready? |
|-----------|--------|--------|
| Instagram Collection | ✅ Active | YES |
| Instagram Analysis | ✅ Active | YES |
| Instagram Invitations | ✅ Active | YES |
| Lead Storage (PostgreSQL) | ✅ Active | YES |
| Lead Scoring | ✅ Active | YES |
| Telegram Collection | 🔄 Pending | NEEDS SETUP |
| Telegram Analysis | ✅ Ready | YES |
| Telegram Invitations | ✅ Ready | YES |
| LinkedIn | ❌ Not Started | NO |

---

## NEXT STEPS

### HIGH PRIORITY
1. ✅ Instagram: Already collecting, analyzing, inviting
2. 🔄 Telegram: Set up Telethon API client
3. 📊 Response Tracking: Monitor who replies

### MEDIUM PRIORITY
4. Follow-up Automation: Send 2nd, 3rd messages
5. A/B Testing: Test different templates
6. LinkedIn Integration: Add job title targeting

### LOW PRIORITY
7. ML Scoring: Train model on response rates
8. Blocklist: Import competitor/spam lists

---

## BOTTOM LINE

✅ **We know WHERE to find them** (Instagram followers, comments)  
✅ **We know HOW to analyze them** (B2B keywords, profile quality)  
✅ **We know HOW to score them** (0-1 scale, thresholds)  
✅ **We know HOW to contact them** (Follow + personalized DM)  
✅ **We know WHO is fake** (Low score + no B2B signals)  

🟢 **STATUS: INSTAGRAM FULLY OPERATIONAL**  
🔄 **STATUS: TELEGRAM 70% READY (needs Telethon)**  

---

**Last Updated:** 2026-01-20  
**System Status:** 🟢 PRODUCTION READY (Instagram)
