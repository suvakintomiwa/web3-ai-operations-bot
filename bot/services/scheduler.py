"""
NexusBot Scheduler
==================
APScheduler background jobs for automated alerts and data fetching.
Jobs:
  - Alpha scan every 5 minutes
  - Trending check every 10 minutes
  - Job alerts every hour
  - Reminder check every minute
  - Whale watch every 15 minutes
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from aiogram import Bot

from bot.config import (
    ALPHA_SCAN_INTERVAL, TRENDING_SCAN_INTERVAL,
    JOB_SCAN_INTERVAL, REMINDER_CHECK_INTERVAL, WHALE_SCAN_INTERVAL
)
from bot import database as db
from bot.services.dexscreener import get_trending_tokens, get_new_pairs, format_pair
from bot.services.coingecko import get_trending_coins
from bot.services.jobs_scraper import get_all_cm_jobs


# ─── Cache to prevent duplicate alerts ─────────────────────────────────────────
_seen_tokens: set = set()
_last_job_hash: str = ""


async def check_reminders(bot: Bot):
    """Check and send due reminders."""
    try:
        reminders = await db.get_due_reminders()
        for reminder in reminders:
            try:
                await bot.send_message(
                    chat_id=reminder["user_id"],
                    text=(
                        f"⏰ <b>REMINDER</b>\n"
                        f"{'━'*20}\n\n"
                        f"📌 {reminder['message']}\n\n"
                        f"<i>Set earlier • NexusBot</i>"
                    ),
                    parse_mode="HTML"
                )
                await db.mark_reminder_sent(reminder["id"])
                logger.info(f"✅ Reminder sent to {reminder['user_id']}")
            except Exception as e:
                logger.error(f"Failed to send reminder {reminder['id']}: {e}")
    except Exception as e:
        logger.error(f"Reminder check error: {e}")


async def scan_new_alpha(bot: Bot):
    """Scan for new alpha opportunities and alert subscribers."""
    global _seen_tokens
    
    try:
        subscribers = await db.get_alert_subscribers("alpha")
        if not subscribers:
            return
        
        # Get new pairs from DexScreener
        pairs = await get_new_pairs(limit=5)
        
        new_tokens = []
        for pair in pairs:
            token = format_pair(pair)
            token_id = f"{token['chain']}-{token['address']}"
            
            if token_id not in _seen_tokens and token.get("liquidity_usd", 0) > 10000:
                new_tokens.append(token)
                _seen_tokens.add(token_id)
        
        # Keep cache from growing too large
        if len(_seen_tokens) > 500:
            _seen_tokens = set(list(_seen_tokens)[-250:])
        
        if not new_tokens:
            return
        
        # Format alert message
        msg_lines = [
            "🔔 <b>NEW ALPHA ALERT</b>",
            "━" * 25,
            "",
        ]
        
        for token in new_tokens[:3]:
            from bot.services.formatter import format_token_card
            msg_lines.append(format_token_card(token))
            msg_lines.append("")
        
        msg_lines.append("⚡ <i>NexusBot Alpha Scanner • DYOR</i>")
        msg = "\n".join(msg_lines)
        
        # Send to all alpha subscribers
        for user_id in subscribers:
            try:
                await bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML",
                                        disable_web_page_preview=True)
                await asyncio.sleep(0.1)  # Rate limit
            except Exception as e:
                logger.warning(f"Failed to send alpha alert to {user_id}: {e}")
        
        logger.info(f"📡 Alpha alert sent to {len(subscribers)} subscribers")
        
    except Exception as e:
        logger.error(f"Alpha scan error: {e}")


async def scan_trending(bot: Bot):
    """Send trending tokens alert."""
    try:
        subscribers = await db.get_alert_subscribers("trending")
        if not subscribers:
            return
        
        coins = await get_trending_coins()
        if not coins:
            return
        
        msg_lines = ["🔥 <b>TRENDING UPDATE</b>", "━" * 25, ""]
        
        for i, coin_data in enumerate(coins[:5], 1):
            item = coin_data.get("item", {})
            name = item.get("name", "Unknown")
            symbol = item.get("symbol", "?").upper()
            rank = item.get("market_cap_rank", "?")
            msg_lines.append(f"{i}. <b>{name}</b> <code>${symbol}</code> | Rank #{rank}")
        
        msg_lines.extend(["", "⚡ <i>Via CoinGecko • NexusBot Alerts</i>"])
        msg = "\n".join(msg_lines)
        
        for user_id in subscribers:
            try:
                await bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML",
                                        disable_web_page_preview=True)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"Failed to send trending alert to {user_id}: {e}")
        
    except Exception as e:
        logger.error(f"Trending scan error: {e}")


async def scan_jobs(bot: Bot):
    """Send new job alerts to subscribers."""
    global _last_job_hash
    
    try:
        subscribers = await db.get_alert_subscribers("jobs")
        if not subscribers:
            return
        
        jobs = await get_all_cm_jobs()
        if not jobs:
            return
        
        # Simple dedup: hash first job title
        current_hash = f"{jobs[0]['title'][:30]}" if jobs else ""
        if current_hash == _last_job_hash:
            return
        _last_job_hash = current_hash
        
        msg_lines = ["💼 <b>NEW JOB ALERT</b>", "━" * 25, ""]
        
        for job in jobs[:3]:
            msg_lines.extend([
                f"🎯 <b>{job['title']}</b>",
                f"🏢 {job.get('company', 'Anonymous')} • 🌐 Remote",
                f"🔗 <a href='{job.get('url', '#')}'>Apply →</a>",
                "",
            ])
        
        msg_lines.append("⚡ <i>NexusBot Job Scanner • New opportunities found</i>")
        msg = "\n".join(msg_lines)
        
        for user_id in subscribers:
            try:
                await bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML",
                                        disable_web_page_preview=True)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"Failed to send job alert to {user_id}: {e}")
        
    except Exception as e:
        logger.error(f"Job scan error: {e}")


async def whale_watch(bot: Bot):
    """Monitor for whale activity alerts."""
    try:
        subscribers = await db.get_alert_subscribers("whale")
        if not subscribers:
            return
        
        # Get pairs with high volume (proxy for whale activity)
        pairs = await get_trending_tokens(limit=3)
        
        if not pairs:
            return
        
        whale_tokens = []
        for pair in pairs:
            if isinstance(pair, dict):
                token = format_pair(pair) if "baseToken" in pair else pair
                vol = token.get("volume_24h", 0)
                mc = token.get("market_cap", 0)
                
                if mc > 0 and vol > 0:
                    vol_mc = vol / mc
                    if vol_mc > 2:  # Volume > 2x market cap = whale activity
                        whale_tokens.append((token, vol_mc))
        
        if not whale_tokens:
            return
        
        msg_lines = ["🐋 <b>WHALE ALERT</b>", "━" * 25, ""]
        
        for token, ratio in whale_tokens[:2]:
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "?")
            vol = token.get("volume_24h", 0)
            from bot.services.formatter import format_number
            msg_lines.extend([
                f"🐋 <b>{name}</b> <code>${symbol}</code>",
                f"📊 Vol/MC Ratio: {ratio:.1f}x",
                f"💰 24h Volume: {format_number(vol)}",
                "",
            ])
        
        msg_lines.append("⚠️ <i>High volume detected • Could be whale activity • DYOR</i>")
        msg = "\n".join(msg_lines)
        
        for user_id in subscribers:
            try:
                await bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML",
                                        disable_web_page_preview=True)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"Failed to send whale alert to {user_id}: {e}")
        
    except Exception as e:
        logger.error(f"Whale watch error: {e}")


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Create and configure the scheduler with all jobs."""
    scheduler = AsyncIOScheduler(timezone="UTC")
    
    # Reminder check — every minute
    scheduler.add_job(
        check_reminders,
        trigger=IntervalTrigger(minutes=REMINDER_CHECK_INTERVAL),
        args=[bot],
        id="reminders",
        name="Check Reminders",
        replace_existing=True,
    )
    
    # Alpha scan — every 5 minutes
    scheduler.add_job(
        scan_new_alpha,
        trigger=IntervalTrigger(minutes=ALPHA_SCAN_INTERVAL),
        args=[bot],
        id="alpha_scan",
        name="Alpha Scanner",
        replace_existing=True,
    )
    
    # Trending check — every 10 minutes
    scheduler.add_job(
        scan_trending,
        trigger=IntervalTrigger(minutes=TRENDING_SCAN_INTERVAL),
        args=[bot],
        id="trending_scan",
        name="Trending Scanner",
        replace_existing=True,
    )
    
    # Job alerts — every hour
    scheduler.add_job(
        scan_jobs,
        trigger=IntervalTrigger(minutes=JOB_SCAN_INTERVAL),
        args=[bot],
        id="job_scan",
        name="Job Scanner",
        replace_existing=True,
    )
    
    # Whale watch — every 15 minutes
    scheduler.add_job(
        whale_watch,
        trigger=IntervalTrigger(minutes=WHALE_SCAN_INTERVAL),
        args=[bot],
        id="whale_watch",
        name="Whale Watcher",
        replace_existing=True,
    )
    
    logger.success(f"✅ Scheduler configured: {len(scheduler.get_jobs())} jobs registered")
    return scheduler
