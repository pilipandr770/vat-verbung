# 🎯 Audience Acquisition Pipeline - Quick Reference

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│              AUDIENCE SEARCH → FILTER → INVITE SYSTEM               │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 1️⃣  DISCOVERY: WHERE WE FIND THEM                                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  INSTAGRAM                          TELEGRAM                         │
│  ├─ Followers of                    ├─ Members of B2B chats       │
│  │  B2B accounts                    │  (Group lists)              │
│  ├─ Commenters on                   ├─ Channel participants       │
│  │  industry posts                  │  (Public channels)          │
│  └─ Example targets:                ├─ Message senders            │
│     @marketing_agency               │  (Active users)             │
│     @b2b_startup_hub                └─ Status: 🔄 Pending         │
│     @digital_solutions              │  Telethon setup             │
│  └─ Status: ✅ ACTIVE               │                             │
│                                     │  LINKEDIN (Future)          │
│  + Public data access               ├─ Search by industry         │
│  + Large followings                 ├─ Group members              │
│  + Activity indicators              └─ Status: ❌ Not started    │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 2️⃣  DATA EXTRACTION: WHAT WE CAPTURE                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  username:        maria_lopez_marketing                             │
│  user_id:         1234567890                                        │
│  bio:             "Digital Marketing Manager | B2B SaaS | 5+ yrs"   │
│  followers:       2,450                                             │
│  following:       890                                               │
│  posts:           157                                               │
│  is_business:     True                                              │
│  is_private:      False                                             │
│  source:          followers_of_b2b_marketing_agency                │
│  email:           (if found)                                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 3️⃣  ANALYSIS: PROFILE DEEP-DIVE                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  B2B KEYWORDS DETECTION                                             │
│  ├─ "Digital" ✓                   → +0.35 points                   │
│  ├─ "Marketing" ✓                 (3+ keywords found)              │
│  ├─ "Manager" ✓                                                     │
│  └─ Match: B2B Industry                                             │
│                                                                       │
│  PROFILE QUALITY ANALYSIS                                           │
│  ├─ Followers: 2,450              → +0.1 (good range)              │
│  ├─ Ratio: 2.75                   → +0.2 (excellent)               │
│  ├─ Posts: 157                    → +0.1 (very active)             │
│  ├─ Business account: Yes         → +0.15 (official)               │
│  └─ Public: Yes                   → +0.05 (transparent)            │
│                                                                       │
│  ACTIVITY INDICATORS                                                │
│  ├─ Posting frequency: Regular                                      │
│  ├─ Engagement rate: High                                           │
│  └─ Network quality: Professional                                   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 4️⃣  SCORING: RELEVANCE CALCULATION                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  SCORE COMPONENTS (0.0 - 1.0 scale)                                │
│  ├─ B2B Keywords:          +0.35   (3+ keywords)                   │
│  ├─ Follower Quality:      +0.1    (100-100K range)                │
│  ├─ Business Account:      +0.15   (verified)                      │
│  ├─ Engagement Ratio:      +0.1    (>1.5 followers/following)      │
│  ├─ Activity:              +0.1    (10+ posts)                     │
│  └─ Profile Type:          +0.05   (public)                        │
│  ────────────────────────────────                                   │
│     TOTAL SCORE:           0.80    (80% relevant)                  │
│                                                                       │
│  SCORE RANGES & ACTIONS                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Score      │ Decision │ Action                              │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ≥ 0.6      │ INVITE   │ Send personalized invitation ✅     │   │
│  │ 0.3 - 0.6  │ SAVE     │ Store for future campaigns 📦       │   │
│  │ < 0.3      │ SKIP     │ Discard, likely wrong audience ❌   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  MARIA'S SCORE: 0.80 → INVITE                                       │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 5️⃣  STORAGE: DATABASE PERSISTENCE                                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  PostgreSQL leads TABLE                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ id  │ username │ score │ platform  │ invited │ blocked │   │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ 42  │ maria... │ 0.80  │ instagram │  false  │  false  │   │   │
│  │ 43  │ john...  │ 0.05  │ instagram │  false  │  false  │   │   │
│  │ 44  │ alex...  │ 0.55  │ instagram │  false  │  false  │   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  Fields Stored:                                                     │
│  ├─ Identifiers: username, email, user_id, identifier              │
│  ├─ Metadata: bio, source, platform                                │
│  ├─ Scoring: score (0-1), invited, blocked                         │
│  └─ Timestamp: created_at                                          │
│                                                                       │
│  Status: ✅ ACTIVE & GROWING                                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 6️⃣  INVITATION: HOW WE CONTACT THEM                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  INSTAGRAM APPROACH                                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Step 1: FOLLOW USER (Non-intrusive)                     │        │
│  │ ├─ Action: Click follow button                          │        │
│  │ ├─ Delay: 10 seconds                                    │        │
│  │ └─ Purpose: Get on their radar                          │        │
│  │                                                          │        │
│  │ Step 2: SEND DM (Personalized)                          │        │
│  │ ├─ Trigger: Wait 30 seconds                             │        │
│  │ ├─ Template: Selected based on bio                      │        │
│  │ ├─ If "marketing" in bio:                               │        │
│  │ │  "Hi Maria! 👋 Noticed your interest in B2B           │        │
│  │ │   marketing. We're sharing insights on                │        │
│  │ │   automation & growth. Join us? 🚀"                   │        │
│  │ ├─ Once only: MAX_INVITES_PER_LEAD=1                   │        │
│  │ └─ Mark: invited=TRUE in database                       │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                                                       │
│  TELEGRAM APPROACH                                                   │
│  ├─ Direct message via Bot API                                      │
│  ├─ Personalized based on bio                                       │
│  ├─ Delay: 5 minutes between messages                               │
│  └─ Same personalization as Instagram                               │
│                                                                       │
│  LINKEDIN APPROACH (Future)                                         │
│  ├─ Connection request                                              │
│  ├─ Personalized message                                            │
│  └─ Follow-up sequences                                             │
│                                                                       │
│  SAFETY FEATURES                                                    │
│  ├─ Delays: 10-60 sec between actions                               │
│  ├─ Max 1 invite per person (no spam)                               │
│  ├─ Check invited=TRUE (never reinvite)                             │
│  ├─ Error handling (bans, auth issues)                              │
│  └─ Logging: Every action recorded                                  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 7️⃣  TRACKING: MEASURING SUCCESS                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  PostgreSQL actions TABLE                                           │
│  ├─ LEAD_COLLECTED: When we found them                              │
│  ├─ LEAD_ANALYZED: Scoring & analysis results                       │
│  ├─ LEAD_INVITED: When invitation was sent                          │
│  └─ LEAD_SKIPPED: Why we rejected them                              │
│                                                                       │
│  Example Log:                                                       │
│  ├─ 14:35 - Collected maria_lopez_marketing                         │
│  ├─ 14:36 - Analyzed (score: 0.80)                                  │
│  ├─ 14:37 - Followed user                                           │
│  ├─ 14:38 - Sent DM                                                 │
│  ├─ 14:39 - Marked as invited                                       │
│  └─ (pending) - Awaiting response                                   │
│                                                                       │
│  Metrics Tracked:                                                   │
│  ├─ Total collected: 250+ leads                                     │
│  ├─ Invited: ~42 (16.8%)                                            │
│  ├─ Saved: ~127 (50.8%)                                             │
│  ├─ Skipped: ~81 (32.4%)                                            │
│  └─ Average score: 0.41                                             │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

