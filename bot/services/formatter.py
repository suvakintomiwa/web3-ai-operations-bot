"""
Message Formatter
=================
Creates beautiful Telegram-formatted messages with cyberpunk styling.
"""
from datetime import datetime


# ─── Formatting Helpers ────────────────────────────────────────────────────────

def sep(length: int = 28, char: str = "━") -> str:
    return char * length


def header(title: str, emoji: str = "⚡") -> str:
    return f"{emoji} <b>{title}</b>\n{sep()}"


def format_number(n: float, decimals: int = 2) -> str:
    if n >= 1_000_000_000:
        return f"${n/1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    elif n >= 1_000:
        return f"${n/1_000:.1f}K"
    elif n >= 1:
        return f"${n:.{decimals}f}"
    elif n > 0:
        return f"${n:.8f}"
    return "$0"


def format_change(pct: float) -> str:
    if pct > 0:
        return f"🟢 +{pct:.2f}%"
    elif pct < 0:
        return f"🔴 {pct:.2f}%"
    return f"⚪ {pct:.2f}%"


def format_chain_emoji(chain: str) -> str:
    chains = {
        "solana": "◎",
        "ethereum": "⟠",
        "bsc": "🟡",
        "base": "🔵",
        "arbitrum": "💙",
        "polygon": "💜",
        "avalanche": "🔺",
        "optimism": "❤️",
    }
    return chains.get(chain.lower(), "🔗")


