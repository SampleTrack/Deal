# 🤖 Deal Bot — Telegram Affiliate Deal Automation

Automatically fetches deals from **Amazon, Flipkart & Nykaa**, formats them with
honest data + psychological triggers, and posts to **5 Telegram channels** — 3x daily.

---

## 📁 Project Structure

```
deal-bot/
├── main.py              # Entry point — starts bot + scheduler
├── config.py            # All settings from .env
├── database.py          # MongoDB — tracks posted deals
├── scheduler.py         # Posts deals at 9 AM, 1 PM, 8 PM IST
├── formatter.py         # Message templates with variety + psychology
├── fetchers/
│   ├── __init__.py
│   ├── amazon.py        # Amazon PA API fetcher
│   ├── flipkart.py      # Flipkart Affiliate API fetcher
│   └── nykaa.py         # Nykaa Affiliate API fetcher
├── requirements.txt
├── render.yaml          # Render.com deployment config
├── .env.example         # Copy to .env and fill values
└── .gitignore
```

---

## ⚙️ Setup Guide (Step by Step)

### Step 1 — Get Telegram Credentials

1. Go to https://my.telegram.org/apps
2. Create a new app
3. Copy **API ID** and **API Hash**

### Step 2 — Create Telegram Bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Give it a name (e.g. `My Deal Bot`)
4. Copy the **Bot Token**

### Step 3 — Create Your 5 Channels

Create these channels on Telegram:
- `@your_main_deals_channel` — All deals
- `@your_electronics_channel` — Electronics only
- `@your_fashion_channel` — Fashion only
- `@your_skincare_channel` — Skincare only
- `@your_home_channel` — Home & Kitchen only

⚠️ **Add your bot as Admin** to all 5 channels!

### Step 4 — Get Affiliate IDs

| Platform | Signup URL |
|---|---|
| Amazon | https://affiliate-program.amazon.in |
| Flipkart | https://affiliate.flipkart.com |
| Nykaa | https://www.nykaa.com/affiliate |

### Step 5 — Setup MongoDB (Free)

1. Go to https://www.mongodb.com/atlas
2. Create free account
3. Create a free cluster
4. Copy the **connection string**

### Step 6 — Configure Environment

```bash
cp .env.example .env
# Fill in all values in .env
```

### Step 7 — Run Locally (Testing)

```bash
pip install -r requirements.txt
python main.py
```

### Step 8 — Deploy to Render (Free Hosting)

1. Push this repo to GitHub
2. Go to https://render.com
3. Click **New → Background Worker**
4. Connect your GitHub repo
5. Add all environment variables from `.env`
6. Click **Deploy**

✅ Bot runs 24/7 for free on Render!

---

## 🤖 How The Bot Works

```
9 AM / 1 PM / 8 PM daily
         ↓
Fetch deals from Amazon + Flipkart + Nykaa
         ↓
Filter (rating 3.5+, 50+ reviews)
         ↓
Check MongoDB — skip already posted deals
         ↓
Format with honest data + psychology + variety
         ↓
Post to correct niche channel + main channel
         ↓
Save to MongoDB to avoid duplicates
```

---

## 📢 Channel → Platform Mapping

| Channel | Platforms Used |
|---|---|
| Main (all deals) | Amazon + Flipkart + Nykaa |
| Electronics | Amazon + Flipkart |
| Fashion | Flipkart + Amazon |
| Skincare | Nykaa + Amazon |
| Home & Kitchen | Amazon + Flipkart |

---

## 💬 Message Variety System

Every post uses random combination of:
- **8 different openers** — never repeats same headline
- **5 writing styles** — excited / informative / conversational / urgency / story
- **7 day themes** — Monday Deal, Friday Fiesta, etc.
- **Time greetings** — Morning / Afternoon / Evening
- **8 CTA variants** — different call to action buttons
- **Occasional polls + tips** — keeps channel engaging

---

## ✅ Honesty Rules (Built In)

The bot **only shows real data**:
- Free delivery → only shown if actually free
- Stock warning → only shown if real stock message exists
- EMI → only shown if actually available
- Rating → real rating from platform API
- Reviews → real review count from platform API
- Savings → calculated from real MRP vs current price

---

## 📊 MongoDB Collections

| Collection | Purpose |
|---|---|
| `posted_deals` | Tracks all posted deals to avoid duplicates |

---

## 🔧 Customization

Edit `config.py` to change:
- `POST_TIMES` — posting schedule
- `MIN_RATING` — minimum product rating filter
- `MIN_REVIEWS` — minimum reviews filter
- `DEALS_PER_SESSION` — deals per posting session

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| pyrogram | Telegram Bot framework |
| TgCrypto | Encryption for Pyrogram |
| motor | Async MongoDB driver |
| apscheduler | Job scheduling |
| aiohttp | Async HTTP requests for APIs |
| python-dotenv | Load .env variables |
| amazon-paapi5 | Amazon Product Advertising API helper |

---

## ⚠️ Important Notes

1. **Never commit `.env` to GitHub** — it contains secret keys
2. Add your bot as **Admin** in all 5 channels before running
3. Amazon PA API requires **3 sales in 180 days** to stay active
4. Flipkart affiliate requires approval — apply at affiliate.flipkart.com
5. Test with a private channel first before going live

---

## 💰 Expected Earnings (Estimate)

| Stage | Monthly Income |
|---|---|
| Month 1 (setup) | ₹2,000 – ₹5,000 |
| Month 3 (growing) | ₹8,000 – ₹20,000 |
| Month 6 (established) | ₹25,000 – ₹60,000 |

*Depends on channel growth, niche, and deal quality*
