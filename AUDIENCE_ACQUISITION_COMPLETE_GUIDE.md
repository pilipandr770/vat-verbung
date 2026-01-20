# 🎯 Audience Search, Filtering & Invitation System - Complete Analysis

**Date:** January 20, 2026  
**Status:** Current Implementation Review  
**Question:** "Как мы ищем целевую аудиторию? Как мы их фильтруем и приглашаем?"

---

## 🗺️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AUDIENCE ACQUISITION PIPELINE                              │
│  (Search → Filter → Store → Analyze → Score → Invite)       │
└─────────────────────────────────────────────────────────────┘

STEP 1: DISCOVERY (Where We Find People)
├─ Telegram
│  ├─ Collect from public chats/channels
│  ├─ Source: messages, comments, participant lists
│  └─ Tool: TelegramCollector (via Telethon API)
│
├─ Instagram
│  ├─ Collect followers of similar accounts
│  ├─ Collect from post comments
│  ├─ Source: @B2B_competitors, @industry_leaders
│  └─ Tool: InstagramCollector (via instagrapi)
│
└─ LinkedIn (Future)
   ├─ Search by industry, job title, company
   ├─ Collect from group members
   └─ Tool: TBD

STEP 2: DATA EXTRACTION (What We Capture)
├─ User ID (platform-specific)
├─ Username / Email
├─ Bio / Profile description
├─ Follower count
├─ Following count / Network size
├─ Profile type (public/private/business)
├─ Activity level
└─ Source (where we found them)

STEP 3: ANALYSIS (Profile Deep-Dive)
├─ B2B Keyword Detection
│  └─ business, company, enterprise, ceo, founder, etc.
│
├─ Profile Completeness
│  ├─ Has bio
│  ├─ Number of posts
│  ├─ Follower/following ratio
│  └─ Account type (business vs personal)
│
├─ Activity Assessment
│  ├─ Engagement rate (comments, shares)
│  ├─ Posting frequency
│  └─ Audience interaction
│
└─ Tools: InstagramAnalyzer, TelegramAnalyzer

STEP 4: SCORING (Is This a Real Lead?)
├─ B2B Keyword Score: 0-0.4 points
│  └─ 3+ keywords: +0.4 | 2 keywords: +0.2 | 1 keyword: +0.1
│
├─ Profile Quality Score: 0-0.3 points
│  ├─ Followers: +0.1 (100-100K range)
│  ├─ Business account: +0.15
│  ├─ Good ratio: +0.2
│  └─ Engagement: +0.1
│
├─ Activity Score: 0-0.3 points
│  ├─ 10+ posts: +0.1
│  ├─ Active in B2B chats: +0.15
│  └─ Public profile: +0.05
│
└─ Tool: LeadScorer (0.0-1.0 scale)

STEP 5: DECISION THRESHOLDS
├─ Score ≥ 0.6 → INVITE
│  └─ High-confidence B2B lead, send personalized invitation
│
├─ 0.3 ≤ Score < 0.6 → SAVE
│  └─ Potential lead, store for future campaigns
│
└─ Score < 0.3 → SKIP
   └─ Low relevance, likely consumer/wrong audience

STEP 6: STORAGE (Where We Keep Them)
├─ PostgreSQL "leads" table
├─ Fields:
│  ├─ id (primary key)
│  ├─ platform (instagram, telegram, linkedin)
│  ├─ identifier (username)
│  ├─ email (if available)
│  ├─ bio (profile description)
│  ├─ score (0-1 relevance score)
│  ├─ invited (boolean)
│  ├─ blocked (boolean - for spam/unresponsive)
│  └─ created_at (timestamp)
│
└─ Status: Active, Invited, Blocked, Follow-up

