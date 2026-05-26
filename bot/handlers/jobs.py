"""
Jobs Handlers
=============
/jobs, /cmjobs, /modjobs, /nftjobs, /tester
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.jobs_scraper import get_all_cm_jobs, get_all_mod_jobs, get_nft_jobs, get_tester_jobs
from bot.services.formatter import format_jobs_message, format_job_card

router = Router()


def job_actions_keyboard(job_type: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Refresh", callback_data=f"cmd_{job_type}"),
            InlineKeyboardButton(text="✉️ Write DM", callback_data="menu_outreach_kol"),
        ],
        [
            InlineKeyboardButton(text="👥 CM Jobs", callback_data="cmd_cmjobs"),
            InlineKeyboardButton(text="🛡️ Mod Jobs", callback_data="cmd_modjobs"),
        ],
        [
            InlineKeyboardButton(text="🎨 NFT Jobs", callback_data="cmd_nftjobs"),
            InlineKeyboardButton(text="🧪 Tester", callback_data="cmd_tester"),
        ],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("jobs"))
async def cmd_jobs(message: Message):
    """Show all Web3 jobs."""
    await message.answer("🔍 <i>Scanning Web3 job boards...</i>", parse_mode="HTML")
    
    # Aggregate from multiple sources
    cm_jobs = await get_all_cm_jobs()
    mod_jobs = await get_all_mod_jobs()
    
    all_jobs = (cm_jobs + mod_jobs)[:15]
    
    msg = format_jobs_message(all_jobs, "ALL WEB3 JOBS")
    
    await message.answer(
        msg,
        parse_mode="HTML",
        reply_markup=job_actions_keyboard("jobs"),
        disable_web_page_preview=True
    )


@router.message(Command("cmjobs"))
async def cmd_cm_jobs(message: Message):
    """Show Community Manager jobs."""
    await message.answer("👥 <i>Finding CM opportunities...</i>", parse_mode="HTML")
    
    jobs = await get_all_cm_jobs()
    
    if jobs:
        msg = format_jobs_message(jobs, "COMMUNITY MANAGER JOBS 👥")
    else:
        msg = (
            "👥 <b>COMMUNITY MANAGER JOBS</b>\n"
            "━" * 28 + "\n\n"
            "⚠️ Job boards are temporarily slow. Here are the best places to find CM roles:\n\n"
            "🎯 <b>BEST CM JOB SOURCES</b>\n"
            "• cryptojobslist.com/community-manager\n"
            "• web3.career/community-manager-jobs\n"
            "• remote3.co/web3-jobs\n"
            "• LinkedIn → Web3 Community Manager\n"
            "• Telegram: @web3_jobs_channel\n\n"
            "📋 <b>HOW TO STAND OUT</b>\n"
            "• Show your Discord/Telegram stats\n"
            "• Highlight past community growth numbers\n"
            "• Include raid/engagement examples\n"
            "• Use /outreach to write custom DMs\n\n"
            "⚡ <i>Use /outreach [project] to write a custom application DM</i>"
        )
    
    await message.answer(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 CryptoJobsList", url="https://cryptojobslist.com/community-manager"),
                InlineKeyboardButton(text="🌐 web3.career", url="https://web3.career/community-manager-jobs"),
            ],
            [
                InlineKeyboardButton(text="✉️ Write DM", callback_data="menu_outreach_kol"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_cmjobs"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("modjobs"))
async def cmd_mod_jobs(message: Message):
    """Show Moderator jobs."""
    await message.answer("🛡️ <i>Finding moderator openings...</i>", parse_mode="HTML")
    
    jobs = await get_all_mod_jobs()
    
    if jobs:
        msg = format_jobs_message(jobs, "MODERATOR JOBS 🛡️")
    else:
        msg = (
            "🛡️ <b>MODERATOR OPPORTUNITIES</b>\n"
            "━" * 28 + "\n\n"
            "🎯 <b>WHERE TO FIND MOD ROLES</b>\n\n"
            "1. 📡 <b>Telegram Groups</b>\n"
            "   • Join new project groups early\n"
            "   • Be active, helpful, professional\n"
            "   • DM admins after proving yourself\n\n"
            "2. 💬 <b>Discord Communities</b>\n"
            "   • Apply in #mod-applications channels\n"
            "   • Engage in new server launches\n\n"
            "3. 🐦 <b>Twitter/X</b>\n"
            "   • Search 'looking for moderator Web3'\n"
            "   • Follow project launch announcements\n\n"
            "4. 💼 <b>Job Boards</b>\n"
            "   • cryptojobslist.com/moderator\n"
            "   • web3.career/discord-moderator-jobs\n\n"
            "💡 Use /outreach to write a mod application DM!"
        )
    
    await message.answer(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 CryptoJobsList", url="https://cryptojobslist.com/moderator"),
                InlineKeyboardButton(text="✉️ Write DM", callback_data="menu_outreach_kol"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("nftjobs"))
async def cmd_nft_jobs(message: Message):
    """Show NFT art/design jobs."""
    await message.answer("🎨 <i>Finding NFT art opportunities...</i>", parse_mode="HTML")
    
    jobs = await get_nft_jobs()
    
    lines = ["🎨 <b>NFT & CREATIVE GIGS</b>", "━" * 28, ""]
    
    if jobs:
        for i, job in enumerate(jobs[:8], 1):
            lines.append(format_job_card(job, i))
            lines.append("")
    
    lines.extend([
        "━" * 28,
        "🎯 <b>BEST NFT GIG PLATFORMS</b>",
        "• Foundation.app — Premium NFT marketplace",
        "• SuperRare — Curated digital art",
        "• Manifold.xyz — Creator tools + collab",
        "• Zora — Open NFT creation",
        "• Magic Eden — Solana/ETH/Base NFTs",
        "",
        "💡 <b>HOW TO GET NFT GIGS</b>",
        "• Post your portfolio on Twitter with #NFTArt",
        "• Engage with project founders early",
        "• DM with your art before they announce artist search",
        "• Join NFT artist Discord servers",
        "",
        "⚡ <i>Use /outreach to write pitch DMs for NFT collabs</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Foundation", url="https://foundation.app"),
                InlineKeyboardButton(text="🪄 Magic Eden", url="https://magiceden.io"),
            ],
            [
                InlineKeyboardButton(text="✉️ Pitch DM", callback_data="menu_outreach_kol"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_nftjobs"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("tester"))
async def cmd_tester(message: Message):
    """Show protocol testing opportunities."""
    await message.answer("🧪 <i>Finding testing opportunities...</i>", parse_mode="HTML")
    
    jobs = await get_tester_jobs()
    
    lines = ["🧪 <b>PROTOCOL TESTING & BUG BOUNTIES</b>", "━" * 28, ""]
    
    if jobs:
        for i, job in enumerate(jobs[:5], 1):
            lines.append(format_job_card(job, i))
            lines.append("")
    
    lines.extend([
        "━" * 28,
        "🎯 <b>HOW TO BECOME A WEB3 TESTER</b>",
        "",
        "🐛 <b>Bug Bounties (Paid)</b>",
        "• Immunefi.com — Biggest crypto bug bounties",
        "• Code4rena.com — Audit contests",
        "• Sherlock.xyz — Security competitions",
        "",
        "🧪 <b>Testnet Programs</b>",
        "• Follow project Twitter for testnet announcements",
        "• Join Discord for test tasks",
        "• Document bugs professionally",
        "• Build reputation = get hired for mainnet",
        "",
        "📝 <b>What Testers Do</b>",
        "• Test new DeFi protocols before launch",
        "• Report UI/UX bugs and smart contract issues",
        "• Complete test transactions and flows",
        "• Write detailed bug reports",
        "• Earn rewards in tokens or USD",
        "",
        "⚡ <i>Start with testnet programs — they're completely free to join</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🐛 Immunefi", url="https://immunefi.com"),
                InlineKeyboardButton(text="🏆 Code4rena", url="https://code4rena.com"),
            ],
            [
                InlineKeyboardButton(text="🔒 Sherlock", url="https://sherlock.xyz"),
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_tester"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


# ─── Callback handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "cmd_jobs")
async def cb_jobs(callback: CallbackQuery):
    await callback.answer("Loading all jobs...")
    await cmd_jobs(callback.message)


@router.callback_query(F.data == "cmd_cmjobs")
async def cb_cm_jobs(callback: CallbackQuery):
    await callback.answer("Loading CM jobs...")
    await cmd_cm_jobs(callback.message)


@router.callback_query(F.data == "cmd_modjobs")
async def cb_mod_jobs(callback: CallbackQuery):
    await callback.answer("Loading mod jobs...")
    await cmd_mod_jobs(callback.message)


@router.callback_query(F.data == "cmd_nftjobs")
async def cb_nft_jobs(callback: CallbackQuery):
    await callback.answer("Loading NFT jobs...")
    await cmd_nft_jobs(callback.message)


@router.callback_query(F.data == "cmd_tester")
async def cb_tester(callback: CallbackQuery):
    await callback.answer("Loading tester gigs...")
    await cmd_tester(callback.message)