FAKE vs REAL LEAD DETECTION
═══════════════════════════════════════════════════════════════════════

🚩 FAKE/WRONG AUDIENCE (Low Score)        ✅ REAL B2B LEAD (High Score)
├─ No bio or vague                         ├─ Detailed bio with role
├─ <10 followers                           ├─ 100+ followers
├─ 0 posts / Never active                  ├─ Regular posting
├─ Private account, closed                 ├─ Public, transparent
├─ Auto-generated username                 ├─ Professional name
├─ All-caps messages                       ├─ Normal messaging
├─ Engagement rate: 0%                     ├─ Comments, interactions
├─ Links only (spam)                       ├─ Real content
└─ Consumer interests (memes, travel)      └─ Industry keywords

CONFIDENCE LEVELS:
├─ 0.6-1.0 (HIGH): 99% sure this is a real B2B lead
│  └─ Action: Send invitation immediately
│
├─ 0.3-0.6 (MEDIUM): Might be useful later
│  └─ Action: Store in database, nurture later
│
└─ 0.0-0.3 (LOW): Almost certainly wrong audience
   └─ Action: Skip, don't contact

DECISION FLOWCHART
═══════════════════════════════════════════════════════════════════════

                      FOUND USER
                          ↓
              Extract Profile Data
                          ↓
                  Analyze Profile
                          ↓
         B2B Keywords Found?
                ↙         ↘
             YES          NO
              ↓           ↓
          Count:3+    Count:1-2      Count:0
            ↓           ↓             ↓
          +0.35       +0.2          +0.0
            ↓           ↓             ↓
       Follower Quality Assessment
            ↓           ↓             ↓
       Profile Completeness Check
            ↓           ↓             ↓
        Activity Level
            ↓           ↓             ↓
         SCORE       SCORE         SCORE
         0.60+      0.30-0.60      <0.30
            ↓           ↓             ↓
         INVITE      SAVE           SKIP
          (✅)         (📦)          (❌)
            ↓           ↓             ↓
        Follow +      Store in      Discard
         DM msg      Database

CURRENT STATUS
═══════════════════════════════════════════════════════════════════════

✅ INSTAGRAM
   ├─ Collection: WORKING (followers, comments)
   ├─ Analysis: WORKING (bio keywords, profile quality)
   ├─ Scoring: WORKING (0-1 scale)
   └─ Invitation: WORKING (follow + DM)

🔄 TELEGRAM
   ├─ Collection: FRAMEWORK READY (needs Telethon)
   ├─ Analysis: READY (logic implemented)
   ├─ Scoring: READY (reuses LeadScorer)
   └─ Invitation: READY (Bot API configured)

❌ LINKEDIN
   ├─ Collection: NOT STARTED
   ├─ Analysis: NOT STARTED
   ├─ Scoring: NOT STARTED
   └─ Invitation: NOT STARTED

TIMELINE
═════════════════════════════════════════════════════════════════════

Per Day (Automated):
├─ 🔍 Collection runs: 2-3 times/day
│  └─ Discovers: 50-100 new leads
├─ 📊 Analysis: Instant (per discovery)
├─ 📧 Invitations: Spread throughout day
│  └─ Sends: 20-30 personalized messages
└─ 📈 Tracking: Real-time logging

Per Week:
├─ Total new leads: 300-500
├─ Total invited: 50-100 (high-quality)
├─ Total saved: 150-250 (for nurturing)
└─ Success rate: TBD (measuring now)

Per Month:
├─ Total acquired: 1,200-2,000 leads
├─ Database size: Growing
├─ Average quality: Improving
└─ ROI: TBD (tracking responses)

═══════════════════════════════════════════════════════════════════════
Last Updated: 2026-01-20
System Status: 🟢 INSTAGRAM READY, 🔄 TELEGRAM IN PROGRESS
═══════════════════════════════════════════════════════════════════════
```