STEP 7: INVITATION (How We Contact Them)
├─ Telegram
│  ├─ Method: Direct private message via Bot API
│  ├─ Delay: 5 minutes between messages
│  ├─ Personalization: Bio-based template selection
│  └─ Tool: TelegramInviter
│
├─ Instagram
│  ├─ Method 1: Follow user
│  ├─ Method 2: Send 1 personalized DM
│  ├─ Delay: 10 seconds (follows), 30 seconds (DMs)
│  ├─ Personalization: Based on bio
│  └─ Tool: InstagramInviter
│
└─ LinkedIn (Future)
   ├─ Connection request
   ├─ Personalized message
   └─ Follow-up strategy

STEP 8: TRACKING (Did It Work?)
├─ Mark lead as "invited" in database
├─ Log attempt in "actions" table
├─ Track response/engagement
├─ Mark as "blocked" if spam complaint
└─ Schedule follow-ups
```

---

## 🔍 Detailed Breakdown

### STEP 1: AUDIENCE DISCOVERY

#### Telegram Collection
**File:** `channels/telegram/collector.py`

```python
class TelegramCollector:
    Methods:
    ├─ collect_from_chats(chat_ids: List[str]) → List[Dict]
    │  ├─ Requires: Telethon API client + user session
    │  ├─ Reads: Chat members, message senders, participant lists
    │  └─ Status: TODO - requires Telethon integration
    │
    ├─ collect_from_channels(channel_usernames: List[str]) → List[Dict]
    │  ├─ Target: Public B2B channels
    │  ├─ Extracts: Users from comments, message threads
    │  └─ Status: TODO - requires Telethon integration
    │
    └─ parse_message_for_leads(message_text) → Dict
       ├─ Finds: Email addresses, URLs, contact info
       └─ Returns: Contact data from message content
```

**Current Status:** Framework ready, needs Telethon client setup
- Requires: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, user session
- Reads: Public chats, channels, group membership lists
- Extracts: Usernames, emails, profile links

#### Instagram Collection
**File:** `channels/instagram/collector.py`

```python
class InstagramCollector:
    Methods:
    ├─ collect_from_similar_accounts(account_usernames)
    │  ├─ Input: ["@B2B_company", "@digital_marketing", "@startup_hub"]
    │  ├─ Extracts: Followers of these accounts (up to 100/account)
    │  ├─ Gets: username, user_id, bio, follower_count
    │  └─ Status: ✅ READY
    │
    ├─ collect_from_comments(post_ids)
    │  ├─ Input: Instagram media IDs
    │  ├─ Extracts: Users who commented on posts
    │  ├─ Gets: username, bio, profile info, comment text
    │  └─ Status: ✅ READY
    │
    └─ get_user_info(username)
       ├─ Gets: Full profile details
       └─ Status: ✅ READY
```

**Current Status:** ✅ FULLY IMPLEMENTED
- Uses: `instagrapi` library
- Authenticates: With real Instagram account
- Collects: 100-150 users per source
- Data: Complete profile information

---

### STEP 2: DATA EXTRACTION

**Example Lead Data (After Collection):**

```python
lead = {
    # Identifiers
    "platform": "instagram",
    "identifier": "maria_lopez_marketing",
    "username": "maria_lopez_marketing",
    "user_id": 1234567890,
    
    # Profile Info
    "bio": "Digital Marketing Manager | B2B SaaS | 5+ years experience | Strategy & Growth",
    "email": None,  # If found in bio
    
    # Metrics
    "follower_count": 2450,
    "following_count": 890,
    "media_count": 157,
    
    # Status
    "is_private": False,
    "is_business": True,
    
    # Source
    "source": "followers_of_b2b_marketing_agency",
    
    # Discovery
    "comment_text": "Great insights on marketing automation!"  # If from comments
}
```

---

### STEP 3: ANALYSIS (Profile Deep-Dive)

#### Instagram Analysis
**File:** `channels/instagram/analyzer.py`

```python
class InstagramAnalyzer:
    def analyze_profile(bio, follower_count, is_private, is_business):
        
        # Factor 1: B2B Keywords in Bio (+0-0.4)
        Keywords: "business", "company", "marketing", "manager",
                  "ceo", "founder", "solutions", "consulting"
        
        Example:
        - "Digital Marketing Manager | B2B SaaS"
          ├─ "Digital" ✓
          ├─ "Marketing" ✓
          ├─ "Manager" ✓
          └─ Score: +0.4 (3 keywords)
        
        # Factor 2: Profile Quality (+0-0.3)
        ├─ Follower count 100-100K: +0.1
        ├─ Ratio followers/following > 1.5: +0.2
        ├─ 10+ posts: +0.1
        ├─ Business account: +0.15
        └─ Public profile: +0.05
        
        # Factor 3: Activity Level
        ├─ Engagement indicators
        ├─ Post frequency
        └─ Community interaction
        
        Returns:
        {
            "score": 0.68,  # 0-1 scale
            "is_b2b": True,
            "recommendation": "INVITE",  # if score >= 0.6 AND B2B
            "reasons": [
                "Bio contains 3 B2B keywords",
                "Good follower/following ratio",
                "Business account"
            ]
        }
