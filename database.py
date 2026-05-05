"""
database.py - MongoDB connection and operations
Tracks posted deals to avoid duplicates
"""

import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

logger = logging.getLogger(__name__)

client = None
db     = None


async def connect_db():
    """Connect to MongoDB"""
    global client, db
    try:
        client = AsyncIOMotorClient(Config.MONGO_URI)
        db     = client[Config.MONGO_DB_NAME]
        await db.command("ping")
        logger.info("MongoDB connected!")

        # Create indexes
        await db.posted_deals.create_index("product_id", unique=True)
        await db.posted_deals.create_index("posted_at")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise


async def is_deal_posted(product_id: str) -> bool:
    """Check if deal was already posted today"""
    try:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        result = await db.posted_deals.find_one({
            "product_id": product_id,
            "posted_at": {"$gte": today_start}
        })
        return result is not None
    except Exception as e:
        logger.error(f"Error checking deal: {e}")
        return False


async def mark_deal_posted(product_id: str, platform: str, category: str):
    """Save posted deal to MongoDB"""
    try:
        await db.posted_deals.update_one(
            {"product_id": product_id},
            {"$set": {
                "product_id": product_id,
                "platform":   platform,
                "category":   category,
                "posted_at":  datetime.utcnow()
            }},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error saving deal: {e}")


async def get_stats() -> dict:
    """Get posting statistics"""
    try:
        total  = await db.posted_deals.count_documents({})
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        today  = await db.posted_deals.count_documents({"posted_at": {"$gte": today_start}})
        return {"total_posted": total, "posted_today": today}
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {}


async def close_db():
    """Close MongoDB connection"""
    if client:
        client.close()
        logger.info("MongoDB connection closed")
