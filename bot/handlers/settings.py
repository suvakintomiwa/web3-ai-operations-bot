"""
Settings & Alerts Handlers
===========================
/settings, /alerts commands
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database as db

router = Router()

ALERT_CONFIG = {
    "alpha": {"emoji": "⚡", "label": "Alpha Alerts", "desc": "New gem discoveries every 5min"},
    "trending": {"emoji": "🔥", "label": "Trending Updates", "desc": "What's pumping every 10min"},
    "jobs": {"emoji": "💼", "label": "Job Alerts", "desc": "New Web3 job postings hourly"},
    "whale": {"emoji": "🐋", "label": "Whale Alerts", "desc": "Large wallet movement alerts"},
    "memecoins": {"emoji": "🎭", "label": "Memecoin Alerts", "desc": "New meme coin launches"},
    "airdrops": {"emoji": "🪂", "label": "Airdrop Alerts", "desc": "Airdrop opportunity alerts"},
}


def alerts_keyboard(active_alerts: set) -> InlineKeyboardMarkup:
    """Build alerts toggle keyboard."""
    buttons = []
    
    for alert_type, config in ALERT_CONFIG.items():
        is_active = alert_type in active_alerts
        status = "✅" if is_active else "❌"
        label = f"{status} {config['emoji']} {config['label']}"
        buttons.append([InlineKeyboardButton(
            text=label,
            callback_data=f"toggle_alert_{alert_type}"
        )])
    
    buttons.append([
        InlineKeyboardButton(text="✅ Enable All", callback_data="alerts_enable_all"),
        InlineKeyboardButton(text="❌ Disable All", callback_data="alerts_disable_all"),
    ])
    buttons.append([InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("alerts"))
async def cmd_alerts(message: Message):
    """Manage alert subscriptions."""
    user_id = message.from_user.id
    user_alerts = await db.get_user_alerts(user_id)
    active = {a["alert_type"] for a in user_alerts if a["is_active"]}
    
    lines = [
        "🔔 <b>ALERT SUBSCRIPTIONS</b>",
        "━" * 28,
        "",
        "Toggle which alerts you want to receive:",
        "",
    ]
    
    for alert_type, config in ALERT_CONFIG.items():
        is_active = alert_type in active
        status = "✅ ON" if is_active else "❌ OFF"
        lines.append(f"{config['emoji']} <b>{config['label']}</b> — {status}")
        lines.append(f"   <i>{config['desc']}</i>")
        lines.append("")
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=alerts_keyboard(active)
    )


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Show bot settings."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    username = user.get("username", "Not set") if user else "Not set"
    joined = user.get("joined_at", "Unknown")[:10] if user else "Unknown"
    
    # Count user data
    notes = await db.get_notes(user_id, limit=100)
    watchlist = await db.get_watchlist(user_id)
    user_alerts = await db.get_user_alerts(user_id)
    active_alerts = sum(1 for a in user_alerts if a["is_active"])
    
    settings_msg = (
        f"⚙️ <b>NEXUSBOT SETTINGS</b>\n"
        f"━" * 28 + f"\n\n"
        f"👤 <b>PROFILE</b>\n"
        f"ID: <code>{user_id}</code>\n"
        f"Username: @{username}\n"
        f"Joined: {joined}\n\n"
        f"📊 <b>YOUR DATA</b>\n"
        f"📝 Notes saved: {len(notes)}\n"
        f"👁️ Watchlist items: {len(watchlist)}\n"
        f"🔔 Active alerts: {active_alerts}/{len(ALERT_CONFIG)}\n\n"
        f"🤖 <b>AI CONFIGURATION</b>\n"
        f"Primary: Groq (LLaMA 3 70B)\n"
        f"Fallback 1: OpenRouter (Mistral)\n"
        f"Fallback 2: Google Gemini Pro\n"
        f"Fallback 3: DeepSeek Chat\n\n"
        f"━" * 28 + f"\n"
        f"<i>Version 1.0.0 • Free Stack • Railway</i>"
    )
    
    await message.answer(
        settings_msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔔 Manage Alerts", callback_data="menu_alerts"),
                InlineKeyboardButton(text="📝 Notes", callback_data="cmd_notes"),
            ],
            [
                InlineKeyboardButton(text="👁️ Watchlist", callback_data="cmd_watchlist"),
                InlineKeyboardButton(text="🗑️ Clear History", callback_data="ai_clear"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ])
    )


# ─── Alert Toggle Callbacks ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("toggle_alert_"))
async def cb_toggle_alert(callback: CallbackQuery):
    alert_type = callback.data.replace("toggle_alert_", "")
    user_id = callback.from_user.id
    
    # Get current state
    user_alerts = await db.get_user_alerts(user_id)
    active = {a["alert_type"] for a in user_alerts if a["is_active"]}
    
    if alert_type in active:
        await db.unsubscribe_alert(user_id, alert_type)
        config = ALERT_CONFIG.get(alert_type, {})
        await callback.answer(f"❌ {config.get('emoji', '')} {config.get('label', '')} disabled")
    else:
        await db.subscribe_alert(user_id, alert_type)
        config = ALERT_CONFIG.get(alert_type, {})
        await callback.answer(f"✅ {config.get('emoji', '')} {config.get('label', '')} enabled!")
    
    # Refresh keyboard
    user_alerts = await db.get_user_alerts(user_id)
    new_active = {a["alert_type"] for a in user_alerts if a["is_active"]}
    
    try:
        await callback.message.edit_reply_markup(reply_markup=alerts_keyboard(new_active))
    except Exception:
        pass


@router.callback_query(F.data == "alerts_enable_all")
async def cb_enable_all_alerts(callback: CallbackQuery):
    user_id = callback.from_user.id
    for alert_type in ALERT_CONFIG.keys():
        await db.subscribe_alert(user_id, alert_type)
    
    user_alerts = await db.get_user_alerts(user_id)
    active = {a["alert_type"] for a in user_alerts if a["is_active"]}
    
    await callback.answer("✅ All alerts enabled!")
    try:
        await callback.message.edit_reply_markup(reply_markup=alerts_keyboard(active))
    except Exception:
        pass


@router.callback_query(F.data == "alerts_disable_all")
async def cb_disable_all_alerts(callback: CallbackQuery):
    user_id = callback.from_user.id
    for alert_type in ALERT_CONFIG.keys():
        await db.unsubscribe_alert(user_id, alert_type)
    
    await callback.answer("❌ All alerts disabled")
    try:
        await callback.message.edit_reply_markup(reply_markup=alerts_keyboard(set()))
    except Exception:
        pass
