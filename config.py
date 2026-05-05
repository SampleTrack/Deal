"""
config.py - All environment variables and settings
Copy .env.example to .env and fill in your values
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ─── Telegram ───────────────────────────────────────────
    TELEGRAM_API_ID        = int(os.getenv("TELEGRAM_API_ID", 0))
    TELEGRAM_API_HASH      = os.getenv("TELEGRAM_API_HASH", "")
    TELEGRAM_BOT_TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # ─── Telegram Channels ──────────────────────────────────
    CHANNEL_MAIN           = os.getenv("CHANNEL_MAIN", "@your_main_channel")
    CHANNEL_ELECTRONICS    = os.getenv("CHANNEL_ELECTRONICS", "@your_electronics_channel")
    CHANNEL_FASHION        = os.getenv("CHANNEL_FASHION", "@your_fashion_channel")
    CHANNEL_SKINCARE       = os.getenv("CHANNEL_SKINCARE", "@your_skincare_channel")
    CHANNEL_HOME           = os.getenv("CHANNEL_HOME", "@your_home_channel")

    # ─── Amazon Affiliate ───────────────────────────────────
    AMAZON_ACCESS_KEY      = os.getenv("AMAZON_ACCESS_KEY", "")
    AMAZON_SECRET_KEY      = os.getenv("AMAZON_SECRET_KEY", "")
    AMAZON_AFFILIATE_TAG   = os.getenv("AMAZON_AFFILIATE_TAG", "yourtag-21")
    AMAZON_COUNTRY         = "IN"

    # ─── Flipkart Affiliate ─────────────────────────────────
    FLIPKART_AFFILIATE_ID  = os.getenv("FLIPKART_AFFILIATE_ID", "")
    FLIPKART_AFFILIATE_TOKEN = os.getenv("FLIPKART_AFFILIATE_TOKEN", "")

    # ─── Nykaa Affiliate ────────────────────────────────────
    NYKAA_AFFILIATE_ID     = os.getenv("NYKAA_AFFILIATE_ID", "")

    # ─── MongoDB ────────────────────────────────────────────
    MONGO_URI              = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME          = os.getenv("MONGO_DB_NAME", "dealbot")

    # ─── Scheduler Times (24hr format) ──────────────────────
    POST_TIMES             = ["09:00", "13:00", "20:00"]

    # ─── Deal Filters ───────────────────────────────────────
    MIN_RATING             = 3.5
    MIN_REVIEWS            = 50
    DEALS_PER_SESSION      = 5   # deals posted per scheduled run
