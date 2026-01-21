# Instagram Graph API Configuration

## Overview

The system supports **two ways** to publish to Instagram:

1. **instagrapi** (current) - Direct Instagram login
   - Pro: Works with any account
   - Con: Vulnerable to IP blocking (Render is blocked)

2. **Meta Graph API** (recommended) - Official Meta API
   - Pro: No IP blocking, official & reliable
   - Con: Requires Business Account setup

---

## Setup Instagram Graph API

### Step 1: Prepare Instagram Account

1. Convert your Instagram account to **Business Account**:
   - Settings → Account Type → Switch to Professional Account → Select "Business"

2. Connect to Facebook Page:
   - Go to Facebook.com
   - Create a Facebook Page (or use existing)
   - Go to Settings → Instagram Accounts → Connect your Business Account

### Step 2: Create Meta App

1. Go to https://developers.facebook.com/apps/
2. Click "Create App"
3. Choose **Business** type
4. Fill in details and create

### Step 3: Add Instagram Product

1. In your Meta App, go to **Products**
2. Add **Instagram Graph API**
3. Add **Facebook Login**

### Step 4: Get Access Token

1. Go to **Tools → Access Token Debugger**
2. Generate a **System User Access Token**:
   - Settings → Users → System Users
   - Create system user with "Admin" role
   - Generate token with these permissions:
     - `instagram_business_content_publish`
     - `instagram_business_manage_messages`
     - `instagram_business_manage_comments`
     - `pages_manage_posts`

3. Copy the **Access Token** (it looks like: `EAABs...`)

### Step 5: Get Business Account ID

1. Go to your Meta App dashboard
2. Go to **Tools → Graph API Explorer**
3. Run query:
```
GET /me/instagram_business_accounts
```
4. Copy the `id` field (looks like: `17841401234567890`)

### Step 6: Update .env

Add to your `.env` file:

```bash
# Instagram Graph API (optional - for Meta Business Account)
META_ACCESS_TOKEN=EAABs...YOUR_TOKEN_HERE...
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841401234567890
```

### Step 7: Verify Setup

Run this Python script to test:

```python
from channels.instagram.graph_api_publisher import InstagramGraphAPIPublisher

publisher = InstagramGraphAPIPublisher()
result = InstagramGraphAPIPublisher.validate_credentials(
    business_account_id=YOUR_ID,
    access_token=YOUR_TOKEN
)
print("✅ Valid" if result else "❌ Invalid")
```

---

## How It Works

Once configured:

1. **System automatically detects** Graph API credentials in .env
2. **Scheduler uses Graph API** for Instagram publishing
3. **No more IP blocking** - posts go through official Meta API
4. **Automatic fallback** to instagrapi if Graph API not configured

---

## Publishing Flow

```
Content Generation (30 themes)
    ↓
LinkedIn + Telegram + Instagram (Graph API)
    ↓
Database (Post + Action logs)
    ↓
Insights via Meta API Analytics
```

---

## Troubleshooting

**Error: "Graph API credentials not configured"**
- Add `META_ACCESS_TOKEN` and `INSTAGRAM_BUSINESS_ACCOUNT_ID` to .env
- Or remove them to fallback to instagrapi

**Error: "Invalid credentials"**
- Check token hasn't expired (long-lived tokens expire in ~60 days)
- Verify Business Account ID is correct
- Regenerate token in Meta App dashboard

**Posts publishing with placeholder image**
- Graph API currently uses placeholder
- To use real images: Upload to Meta server first, get image ID, then publish

---

## References

- https://developers.facebook.com/docs/instagram-api
- https://developers.facebook.com/docs/instagram-api/guides/content-publishing
- https://developers.facebook.com/docs/instagram-api/reference/ig-user/media

