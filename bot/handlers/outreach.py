"""
Outreach & Content Handlers
============================
/outreach, /raid, /shill, /network
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database as db
from bot.services.ai_service import (
    generate_kol_dm, generate_raid_message, generate_shill_thread,
    generate_engagement_strategy, generate_mod_reply
)

router = Router()


@router.message(Command("outreach"))
async def cmd_outreach(message: Message):
    """Generate KOL outreach DMs."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "📬 <b>KOL OUTREACH DM WRITER</b>\n"
            "━" * 25 + "\n\n"
            "I'll write professional KOL outreach DMs for any project.\n\n"
            "<b>Usage:</b>\n"
            "<code>/outreach [project] — [your pitch]</code>\n\n"
            "<b>Examples:</b>\n"
            "<code>/outreach $PEPE2 — pitch my CM services</code>\n"
            "<code>/outreach NFT Project Alpha — offer community management</code>\n"
            "<code>/outreach @SolanaStartup — propose KOL partnership</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Back", callback_data="menu_outreach")]
            ])
        )
        return
    
    details = parts[1]
    project_name = details.split("—")[0].strip() if "—" in details else details.split("-")[0].strip()
    my_role = "Community Manager, Raid Leader, KOL Outreach Specialist with Web3 experience"
    
    thinking_msg = await message.answer("📬 <i>Writing your KOL outreach DM...</i>", parse_mode="HTML")
    
    try:
        dm = await generate_kol_dm(project_name, my_role, "Project Founder/CM Lead")
        
        await thinking_msg.delete()
        
        await message.answer(
            f"📬 <b>KOL OUTREACH DM</b>\n"
            f"━" * 25 + f"\n"
            f"Project: <b>{project_name}</b>\n"
            f"━" * 25 + f"\n\n"
            f"{dm}\n\n"
            f"━" * 25 + "\n"
            f"<i>✏️ Customize before sending! Add specific project details.</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Regenerate", callback_data=f"regen_outreach"),
                    InlineKeyboardButton(text="💾 Save DM", callback_data="save_dm"),
                ],
                [InlineKeyboardButton(text="📬 New DM", callback_data="menu_outreach_kol")],
                [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
            ])
        )
        
        # Log to outreach history
        await db.log_outreach(
            user_id=message.from_user.id,
            project=project_name,
            contact="",
            message=dm,
            platform="telegram"
        )
        
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Error: {str(e)[:200]}", parse_mode="HTML")


@router.message(Command("raid"))
async def cmd_raid(message: Message):
    """Generate raid messages."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "⚔️ <b>RAID MESSAGE GENERATOR</b>\n"
            "━" * 25 + "\n\n"
            "Generate high-energy raid messages for any project.\n\n"
            "<b>Usage:</b>\n"
            "<code>/raid [project] — [context]</code>\n\n"
            "<b>Examples:</b>\n"
            "<code>/raid $PEPE2 — Solana memecoin launching today</code>\n"
            "<code>/raid @NFTProject — mint starts in 1 hour</code>\n"
            "<code>/raid $DEGEN — Base chain, 100% fair launch</code>",
            parse_mode="HTML"
        )
        return
    
    details = parts[1]
    project_parts = details.split("—") if "—" in details else details.split("-")
    project_name = project_parts[0].strip()
    context = project_parts[1].strip() if len(project_parts) > 1 else ""
    
    thinking_msg = await message.answer("⚔️ <i>Generating raid messages...</i>", parse_mode="HTML")
    
    try:
        raid_msg = await generate_raid_message(project_name, "Solana/Base/ETH", context)
        
        await thinking_msg.delete()
        
        await message.answer(
            f"⚔️ <b>RAID MESSAGES</b>\n"
            f"━" * 25 + f"\n"
            f"Project: <b>{project_name}</b>\n"
            f"━" * 25 + f"\n\n"
            f"{raid_msg}\n\n"
            f"━" * 25 + "\n"
            f"<i>Copy and paste into your raid channel!</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Regenerate", callback_data="regen_raid"),
                    InlineKeyboardButton(text="📢 Shill Version", callback_data="regen_shill"),
                ],
                [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
            ])
        )
        
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Error: {str(e)[:200]}", parse_mode="HTML")


@router.message(Command("shill"))
async def cmd_shill(message: Message):
    """Generate shill content for Twitter/X."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "📢 <b>SHILL CONTENT GENERATOR</b>\n"
            "━" * 25 + "\n\n"
            "Create viral Twitter/X shill threads and Telegram promos.\n\n"
            "<b>Usage:</b>\n"
            "<code>/shill [project] — [details]</code>\n\n"
            "<b>Examples:</b>\n"
            "<code>/shill $DEGEN — Base chain, 100% fair launch, 10K holders</code>\n"
            "<code>/shill NFT Collection — 5555 pfp, utility-first, Solana</code>",
            parse_mode="HTML"
        )
        return
    
    details = parts[1]
    project_parts = details.split("—") if "—" in details else details.split("-")
    project_name = project_parts[0].strip()
    project_details = project_parts[1].strip() if len(project_parts) > 1 else "Exciting new Web3 project"
    
    thinking_msg = await message.answer("📢 <i>Writing viral shill content...</i>", parse_mode="HTML")
    
    try:
        shill = await generate_shill_thread(project_name, project_details)
        
        await thinking_msg.delete()
        
        await message.answer(
            f"📢 <b>SHILL THREAD</b>\n"
            f"━" * 25 + f"\n"
            f"Project: <b>{project_name}</b>\n"
            f"━" * 25 + f"\n\n"
            f"{shill}\n\n"
            f"━" * 25 + "\n"
            f"<i>🐦 Ready to paste into Twitter/X! Customize as needed.</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Regenerate", callback_data="regen_shill"),
                    InlineKeyboardButton(text="⚔️ Raid Version", callback_data="regen_raid"),
                ],
                [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
            ])
        )
        
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Error: {str(e)[:200]}", parse_mode="HTML")


