"""
scheduler.py - Schedule deal posting 3x daily
Fetches, filters, formats and posts to correct channels
"""

import logging
import random
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
from pyrogram.errors import FloodWait

from config import Config
from database import connect_db, is_deal_posted, mark_deal_posted
from fetchers import AmazonFetcher, FlipkartFetcher, NykaaFetcher
from formatter import (
    format_deal_message,
    format_poll_post,
    format_tip_post,
    format_morning_post,
)

logger = logging.getLogger(__name__)

# ─── Channel Map ─────────────────────────────────────────────────────────────
CHANNEL_MAP = {
    "electronics": Config.CHANNEL_ELECTRONICS,
    "fashion":     Config.CHANNEL_FASHION,
    "skincare":    Config.CHANNEL_SKINCARE,
    "home":        Config.CHANNEL_HOME,
}

# ─── Platform → Fetcher Map ──────────────────────────────────────────────────
FETCHERS = {
    "electronics": [AmazonFetcher(), FlipkartFetcher()],
    "fashion":     [FlipkartFetcher(), AmazonFetcher()],
    "skincare":    [NykaaFetcher(), AmazonFetcher()],
    "home":        [AmazonFetcher(), FlipkartFetcher()],
}


async def send_message_safe(app: Client, channel: str, text: str, photo: str = None):
    """Send message with flood wait handling"""
    try:
        if photo:
            await app.send_photo(channel, photo=photo, caption=text)
        else:
            await app.send_message(channel, text)
        await asyncio.sleep(2)  # Small delay between messages
    except FloodWait as e:
        logger.warning(f"FloodWait {e.value}s — waiting...")
        await asyncio.sleep(e.value)
        await send_message_safe(app, channel, text, photo)
    except Exception as e:
        logger.error(f"Failed to send to {channel}: {e}")


async def post_deals_session(app: Client):
    """Main posting session — fetch, filter, format, post"""
    logger.info(f"Starting deal session at {datetime.now().strftime('%H:%M')}")

    hour = datetime.now().hour

    # Morning greeting
    if hour == 9:
        await send_message_safe(app, Config.CHANNEL_MAIN, format_morning_post())
        await asyncio.sleep(3)

    categories = ["electronics", "fashion", "skincare", "home"]
    random.shuffle(categories)  # Randomize order each session

    posted_count = 0

    for category in categories:
        fetchers = FETCHERS[category]
        all_deals = []

        # Fetch from all platforms for this category
        for fetcher in fetchers:
            try:
                deals = await fetcher.fetch_deals(category, count=10)
                all_deals.extend(deals)
            except Exception as e:
                logger.error(f"Fetcher error for {category}: {e}")

        if not all_deals:
            logger.warning(f"No deals found for {category}")
            continue

        # Shuffle for variety
        random.shuffle(all_deals)

        # Post best deal for this category
        for deal in all_deals:
            product_id = deal.get("product_id", "")

            # Skip already posted today
            if await is_deal_posted(product_id):
                continue

            # Format message
            message = format_deal_message(deal)
            image   = deal.get("image", "")

            # Post to niche channel
            niche_channel = CHANNEL_MAP.get(category)
            if niche_channel:
                await send_message_safe(app, niche_channel, message, image)

            # Post to main channel too
            await send_message_safe(app, Config.CHANNEL_MAIN, message, image)

            # Mark as posted
            await mark_deal_posted(product_id, deal["platform"], category)

            posted_count += 1
            logger.info(f"Posted: {deal['title'][:50]} [{category}]")

            # Only 1 deal per category per session
            break

        # Small gap between categories
        await asyncio.sleep(5)

    # Occasionally post engagement content
    roll = random.random()
    if roll < 0.2:  # 20% chance
        await send_message_safe(app, Config.CHANNEL_MAIN, format_poll_post())
    elif roll < 0.35:  # 15% chance
        await send_message_safe(app, Config.CHANNEL_MAIN, format_tip_post())

    logger.info(f"Session complete. Posted {posted_count} deals.")


async def start_scheduler(app: Client):
    """Initialize DB and start APScheduler"""
    await connect_db()

    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

    # Schedule 3x daily
    scheduler.add_job(
        post_deals_session,
        "cron", hour=9,  minute=0,
        args=[app], id="morning"
    )
    scheduler.add_job(
        post_deals_session,
        "cron", hour=13, minute=0,
        args=[app], id="afternoon"
    )
    scheduler.add_job(
        post_deals_session,
        "cron", hour=20, minute=0,
        args=[app], id="evening"
    )

    scheduler.start()
    logger.info("Scheduler started — posting at 9 AM, 1 PM, 8 PM IST daily")