```

#### Telegram Analysis
**File:** `channels/telegram/analyzer.py`

```python
class TelegramAnalyzer:
    def analyze_user(username, bio, messages, chat_participation):
        
        # Same scoring logic as Instagram
        # Plus: Chat participation level
        
        # Factor 1: Bio Keywords (+0-0.4)
        # Factor 2: Message Content (+0-0.3)
        # Factor 3: Activity in B2B chats (+0-0.15)
        # Factor 4: Network size
        
        Returns: Same structure as Instagram
```

---

### STEP 4: SCORING & DECISION

**File:** `core/scoring.py`

```python
class LeadScorer:
    
    SCORE RANGES:
    ├─ 0.0 - 0.3  → SKIP (Low relevance, not our audience)
    ├─ 0.3 - 0.6  → SAVE (Potential lead, store for campaigns)
    └─ 0.6 - 1.0  → INVITE (High confidence B2B, send invitation)
    
    SCORING FACTORS:
    1. B2B Keywords: 0-0.35 points
       ├─ 3+ keywords: +0.35
       ├─ 2 keywords: +0.2
       ├─ 1 keyword: +0.1
       └─ 0 keywords: +0.0
    
    2. Message/Content Keywords: 0-0.25 points
       ├─ 3+ keywords: +0.25
       └─ 1-2 keywords: +0.15
    
    3. Profile Quality: 0-0.25 points
       ├─ Followers 100-100K: +0.1
       ├─ Good ratio: +0.1
       ├─ Business account: +0.1
       └─ Engagement: +0.1
    
    4. Activity Level: 0-0.15 points
       ├─ 10+ posts: +0.1
       ├─ Active in chats: +0.15
       └─ Public: +0.05
    
    EXAMPLE SCORES:
    
    Lead A: Maria (Marketing Manager)
    ├─ Bio keywords: 3 ("digital", "marketing", "manager") → +0.35
    ├─ Followers: 2,450 (good) → +0.1
    ├─ Business account: Yes → +0.15
    ├─ Engagement: Good ratio → +0.1
    ├─ Posts: 157 → +0.1
    └─ TOTAL: 0.8 → INVITE ✅
    
    Lead B: John (Consumer)
    ├─ Bio: "Photography enthusiast | Travel lover"
    ├─ Keywords: 0 → +0.0
    ├─ Followers: 450 → +0.05
    ├─ Business account: No → +0.0
    ├─ Engagement: Low → +0.0
    └─ TOTAL: 0.05 → SKIP ❌
    
    Lead C: Alex (Small Business Owner)
    ├─ Bio: "Founder | E-commerce | Learning growth hacking"
    ├─ Keywords: 2 ("Founder", "Business") → +0.2
    ├─ Followers: 890 → +0.1
    ├─ Business account: Yes → +0.15
    ├─ Activity: Moderate → +0.1
    └─ TOTAL: 0.55 → SAVE 📦
