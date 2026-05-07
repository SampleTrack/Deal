import asyncio
import logging
import os
from aiohttp import web
from pyrogram import Client
from scheduler import start_scheduler
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- DUMMY WEB SERVER ---
async def handle_health_check(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render assigns a PORT dynamically, default to 8080 locally
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Dummy web server listening on port {port}")
# ------------------------

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
        
        # Start the fake web server to satisfy Render
        await start_dummy_server()
        
        # Start your deal scheduler
        await start_scheduler(app)
        
        # Keep the process alive
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
