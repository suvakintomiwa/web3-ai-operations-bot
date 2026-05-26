"""
Personal Organizer Handlers
============================
/reminder, /watchlist, /save, /notes
"""
import re
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database as db
from bot.services.formatter import format_watchlist, format_notes

router = Router()


def parse_time_delta(time_str: str) -> timedelta | None:
    """Parse time string like '2h', '30m', '1d' into timedelta."""
    time_str = time_str.lower().strip()
    
    patterns = [
        (r"(\d+)s", "seconds"),
        (r"(\d+)m(?:in)?", "minutes"),
        (r"(\d+)h(?:r|ours?)?", "hours"),
        (r"(\d+)d(?:ay)?", "days"),
        (r"(\d+)w(?:eek)?", "weeks"),
    ]
    
    for pattern, unit in patterns:
        match = re.match(pattern, time_str)
        if match:
            amount = int(match.group(1))
            return timedelta(**{unit: amount})
    
    return None


@router.message(Command("reminder"))
async def cmd_reminder(message: Message):
    """Set a reminder."""
    text = message.text.strip()
    parts = text.split(maxsplit=2)
    
    if len(parts) < 3:
        await message.answer(
            "⏰ <b>REMINDER SETTER</b>\n"
            "━" * 25 + "\n\n"
            "Set reminders with natural time formats:\n\n"
            "<b>Usage:</b>\n"
            "<code>/reminder [time] [message]</code>\n\n"
            "<b>Time formats:</b>\n"
            "• <code>30m</code> — 30 minutes\n"
            "• <code>2h</code> — 2 hours\n"
            "• <code>1d</code> — 1 day\n"
            "• <code>1w</code> — 1 week\n\n"
            "<b>Examples:</b>\n"
            "<code>/reminder 2h check alpha channel</code>\n"
            "<code>/reminder 30m follow up with DeFi project</code>\n"
            "<code>/reminder 1d apply for CM job at XYZ</code>",
            parse_mode="HTML"
        )
        return
    
    time_str = parts[1]
    reminder_msg = parts[2]
    
    delta = parse_time_delta(time_str)
    
    if not delta:
        await message.answer(
            f"❌ Couldn't parse time: <code>{time_str}</code>\n\n"
            "Use: 30m, 2h, 1d, 1w",
            parse_mode="HTML"
        )
        return
    
    remind_at = datetime.utcnow() + delta
    reminder_id = await db.add_reminder(message.from_user.id, reminder_msg, remind_at)
    
    # Format the reminder time nicely
    if delta.total_seconds() < 3600:
        time_display = f"{int(delta.total_seconds() / 60)} minutes"
    elif delta.total_seconds() < 86400:
        time_display = f"{int(delta.total_seconds() / 3600)} hours"
    else:
        time_display = f"{int(delta.total_seconds() / 86400)} days"
    
    await message.answer(
        f"⏰ <b>REMINDER SET!</b>\n"
        f"━" * 25 + f"\n\n"
        f"📌 <b>Message:</b> {reminder_msg}\n"
        f"⏱️ <b>In:</b> {time_display}\n"
        f"🕐 <b>At:</b> {remind_at.strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"🆔 <b>ID:</b> #{reminder_id}\n\n"
        f"<i>I'll ping you when it's time! ✅</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")]
        ])
    )


@router.message(Command("watchlist"))
async def cmd_watchlist(message: Message):
    """View and manage watchlist."""
    text = message.text.strip()
    parts = text.split(maxsplit=2)
    user_id = message.from_user.id
    
    # Handle subcommands
    if len(parts) >= 2:
        sub = parts[1].lower()
        
        if sub == "add" and len(parts) >= 3:
            project = parts[2]
            item_id = await db.add_to_watchlist(user_id, project)
            await message.answer(
                f"✅ <b>Added to Watchlist!</b>\n\n"
                f"📋 <b>{project}</b>\n"
                f"🆔 ID: #{item_id}\n\n"
                f"<i>Use /watchlist to view all tracked projects</i>",
                parse_mode="HTML"
            )
            return
        
        elif sub == "remove" and len(parts) >= 3:
            try:
                item_id = int(parts[2].lstrip("#"))
                await db.remove_from_watchlist(item_id, user_id)
                await message.answer(f"✅ Item #{item_id} removed from watchlist.")
            except ValueError:
                await message.answer("❌ Invalid ID. Use: /watchlist remove [number]")
            return
    
    # Show watchlist
    items = await db.get_watchlist(user_id)
    msg = format_watchlist(items)
    
    await message.answer(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add Project", callback_data="cmd_watchlist_add"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_watchlist"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ])
    )