```

---

### STEP 5: STORAGE (PostgreSQL)

**Table Structure:**

```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    
    -- Identifiers
    source VARCHAR(100),           -- "followers_of_x", "comments_on_y"
    platform VARCHAR(50),          -- "instagram", "telegram", "linkedin"
    identifier VARCHAR(255),       -- username/email
    
    -- Profile Data
    email VARCHAR(255),            -- if available
    username VARCHAR(255),
    bio TEXT,                      -- full profile description
    
    -- Scoring
    score NUMERIC(3,3),            -- 0.000 to 1.000
    
    -- Status
    invited BOOLEAN DEFAULT FALSE, -- have we invited?
    blocked BOOLEAN DEFAULT FALSE, -- marked as spam/unresponsive?
    
    -- Timestamps
    created_at TIMESTAMP,
    
    -- Metadata (stored as JSON in some DBs)
    metadata JSONB,  -- follower_count, following_count, etc.
);

EXAMPLE RECORDS:
┌────┬─────────────────────────┬────────┬─────────────┬─────────┬────────┬────────┐
│ id │ identifier              │ source │ platform    │ score   │invited │blocked │
├────┼─────────────────────────┼────────┼─────────────┼─────────┼────────┼────────┤
│  1 │ maria_lopez_marketing   │ followers_of_x │ instagram │ 0.80   │  f     │  f    │
│  2 │ john_photos_travel      │ followers_of_x │ instagram │ 0.05   │  f     │  f    │
│  3 │ alex_entrepreneur       │ comments_on_1  │ instagram │ 0.55   │  f     │  f    │
│  4 │ spam_bot_123            │ followers_of_y │ instagram │ 0.10   │  t     │  t    │
│  5 │ b2b_agency              │ followers_of_z │ instagram │ 0.95   │  t     │  f    │
└────┴─────────────────────────┴────────┴─────────────┴─────────┴────────┴────────┘
```

**Current Database Count:**
- Total leads: Varies (depends on collection runs)
- By platform: Instagram (majority), Telegram (pending)
- By status: Active, Invited, Blocked

---

### STEP 6: INVITATION STRATEGY

#### Instagram Invitations
**File:** `channels/instagram/inviter.py`

```python
class InstagramInviter:
    
    TWO-STEP APPROACH:
    
    Step 1: FOLLOW USER
    ├─ Method: client.user_follow(user_id)
    ├─ Purpose: Get on their radar, show interest
    ├─ Delay: 10 seconds (natural behavior)
    └─ Goal: Non-intrusive first contact
    
    Step 2: SEND PERSONALIZED DM
    ├─ Method: client.send_message(user_id, text)
    ├─ Personalization: Based on bio
    ├─ Delay: 30 seconds after follow
    ├─ Content: Relevant to their interests
    └─ ONCE ONLY per person
    
    PERSONALIZATION TEMPLATES:
    
    If "marketing" in bio:
        "Hi [Name]! 👋
        I noticed your interest in marketing & B2B growth.
        
        We share insights on digital transformation, automation...
        Would love to connect! 🚀"
    
    If "entrepreneur" in bio:
        "Hey [Name]! 👋
        Fellow entrepreneur here! 
        
        We're building something interesting in [industry].
        Check us out? 🔗"
    
    If "consulting" in bio:
        "Hi [Name]! 👋
        Consulting expert? Nice!
        
        We're exploring partnerships with consultants...
        DM me if interested!"
    
    SAFETY MEASURES:
    ├─ MAX_INVITES_PER_LEAD=1 (no spam)
    ├─ Delay=30-60 seconds (natural timing)
    ├─ Check "invited" flag (never reinvite)
    ├─ Error handling (banned users, account issues)
    └─ Logging: Every action recorded
