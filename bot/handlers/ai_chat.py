"""
AI Chat Handler
===============
/ai command and general message handler for AI conversation.
"""
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database as db
from bot.services.ai_service import ask_ai

router = Router()

# Track users in AI conversation mode
_ai_mode_users: set = set()


def ai_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Raid Msg", callback_data="ai_template_raid"),
            InlineKeyboardButton(text="📬 KOL DM", callback_data="ai_template_kol"),
        ],
        [
            InlineKeyboardButton(text="📢 Shill Thread", callback_data="ai_template_shill"),
            InlineKeyboardButton(text="🛡️ Mod Reply", callback_data="ai_template_mod"),
        ],
        [
            InlineKeyboardButton(text="🗑️ Clear History", callback_data="ai_clear"),
            InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main"),
        ],
    ])


@router.message(Command("ai"))
async def cmd_ai(message: Message):
    """Handle /ai command."""
    user_id = message.from_user.id
    
    # Get prompt from command args
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        # Show AI menu if no prompt given
        await message.answer(
            "🤖 <b>AI ASSISTANT READY</b>\n"
            "━" * 25 + "\n\n"
            "I can help you with:\n"
            "• Writing raid messages\n"
            "• KOL outreach DMs\n"
            "• Twitter/X shill threads\n"
            "• Project analysis\n"
            "• Community strategies\n"
            "• Mod reply templates\n\n"
            "Just send your message or use a template below!\n\n"
            "Or: <code>/ai [your question here]</code>",
            parse_mode="HTML",
            reply_markup=ai_keyboard()
        )
        # Enable conversation mode
        _ai_mode_users.add(user_id)
        return
    
    prompt = parts[1]
    
    # Show typing indicator
    thinking_msg = await message.answer("🤖 <i>Thinking...</i>", parse_mode="HTML")
    
    try:
        # Get conversation context
        context = await db.get_conversation(user_id, limit=6)
        
        # Save user message
        await db.save_message(user_id, "user", prompt)
        
        # Get AI response
        response, model = await ask_ai(prompt, context=context)
        
        # Save AI response
        await db.save_message(user_id, "assistant", response)
        
        # Delete thinking message
        await thinking_msg.delete()
        
        # Send response
        full_response = (
            f"🤖 <b>AI RESPONSE</b>\n"
            f"━" * 25 + "\n\n"
            f"{response}\n\n"
            f"{'━'*25}\n"
            f"<i>Model: {model}</i>"
        )
        
        # Split if too long for Telegram (4096 char limit)
        if len(full_response) > 4000:
            chunks = [full_response[i:i+4000] for i in range(0, len(full_response), 4000)]
            for chunk in chunks:
                await message.answer(chunk, parse_mode="HTML", reply_markup=ai_keyboard())
        else:
            await message.answer(full_response, parse_mode="HTML", reply_markup=ai_keyboard())
            
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(
            f"❌ AI error: {str(e)[:200]}\n\nTry again in a moment.",
            parse_mode="HTML"
        )


@router.message(F.text & ~F.text.startswith("/"))
async def handle_general_message(message: Message):
    """Handle non-command messages as AI conversation."""
    user_id = message.from_user.id
    
    # Only respond to AI queries if user has sent /ai before or is in AI mode
    if user_id not in _ai_mode_users:
        # Silently ignore or give hint
        return
    
    text = message.text.strip()
    if not text or len(text) < 3:
        return
    
    thinking_msg = await message.answer("🤖 <i>Processing...</i>", parse_mode="HTML")
    
    try:
        context = await db.get_conversation(user_id, limit=8)
        await db.save_message(user_id, "user", text)
        
        response, model = await ask_ai(text, context=context)
        await db.save_message(user_id, "assistant", response)
        
        await thinking_msg.delete()
        
        # Shorter format for conversation
        reply = f"{response}\n\n<i>— {model}</i>"
        
        if len(reply) > 4000:
            reply = reply[:3990] + "..."
        
        await message.answer(reply, parse_mode="HTML", reply_markup=ai_keyboard())
        
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"⚠️ {str(e)[:100]}")


# ─── AI Template Callbacks ─────────────────────────────────────────────────────

@router.callback_query(F.data == "ai_template_raid")
async def cb_ai_raid(callback: CallbackQuery):
    await callback.message.answer(
        "⚔️ <b>RAID MESSAGE GENERATOR</b>\n"
        "━" * 25 + "\n\n"
        "Tell me the project details and I'll write raid messages!\n\n"
        "Example:\n"
        "<code>/raid $PEPE2 on Solana — new memecoin with 1000x potential, launched today</code>",
        parse_mode="HTML"
    )
    _ai_mode_users.add(callback.from_user.id)
    await callback.answer()


@router.callback_query(F.data == "ai_template_kol")
async def cb_ai_kol(callback: CallbackQuery):
    await callback.message.answer(
        "📬 <b>KOL OUTREACH DM WRITER</b>\n"
        "━" * 25 + "\n\n"
        "I'll write you a professional KOL outreach DM!\n\n"
        "Example:\n"
        "<code>/outreach SolanaProjectX — pitch my CM services, 3 years experience, 50K community grown</code>",
        parse_mode="HTML"
    )
    _ai_mode_users.add(callback.from_user.id)
    await callback.answer()


@router.callback_query(F.data == "ai_template_shill")
async def cb_ai_shill(callback: CallbackQuery):
    await callback.message.answer(
        "📢 <b>SHILL THREAD WRITER</b>\n"
        "━" * 25 + "\n\n"
        "Give me the project details and I'll write a viral Twitter thread!\n\n"
        "Example:\n"
        "<code>/shill $DEGEN — Base chain memecoin, 100% fair launch, 50K Twitter followers, mooning</code>",
        parse_mode="HTML"
    )
    _ai_mode_users.add(callback.from_user.id)
    await callback.answer()


@router.callback_query(F.data == "ai_template_mod")
async def cb_ai_mod(callback: CallbackQuery):
    await callback.message.answer(
        "🛡️ <b>MODERATION REPLY WRITER</b>\n"
        "━" * 25 + "\n\n"
        "Describe the situation and I'll write a professional mod response!\n\n"
        "Example:\n"
        "<code>/ai write a mod warning for a user spamming referral links in our Telegram</code>",
        parse_mode="HTML"
    )
    _ai_mode_users.add(callback.from_user.id)
    await callback.answer()


@router.callback_query(F.data == "ai_clear")
async def cb_ai_clear(callback: CallbackQuery):
    user_id = callback.from_user.id
    await db.clear_conversation(user_id)
    await callback.answer("✅ Conversation history cleared!")
    await callback.message.answer(
        "🗑️ Conversation history cleared. Starting fresh!",
        parse_mode="HTML",
        reply_markup=ai_keyboard()
    )
