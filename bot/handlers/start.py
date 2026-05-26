"""
Start & Help Handlers
=====================
/start, /help commands and main menu.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database as db
from bot.services.formatter import format_welcome, format_help_message

router = Router()


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Build the main menu inline keyboard."""
    buttons = [
        [
            InlineKeyboardButton(text="🔍 Alpha", callback_data="menu_alpha"),
            InlineKeyboardButton(text="💼 Jobs", callback_data="menu_jobs"),
            InlineKeyboardButton(text="🤖 AI Chat", callback_data="menu_ai"),
        ],
        [
            InlineKeyboardButton(text="🔬 Analyze", callback_data="menu_analyze"),
            InlineKeyboardButton(text="📬 Outreach", callback_data="menu_outreach"),
            InlineKeyboardButton(text="🗂️ Organizer", callback_data="menu_organizer"),
        ],
        [
            InlineKeyboardButton(text="⛓️ Chains", callback_data="menu_chains"),
            InlineKeyboardButton(text="🔔 Alerts", callback_data="menu_alerts"),
            InlineKeyboardButton(text="⚙️ Settings", callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton(text="📋 Full Help", callback_data="menu_help"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def alpha_submenu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="⚡ Trending", callback_data="cmd_trending"),
            InlineKeyboardButton(text="🆕 New", callback_data="cmd_newprojects"),
        ],
        [
            InlineKeyboardButton(text="🎭 Memecoins", callback_data="cmd_memecoins"),
            InlineKeyboardButton(text="🪂 Airdrops", callback_data="cmd_airdrops"),
        ],
        [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def jobs_submenu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="👥 CM Jobs", callback_data="cmd_cmjobs"),
            InlineKeyboardButton(text="🛡️ Mod Jobs", callback_data="cmd_modjobs"),
        ],
        [
            InlineKeyboardButton(text="🎨 NFT Jobs", callback_data="cmd_nftjobs"),
            InlineKeyboardButton(text="🧪 Tester", callback_data="cmd_tester"),
        ],
        [
            InlineKeyboardButton(text="🌐 All Jobs", callback_data="cmd_jobs"),
        ],
        [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def chains_submenu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="◎ Solana", callback_data="cmd_solana"),
            InlineKeyboardButton(text="🔵 Base", callback_data="cmd_base"),
            InlineKeyboardButton(text="⟠ Ethereum", callback_data="cmd_eth"),
        ],
        [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def outreach_submenu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✉️ KOL DM", callback_data="menu_outreach_kol"),
            InlineKeyboardButton(text="⚔️ Raid Msg", callback_data="menu_outreach_raid"),
        ],
        [
            InlineKeyboardButton(text="📢 Shill", callback_data="menu_outreach_shill"),
            InlineKeyboardButton(text="🤝 Network", callback_data="cmd_network"),
        ],
        [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    user = message.from_user
    await db.upsert_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "Anon"
    )
    
    # Subscribe to default alerts
    for alert_type in ["alpha", "trending"]:
        await db.subscribe_alert(user.id, alert_type)
    
    welcome_text = format_welcome(user.first_name or "Operator")
    
    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(
        format_help_message(),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu_main")]
        ])
    )


# ─── Callback Handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_main")
async def cb_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        format_welcome(callback.from_user.first_name or "Operator"),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery):
    await callback.message.edit_text(
        format_help_message(),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu_main")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "menu_alpha")
async def cb_alpha_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔍 <b>ALPHA HUNTING</b>\n━━━━━━━━━━━━━━━\n\nWhat are you hunting for today?",
        parse_mode="HTML",
        reply_markup=alpha_submenu()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_jobs")
async def cb_jobs_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "💼 <b>WEB3 JOB HUNTING</b>\n━━━━━━━━━━━━━━━\n\nSelect your specialty:",
        parse_mode="HTML",
        reply_markup=jobs_submenu()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_chains")
async def cb_chains_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "⛓️ <b>ECOSYSTEM EXPLORER</b>\n━━━━━━━━━━━━━━━\n\nSelect a blockchain ecosystem:",
        parse_mode="HTML",
        reply_markup=chains_submenu()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_outreach")
async def cb_outreach_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📬 <b>OUTREACH & CONTENT</b>\n━━━━━━━━━━━━━━━\n\nWhat do you need to write?",
        parse_mode="HTML",
        reply_markup=outreach_submenu()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_ai")
async def cb_ai_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🤖 <b>AI ASSISTANT</b>\n━━━━━━━━━━━━━━━\n\n"
        "Send me any message and I'll respond!\n\n"
        "Or use <code>/ai [your question]</code>\n\n"
        "<i>Powered by Groq → OpenRouter → Gemini → DeepSeek (auto-fallback)</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "menu_analyze")
async def cb_analyze_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔬 <b>PROJECT ANALYZER</b>\n━━━━━━━━━━━━━━━\n\n"
        "Send me any of these to analyze:\n"
        "• Token contract address\n"
        "• Project website URL\n"
        "• Twitter/X handle (@...)\n"
        "• Project name or description\n\n"
        "Use: <code>/checkproject [input]</code>\n"
        "Or: <code>/analyze [input]</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "menu_organizer")
async def cb_organizer_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🗂️ <b>PERSONAL ORGANIZER</b>\n━━━━━━━━━━━━━━━\n\n"
        "📌 /reminder [time] [message]\n"
        "Example: /reminder 2h check alpha\n\n"
        "👁️ /watchlist — Track projects\n"
        "💾 /save [text] — Save notes\n"
        "📝 /notes — View all notes",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Notes", callback_data="cmd_notes"),
             InlineKeyboardButton(text="👁️ Watchlist", callback_data="cmd_watchlist")],
            [InlineKeyboardButton(text="◀️ Back", callback_data="menu_main")],
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "menu_alerts")
async def cb_alerts_menu(callback: CallbackQuery):
    from bot.handlers.settings import alerts_keyboard
    user_id = callback.from_user.id
    user_alerts = await db.get_user_alerts(user_id)
    
    active = {a["alert_type"] for a in user_alerts if a["is_active"]}
    
    await callback.message.edit_text(
        "🔔 <b>ALERT SUBSCRIPTIONS</b>\n━━━━━━━━━━━━━━━\n\n"
        "Toggle which alerts you want to receive:",
        parse_mode="HTML",
        reply_markup=alerts_keyboard(active)
    )
    await callback.answer()


@router.callback_query(F.data == "menu_settings")
async def cb_settings(callback: CallbackQuery):
    from bot.handlers.settings import cmd_settings
    await cmd_settings(callback.message)
    await callback.answer()