```

#### Telegram Invitations
**File:** `channels/telegram/inviter.py`

```python
class TelegramInviter:
    
    DIRECT APPROACH:
    ├─ Method: Bot sends private message
    ├─ Delay: 5 minutes between messages
    ├─ Personalization: Bio-based
    ├─ Requires: User ID (from Telegram)
    └─ Once only per person
    
    Similar personalization & safety measures as Instagram
```

---

### STEP 7: DECISION FLOW (COMPLETE EXAMPLE)

```
SCENARIO: Discovering Maria Lopez
═════════════════════════════════════

1. DISCOVERY
   Source: Instagram followers of @digital_marketing_agency
   Found: maria_lopez_marketing
   
2. DATA EXTRACTION
   ├─ username: maria_lopez_marketing
   ├─ bio: "Digital Marketing Manager | B2B SaaS Growth | 5+ years"
   ├─ followers: 2,450
   ├─ following: 890
   ├─ posts: 157
   ├─ business: True
   └─ private: False

3. ANALYSIS
   Bio Keywords:
   ├─ "Digital" → B2B keyword ✓
   ├─ "Marketing" → B2B keyword ✓
   ├─ "Manager" → B2B keyword ✓
   └─ Count: 3 keywords
   
   Profile Quality:
   ├─ Followers (2,450): Good ✓
   ├─ Ratio (2,450/890): 2.75 (Excellent) ✓
   ├─ Posts: 157 (Very active) ✓
   └─ Business account: Yes ✓

4. SCORING
   ├─ Bio keywords (3): +0.35
   ├─ Followers (good): +0.1
   ├─ Business account: +0.15
   ├─ Profile quality: +0.1
   ├─ Activity: +0.1
   └─ TOTAL SCORE: 0.80

5. DECISION
   Score: 0.80 ≥ 0.6
   Is B2B: YES
   Decision: ✅ INVITE

6. STORAGE
   INSERT INTO leads (
       platform='instagram',
       identifier='maria_lopez_marketing',
       source='followers_of_b2b_marketing',
       bio='Digital Marketing Manager | B2B SaaS...',
       score=0.80,
       invited=FALSE
   )

7. INVITATION
   ├─ Follow user: ✅ Done
   ├─ Wait 10 seconds
   ├─ Send DM: "Hi Maria! 👋 I noticed your interest in marketing..."
   ├─ Wait 30 seconds
   ├─ Mark as invited: UPDATE leads SET invited=TRUE
   └─ Log action: INSERT INTO actions (...)

8. TRACKING
   ├─ Invitation sent: Jan 20, 14:35
   ├─ Response: (pending)
   ├─ Follow-up: Schedule if no response
   └─ Mark as blocked if: Unfollow, report spam, delete message
```

---

## 📊 Current Implementation Status

### ✅ IMPLEMENTED & READY

| Component | Status | Details |
|-----------|--------|---------|
| **Instagram Collection** | ✅ READY | Followers, comments, user info |
| **Instagram Analysis** | ✅ READY | B2B keyword detection, scoring |
| **Instagram Invitations** | ✅ READY | Follow + DM with personalization |
| **Lead Storage (PostgreSQL)** | ✅ READY | Leads table with all fields |
| **Lead Scoring** | ✅ READY | 0-1 scale with thresholds |
| **Personalization** | ✅ READY | Template selection by interests |
| **Safety Features** | ✅ READY | Delays, max invites, logging |

### 🔄 IN DEVELOPMENT

| Component | Status | Details |
|-----------|--------|---------|
| **Telegram Collection** | 🔄 Framework | Needs Telethon client + API keys |
| **Telegram Analysis** | 🔄 Ready | Logic written, waiting for data |
| **Telegram Invitations** | 🔄 Ready | Logic written, Bot API configured |
| **Batch Processing** | 🔄 Partial | Scheduler jobs defined, not active |

### ❌ TODO

| Component | Status | Details |
|-----------|--------|---------|
| **LinkedIn Collection** | ❌ Not Started | Requires LinkedIn API setup |
| **LinkedIn Analysis** | ❌ Not Started | Job title extraction, etc |
| **LinkedIn Invitations** | ❌ Not Started | Connection requests, messaging |
| **Follow-up Automation** | ❌ Not Started | Retry logic, nurture sequences |
| **Response Tracking** | ❌ Not Started | Track who responds |

---

## 🎯 How It Determines Fake vs Real Lead

### Fake/Wrong Audience Indicators

```
RED FLAGS (Score Reduction):
├─ Private account with 0 posts: Likely fake
├─ No bio or empty bio: Suspicious
├─ Follower count < 10: Too new/fake
├─ 100% following, 0 followers: Bot
├─ Links only in bio: Spam
├─ ALL CAPS MESSAGES: Likely spam
├─ Engagement rate 0%: Inactive/fake
├─ Username looks auto-generated: Bot
└─ Repeatedly unresponsive: Mark as blocked