@router.message(Command("network"))
async def cmd_network(message: Message):
    """View and manage outreach network."""
    user_id = message.from_user.id
    history = await db.get_outreach_history(user_id, limit=10)
    
    lines = ["🤝 <b>OUTREACH NETWORK</b>", "━" * 25, ""]
    
    if history:
        lines.append(f"📊 <b>Recent Outreach ({len(history)} entries)</b>\n")
        for entry in history:
            lines.extend([
                f"━" * 20,
                f"🎯 <b>{entry['project']}</b>",
                f"📱 {entry['platform']} | 🕐 {entry['sent_at'][:10]}",
                f"<i>{entry['message'][:100]}...</i>" if len(entry['message']) > 100 else f"<i>{entry['message']}</i>",
                "",
            ])
    else:
        lines.extend([
            "No outreach history yet.\n",
            "📬 Start outreach with:\n",
            "• /outreach [project] — Write a KOL DM",
            "• /raid [project] — Create raid messages",
            "• /shill [project] — Build Twitter content",
        ])
    
    lines.extend([
        "━" * 25,
        "💡 <b>OUTREACH TIPS</b>",
        "• Personalize every DM before sending",
        "• Follow up after 48h if no response",
        "• Track your success rate manually",
        "• Use /notes to log contact details",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📬 Write DM", callback_data="menu_outreach_kol"),
                InlineKeyboardButton(text="📝 Notes", callback_data="cmd_notes"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ])
    )


# ─── Callback Handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "cmd_network")
async def cb_network(callback: CallbackQuery):
    await callback.answer("Loading network...")
    await cmd_network(callback.message)


@router.callback_query(F.data == "menu_outreach_kol")
async def cb_outreach_kol(callback: CallbackQuery):
    await callback.message.answer(
        "📬 <b>KOL DM WRITER</b>\n━" * 1 + "\n\n"
        "Usage: <code>/outreach [project] — [your pitch]</code>\n\n"
        "Example: <code>/outreach $DEGEN — pitch my CM services, 3 years exp</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_outreach_raid")
async def cb_outreach_raid(callback: CallbackQuery):
    await callback.message.answer(
        "⚔️ <b>RAID MESSAGE WRITER</b>\n━" * 1 + "\n\n"
        "Usage: <code>/raid [project] — [context]</code>\n\n"
        "Example: <code>/raid $PEPE2 — Solana memecoin launching now</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_outreach_shill")
async def cb_outreach_shill(callback: CallbackQuery):
    await callback.message.answer(
        "📢 <b>SHILL CONTENT WRITER</b>\n━" * 1 + "\n\n"
        "Usage: <code>/shill [project] — [details]</code>\n\n"
        "Example: <code>/shill $DEGEN — Base chain, fair launch, 10K holders</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "regen_outreach")
async def cb_regen_outreach(callback: CallbackQuery):
    await callback.answer("Use /outreach [project] to generate a new DM!")


@router.callback_query(F.data == "regen_raid")
async def cb_regen_raid(callback: CallbackQuery):
    await callback.answer("Use /raid [project] to generate raid messages!")


@router.callback_query(F.data == "regen_shill")
async def cb_regen_shill(callback: CallbackQuery):
    await callback.answer("Use /shill [project] to generate shill content!")


@router.callback_query(F.data == "save_dm")
async def cb_save_dm(callback: CallbackQuery):
    await callback.answer("Use /save [dm text] to save this DM!")