@router.message(Command("save"))
async def cmd_save(message: Message):
    """Save a note or link."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "💾 <b>SAVE ANYTHING</b>\n"
            "━" * 25 + "\n\n"
            "Save notes, links, addresses, or any text.\n\n"
            "<b>Usage:</b>\n"
            "<code>/save [anything]</code>\n\n"
            "<b>Examples:</b>\n"
            "<code>/save https://newproject.io — alpha find!</code>\n"
            "<code>/save 0x1234abcd — potential gem, check later</code>\n"
            "<code>/save @CMlead at ProjectX — good contact</code>",
            parse_mode="HTML"
        )
        return
    
    content = parts[1]
    user_id = message.from_user.id
    
    # Auto-detect tags
    tags = []
    if "http" in content.lower():
        tags.append("link")
    if "0x" in content or any(c in content for c in ["solana", "sol", "base", "eth"]):
        tags.append("crypto")
    if "@" in content:
        tags.append("contact")
    
    note_id = await db.save_note(user_id, content, ",".join(tags))
    
    await message.answer(
        f"✅ <b>SAVED!</b>\n"
        f"━" * 25 + f"\n\n"
        f"📝 <code>{content[:200]}</code>\n\n"
        f"🏷️ Tags: {', '.join(tags) if tags else 'none'}\n"
        f"🆔 Note ID: #{note_id}\n\n"
        f"<i>View all notes with /notes</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 View Notes", callback_data="cmd_notes"),
                InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main"),
            ]
        ])
    )


@router.message(Command("notes"))
async def cmd_notes(message: Message):
    """View all saved notes."""
    text = message.text.strip()
    parts = text.split(maxsplit=2)
    user_id = message.from_user.id
    
    # Handle delete subcommand
    if len(parts) >= 2 and parts[1].lower() == "delete":
        if len(parts) >= 3:
            try:
                note_id = int(parts[2].lstrip("#"))
                await db.delete_note(note_id, user_id)
                await message.answer(f"✅ Note #{note_id} deleted.")
            except ValueError:
                await message.answer("❌ Invalid ID. Use: /notes delete [number]")
        else:
            await message.answer("Usage: /notes delete [ID]")
        return
    
    # Show all notes
    notes = await db.get_notes(user_id, limit=15)
    msg = format_notes(notes)
    
    await message.answer(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Save New", callback_data="cmd_save_prompt"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_notes"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ])
    )


# ─── Callback Handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "cmd_watchlist")
async def cb_watchlist(callback: CallbackQuery):
    user_id = callback.from_user.id
    items = await db.get_watchlist(user_id)
    msg = format_watchlist(items)
    await callback.message.edit_text(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add", callback_data="cmd_watchlist_add"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_watchlist"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ])
    )
    await callback.answer("Watchlist refreshed!")


@router.callback_query(F.data == "cmd_watchlist_add")
async def cb_watchlist_add(callback: CallbackQuery):
    await callback.message.answer(
        "➕ <b>Add to Watchlist</b>\n\n"
        "Usage: <code>/watchlist add [project name]</code>\n\n"
        "Example: <code>/watchlist add $DEGEN Base chain memecoin</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "cmd_notes")
async def cb_notes(callback: CallbackQuery):
    user_id = callback.from_user.id
    notes = await db.get_notes(user_id, limit=15)
    msg = format_notes(notes)
    
    try:
        await callback.message.edit_text(
            msg,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="➕ Save New", callback_data="cmd_save_prompt"),
                    InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_notes"),
                ],
                [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
            ])
        )
    except Exception:
        await callback.message.answer(msg, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "cmd_save_prompt")
async def cb_save_prompt(callback: CallbackQuery):
    await callback.message.answer(
        "💾 <b>Save Note</b>\n\n"
        "Usage: <code>/save [your text, link, or note]</code>\n\n"
        "Example: <code>/save https://alphaproject.io — check this out</code>",
        parse_mode="HTML"
    )
    await callback.answer()
