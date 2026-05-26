"""
Project Analysis Handlers
=========================
/checkproject, /analyze commands
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.project_analyzer import full_analysis
from bot.services.ai_service import analyze_project_ai

router = Router()


def analysis_keyboard(project: str = "") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🔬 Re-analyze", callback_data=f"reanalyze"),
            InlineKeyboardButton(text="💾 Save", callback_data=f"save_project"),
        ],
        [
            InlineKeyboardButton(text="📋 Add to Watchlist", callback_data="add_watchlist"),
            InlineKeyboardButton(text="📬 Write Outreach", callback_data="menu_outreach_kol"),
        ],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("checkproject"))
async def cmd_check_project(message: Message):
    """Quick project analysis."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "🔬 <b>PROJECT ANALYZER</b>\n"
            "━" * 25 + "\n\n"
            "Send me anything to analyze:\n\n"
            "📍 <b>Token Address</b>\n"
            "<code>/checkproject 0x1234...abcd</code>\n\n"
            "🌐 <b>Website URL</b>\n"
            "<code>/checkproject https://example.com</code>\n\n"
            "🐦 <b>Twitter Handle</b>\n"
            "<code>/checkproject @projecthandle</code>\n\n"
            "📝 <b>Project Name</b>\n"
            "<code>/checkproject PepeCoin meme token on Solana</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")]
            ])
        )
        return
    
    user_input = parts[1].strip()
    
    scanning_msg = await message.answer(
        "⚡ <i>Running project analysis...</i>\n"
        "<i>Checking DexScreener, scanning website, running AI audit...</i>",
        parse_mode="HTML"
    )
    
    try:
        result = await full_analysis(user_input)
        await scanning_msg.delete()
        
        # Split long messages
        if len(result) > 4000:
            result = result[:3990] + "\n<i>...truncated</i>"
        
        await message.answer(
            result,
            parse_mode="HTML",
            reply_markup=analysis_keyboard(user_input),
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await scanning_msg.delete()
        await message.answer(
            f"❌ Analysis failed: {str(e)[:200]}\n\nTry again or use /ai for manual analysis.",
            parse_mode="HTML"
        )


@router.message(Command("analyze"))
async def cmd_analyze(message: Message):
    """Deep AI analysis of any project."""
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "🔬 <b>DEEP AI ANALYZER</b>\n"
            "━" * 25 + "\n\n"
            "I'll run a comprehensive AI-powered analysis.\n\n"
            "You can send:\n"
            "• Token address or name\n"
            "• Project website URL\n"
            "• Paste their whitepaper summary\n"
            "• Twitter/Telegram description\n"
            "• Anything about the project\n\n"
            "<code>/analyze [project info here]</code>",
            parse_mode="HTML"
        )
        return
    
    project_info = parts[1].strip()
    
    thinking_msg = await message.answer(
        "🤖 <i>Running deep AI analysis...</i>\n"
        "<i>Groq → OpenRouter → Gemini (auto-fallback)</i>",
        parse_mode="HTML"
    )
    
    try:
        # First run the automated analysis
        auto_result = await full_analysis(project_info)
        
        # Then get deeper AI analysis
        ai_result, model = await analyze_project_ai(
            f"Analyze this project thoroughly: {project_info}"
        )
        
        await thinking_msg.delete()
        
        # Send automated analysis first
        await message.answer(
            auto_result,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        
        # Then send AI deep dive
        if ai_result and ai_result != auto_result:
            ai_msg = (
                f"━" * 28 + "\n"
                f"🤖 <b>AI DEEP DIVE</b> <i>({model})</i>\n"
                f"━" * 28 + "\n\n"
                f"{ai_result}"
            )
            
            if len(ai_msg) > 4000:
                ai_msg = ai_msg[:3990] + "..."
            
            await message.answer(
                ai_msg,
                parse_mode="HTML",
                reply_markup=analysis_keyboard(project_info),
                disable_web_page_preview=True
            )
        
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Error: {str(e)[:200]}", parse_mode="HTML")


@router.callback_query(F.data == "menu_analyze")
async def cb_analyze_menu(callback: CallbackQuery):
    await callback.message.answer(
        "🔬 <b>PROJECT ANALYZER</b>\n"
        "━" * 25 + "\n\n"
        "Send me anything to analyze:\n"
        "• <code>/checkproject [address/url/handle]</code>\n"
        "• <code>/analyze [project description]</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "reanalyze")
async def cb_reanalyze(callback: CallbackQuery):
    await callback.answer("Send /checkproject [input] to re-analyze!")


@router.callback_query(F.data == "save_project")
async def cb_save_project(callback: CallbackQuery):
    await callback.answer("Use /save [project details] to save this!")


@router.callback_query(F.data == "add_watchlist")
async def cb_add_watchlist(callback: CallbackQuery):
    await callback.answer("Use /watchlist add [project] to track it!")
    await callback.message.answer(
        "📋 To add to watchlist:\n<code>/save [project name and details]</code>",
        parse_mode="HTML"
    )
