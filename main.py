"""
Deal Bot - Main Entry Point
Starts the Pyrogram bot and scheduler
"""

import asyncio
import logging
from pyrogram import Client
from scheduler import start_scheduler
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting Deal Bot...")

    app = Client(
        "deal_bot",
        api_id=Config.TELEGRAM_API_ID,
        api_hash=Config.TELEGRAM_API_HASH,
        bot_token=Config.TELEGRAM_BOT_TOKEN
    )

    async with app:
        logger.info("Bot connected to Telegram!")
        await start_scheduler(app)
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
