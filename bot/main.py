"""
NexusBot — Web3 AI Telegram Assistant
======================================
Main entry point. Initializes bot, registers handlers, starts scheduler.

FREE STACK:
  Bot: aiogram 3.x
  DB: SQLite (aiosqlite)
  AI: Groq → OpenRouter → Gemini → DeepSeek (fallback chain)
  Data: DexScreener, CoinGecko, GitHub, Reddit
  Deploy: Railway free tier

Author: NexusBot
Version: 1.0.0
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN, LOG_LEVEL, BOT_NAME, ADMIN_USER_ID
from bot import database as db
from bot.services.scheduler import setup_scheduler

# Import all handlers
from bot.handlers import start, alpha, jobs, ai_chat, analysis, outreach, organizer, ecosystem, settings


# ─── Configure Logging ──────────────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    colorize=True,
)
logger.add(
    "logs/nexusbot.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time} | {level} | {message}",
)


async def on_startup(bot: Bot):
    """Called when the bot starts up."""
    logger.info("🚀 NexusBot starting up...")
    
    # Initialize database
    await db.init_db()
    
    # Send startup notification to admin
    if ADMIN_USER_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=(
                    "⚡ <b>NEXUSBOT ONLINE</b>\n"
                    "━" * 25 + "\n\n"
                    "✅ Database: Connected\n"
                    "✅ AI Service: Multi-model ready\n"
                    "✅ Scheduler: Running\n"
                    "✅ All handlers: Registered\n\n"
                    "🤖 Bot is fully operational!\n"
                    f"📡 Monitoring started\n\n"
                    "<i>Send /start to begin</i>"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Could not send startup message to admin: {e}")
    
    logger.success(f"✅ {BOT_NAME} is online and ready!")


async def on_shutdown(bot: Bot):
    """Called when the bot shuts down."""
    logger.info(f"🛑 {BOT_NAME} shutting down...")
    
    if ADMIN_USER_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_USER_ID,
                text="⚠️ <b>NexusBot is going offline.</b>\n<i>Will restart automatically on Railway.</i>",
                parse_mode="HTML"
            )
        except Exception:
            pass


async def main():
    """Main async entry point."""
    # Create bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register all routers (ORDER MATTERS for priority)
    dp.include_router(start.router)
    dp.include_router(alpha.router)
    dp.include_router(jobs.router)
    dp.include_router(analysis.router)
    dp.include_router(outreach.router)
    dp.include_router(organizer.router)
    dp.include_router(ecosystem.router)
    dp.include_router(settings.router)
    dp.include_router(ai_chat.router)  # Last — catches all non-command messages
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Setup and start scheduler
    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.success("✅ Background scheduler started")
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info(f"📡 Starting {BOT_NAME} polling...")
    
    try:
        # Start polling
        await dp.start_polling(
            bot,
            allowed_updates=["message", "callback_query", "inline_query"],
            drop_pending_updates=True,
        )
    finally:
        scheduler.shutdown()
        await bot.session.close()
        logger.info("✅ Bot session closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