def format_risk_bar(score: int) -> str:
    filled = int(score / 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty
    
    if score <= 25:
        color = "🟢"
    elif score <= 50:
        color = "🟡"
    elif score <= 75:
        color = "🟠"
    else:
        color = "🔴"
    
    return f"{color} [{bar}] {score}/100"


# ─── Alpha / Token Formatters ──────────────────────────────────────────────────

def format_token_card(token: dict, rank: int = 0) -> str:
    """Format a single token card for display."""
    chain_emoji = format_chain_emoji(token.get("chain", ""))
    name = token.get("name", "Unknown")
    symbol = token.get("symbol", "?")
    mc = token.get("market_cap", 0)
    liq = token.get("liquidity_usd", 0)
    vol = token.get("volume_24h", 0)
    change_24h = token.get("change_24h", 0)
    change_1h = token.get("change_1h", 0)
    url = token.get("url", "")
    
    rank_prefix = f"#{rank} " if rank else ""
    
    lines = [
        f"{'━'*25}",
        f"{rank_prefix}{chain_emoji} <b>{name}</b> <code>${symbol}</code>",
        f"💰 MC: {format_number(mc)}  |  💧 Liq: {format_number(liq)}",
        f"📊 Vol 24h: {format_number(vol)}",
        f"1h: {format_change(change_1h)}  |  24h: {format_change(change_24h)}",
    ]
    
    if url:
        lines.append(f"🔗 <a href='{url}'>DexScreener</a>")
    
    return "\n".join(lines)


def format_trending_message(tokens: list, title: str = "TRENDING NOW") -> str:
    """Format a list of trending tokens."""
    if not tokens:
        return f"⚠️ No trending tokens found right now. Try again in a few minutes."
    
    lines = [header(title, "🔥"), ""]
    
    for i, token in enumerate(tokens[:8], 1):
        lines.append(format_token_card(token, i))
        lines.append("")
    
    lines.append(f"⏰ <i>Updated: {datetime.utcnow().strftime('%H:%M UTC')}</i>")
    lines.append(f"⚡ <i>Powered by DexScreener · NexusBot</i>")
    
    return "\n".join(lines)


# ─── Job Formatters ────────────────────────────────────────────────────────────

def format_job_card(job: dict, rank: int = 0) -> str:
    """Format a single job listing."""
    rank_prefix = f"#{rank} " if rank else ""
    remote_badge = "🌐 Remote" if job.get("remote") else "📍 On-site"
    
    return (
        f"{'━'*25}\n"
        f"{rank_prefix}💼 <b>{job.get('title', 'Unknown Role')}</b>\n"
        f"🏢 {job.get('company', 'Anonymous')}\n"
        f"{remote_badge}  |  📡 {job.get('source', 'Web3')}\n"
        f"🔗 <a href='{job.get('url', '#')}'>Apply Now →</a>"
    )


def format_jobs_message(jobs: list, title: str = "WEB3 JOBS") -> str:
    """Format a list of jobs."""
    if not jobs:
        return f"⚠️ No jobs found right now. Check back later or try a different category."
    
    lines = [header(title, "💼"), ""]
    
    for i, job in enumerate(jobs[:10], 1):
        lines.append(format_job_card(job, i))
        lines.append("")
    
    lines.extend([
        sep(),
        f"📊 <b>{len(jobs)} opportunities found</b>",
        f"⏰ <i>Updated: {datetime.utcnow().strftime('%H:%M UTC')}</i>",
        f"",
        f"💡 Use /outreach to generate custom application DMs",
    ])
    
    return "\n".join(lines)


# ─── Welcome / Menu Formatters ─────────────────────────────────────────────────

def format_welcome(first_name: str) -> str:
    return f"""⚡ <b>NEXUSBOT ONLINE</b>
{sep(30)}
👋 Welcome, <b>{first_name}</b>!

Your personal <b>Web3 AI Assistant</b> is ready.
Built for crypto operators who play to win. 🏆

<b>🎯 QUICK ACTIONS:</b>
• /alpha — Find trending gems
• /cmjobs — CM job opportunities  
• /ai — Chat with AI assistant
• /checkproject — Analyze any project
• /help — Full command reference

{sep(30)}
<i>All systems operational. Free AI powered by Groq → OpenRouter → Gemini → DeepSeek</i>

⚡ <i>NexusBot v1.0 · Railway · SQLite · 100% Free</i>"""


def format_help_message() -> str:
    return """⚡ <b>NEXUSBOT COMMAND REFERENCE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 <b>ALPHA HUNTING</b>
/alpha — Top trending tokens
/newprojects — New launches today
/trending — What's pumping now
/memecoins — Fresh meme coins
/airdrops — Active airdrops
/solana — Solana ecosystem
/base — Base chain projects
/eth — Ethereum ecosystem

💼 <b>JOB HUNTING</b>
/jobs — All Web3 jobs
/cmjobs — Community Manager roles
/modjobs — Moderator openings
/nftjobs — NFT art gigs
/tester — Protocol testing

🔬 <b>PROJECT ANALYSIS</b>
/checkproject [input] — Quick analysis
/analyze [input] — Deep AI analysis

📬 <b>OUTREACH & CONTENT</b>
/outreach [project] — KOL DM writer
/raid [project] — Raid messages
/shill [project] — Shill threads
/network — Contact manager

🗂️ <b>ORGANIZER</b>
/reminder [time] [msg] — Set reminder
/watchlist — View tracked projects
/save [text] — Save note/link
/notes — View all notes

🤖 <b>AI ASSISTANT</b>
/ai [prompt] — Chat with AI
/settings — Configure preferences
/alerts — Manage push alerts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ <i>NexusBot · Powered by free AI · 0$ cost</i>"""


def format_watchlist(items: list) -> str:
    if not items:
        return (
            "📋 <b>YOUR WATCHLIST</b>\n"
            f"{sep()}\n\n"
            "Your watchlist is empty.\n\n"
            "Add projects with:\n"
            "• /save + project info\n"
            "• Forward any token analysis to save it"
        )
    
    lines = [header("YOUR WATCHLIST 🎯"), ""]
    for i, item in enumerate(items, 1):
        chain_emoji = format_chain_emoji(item.get("chain", ""))
        lines.extend([
            f"{i}. {chain_emoji} <b>{item['project']}</b>",
            f"   {item.get('notes', 'No notes') or 'No notes'}",
            f"   <code>ID: {item['id']}</code> | {item['added_at'][:10]}",
            "",
        ])
    
    lines.append("Use /watchlist remove [ID] to remove an item")
    return "\n".join(lines)


def format_notes(notes: list) -> str:
    if not notes:
        return (
            "📝 <b>YOUR NOTES</b>\n"
            f"{sep()}\n\n"
            "No notes yet.\n\n"
            "Save anything with /save [text]"
        )
    
    lines = [header("YOUR NOTES 📝"), ""]
    for note in notes:
        lines.extend([
            f"{'━'*20}",
            f"<code>#{note['id']}</code> · {note['created_at'][:16]}",
            f"{note['content'][:200]}{'...' if len(note['content']) > 200 else ''}",
            "",
        ])
    
    lines.append("Delete with: /notes delete [ID]")
    return "\n".join(lines)