GREEN FLAGS (High Score):
├─ Real profile picture: Not anime/placeholder
├─ Detailed bio: Multi-line, specific role
├─ Consistent posting: Regular content
├─ Authentic engagement: Comments, replies
├─ Industry-specific keywords: Marketing, CEO, etc
├─ Professional account badge: Business account
├─ Proper follower/following ratio: 1:1 to 3:1
└─ Real job title in bio: Manager, Director, etc
```

### Confidence Levels

```
INVITE (0.6+): I'm confident this is a real B2B lead
├─ Has 3+ B2B keywords
├─ 100+ followers
├─ Business account
└─ Active posting
Result: Send personal invitation

SAVE (0.3-0.6): Might be useful later
├─ Has 1-2 B2B keywords
├─ Some activity indicators
├─ Could be good for nurture
└─ Store for future campaigns
Result: Keep in database, don't contact yet

SKIP (<0.3): Almost certainly wrong audience
├─ No B2B signals
├─ Consumer content
├─ No engagement
└─ Very new account
Result: Don't waste time on this person
```

---

## 📈 Metrics & Analytics

### Collection Performance

```
Example Run:
├─ Collected: 250 users from 5 sources
├─ Analyzed: 250 profiles
├─ Invited: 42 (16.8%)    [score ≥ 0.6]
├─ Saved: 127 (50.8%)     [0.3 ≤ score < 0.6]
├─ Skipped: 81 (32.4%)    [score < 0.3]
│
└─ Average score: 0.41
   ├─ High scorers (0.7+): 28 leads
   ├─ Mid scorers (0.4-0.7): 139 leads
   └─ Low scorers (<0.4): 83 leads
```

### Invitation Success Rate

```
Not yet tracked, but typical ranges:
├─ Response rate: 5-15% for cold DMs
├─ Engagement rate: 30-50% of respondents
├─ Conversion rate: 1-5% to actual customers
└─ Factors affecting:
   ├─ Message personalization
   ├─ Timing (business hours vs off-hours)
   ├─ Product relevance
   ├─ Account credibility
   └─ Follow-up sequences
```

---

## 🔧 Configuration & Thresholds

**File:** `.env`

```dotenv
# Scoring thresholds
SCORE_THRESHOLD_SAVE=0.3    # Save if score >= this
SCORE_THRESHOLD_INVITE=0.6  # Invite if score >= this

# Invitation safety
MAX_LEADS_PER_JOB=50        # Max leads per run
MAX_INVITES_PER_LEAD=1      # Send max 1 invite per person

# Delays (to avoid detection/bans)
FOLLOW_DELAY_MIN=10         # Seconds between follows
FOLLOW_DELAY_MAX=20
DM_DELAY_MIN=30             # Seconds between DMs
DM_DELAY_MAX=60
INVITE_DELAY_MIN=300        # 5 mins between invitations
INVITE_DELAY_MAX=600        # 10 mins

# Other
SCHEDULER_TIMEZONE=Europe/Berlin
SCHEDULER_ENABLED=True
```

---

## 📋 Data Flow Summary

```
Instagram.com
     ↓
InstagramCollector (Get followers/commenters)
     ↓
Extracted Data (username, bio, followers, etc)
     ↓
InstagramAnalyzer (Find B2B keywords, quality)
     ↓
LeadScorer (Calculate 0-1 score)
     ↓
Decision
├─ INVITE (≥0.6) → InstagramInviter → Follow + DM
├─ SAVE (0.3-0.6) → PostgreSQL leads table (inactive)
└─ SKIP (<0.3) → Discard

PostgreSQL
     ↓
Scheduler periodically:
├─ _collect_telegram_audience() - get new leads
├─ _collect_instagram_audience() - same
└─ _invite_telegram() / _invite_instagram() - contact them

Actions table logs:
├─ LEAD_COLLECTED - when we found them
├─ LEAD_ANALYZED - scoring results
├─ LEAD_INVITED - when we sent invitation
└─ LEAD_SKIPPED - why we rejected them
```

---

## 🎯 Next Steps to Improve System

### HIGH PRIORITY

1. **Complete Telegram Integration**
   - Add Telethon client setup
   - Implement actual chat/channel collection
   - Test on real Telegram data

2. **Response Tracking**
   - Monitor DM responses
   - Track engagement metrics
   - Adjust strategy based on results

3. **Follow-up Automation**
   - Send follow-up messages after 3 days
   - Different templates for no-response vs rejected

### MEDIUM PRIORITY

4. **LinkedIn Integration**
   - Setup LinkedIn scraper
   - Job title extraction
   - Company targeting

5. **Better Personalization**
   - More granular keyword detection
   - Industry-specific messages
   - Language-specific templates

6. **Blocklist Management**
   - Import competitor emails
   - Exclude corporate domains (we don't want HR)
   - Save blocked users forever

### LOW PRIORITY

7. **A/B Testing**
   - Test different message templates
   - Optimal send times
   - Personalization levels

8. **ML-Based Scoring**
   - Train model on response rates
   - Automatic threshold optimization
   - Anomaly detection for fakes

---

## ✅ Summary

### How We Find Them
1. **Instagram:** Followers of B2B accounts, commenters on industry posts
2. **Telegram:** Members of B2B groups/channels (pending implementation)
3. **LinkedIn:** Search by industry/role (future)

### How We Filter Them
1. **Analysis:** Extract bio, profile metrics, activity indicators
2. **Scoring:** 0-1 scale based on B2B signals, profile quality
3. **Decision:** INVITE (0.6+), SAVE (0.3-0.6), SKIP (<0.3)

### How We Store Them
1. **PostgreSQL leads table:** username, bio, score, platform, status
2. **Deduplication:** Check if already in DB before adding
3. **Status tracking:** invited, blocked, created_at, score

### How We Invite Them
1. **Instagram:** Follow + personalized DM (1 message per person)
2. **Telegram:** Direct message via Bot API (personalized)
3. **Safety:** Delays, max 1 invite per person, error handling

### How We Know If It's Real
1. **B2B Keywords:** 3+ words (0.6 score), 1+ words (>0.3)
2. **Profile Quality:** Followers, business account, posting frequency
3. **Activity:** Engagement rate, community participation
4. **Red Flags:** Fake accounts, bots, spam, unresponsive = blocked

---

**Status:** 🟢 **INSTAGRAM: READY TO USE**  
**Status:** 🔄 **TELEGRAM: 70% READY (needs Telethon setup)**  
**Status:** ❌ **LINKEDIN: NOT STARTED**

---

**Last Updated:** 2026-01-20  
**Created For:** Platform: VAT-Verifizierung Audience Analysis
