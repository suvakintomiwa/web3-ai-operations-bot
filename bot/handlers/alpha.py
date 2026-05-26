"""
Alpha Discovery Handlers
========================
/alpha, /newprojects, /trending, /memecoins, /airdrops
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.dexscreener import get_trending_tokens, get_new_pairs, format_pair
from bot.services.coingecko import get_trending_coins, get_coins_by_category, get_top_gainers, format_coin
from bot.services.formatter import format_trending_message, format_token_card, format_number, format_change

router = Router()


def alpha_actions_keyboard(context: str = "") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Refresh", callback_data=f"refresh_{context}"),
            InlineKeyboardButton(text="🤖 AI Analysis", callback_data=f"ai_analysis_{context}"),
        ],
        [
            InlineKeyboardButton(text="◎ Solana", callback_data="cmd_solana"),
            InlineKeyboardButton(text="🔵 Base", callback_data="cmd_base"),
        ],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("alpha"))
async def cmd_alpha(message: Message):
    """Show top alpha opportunities."""
    await message.answer("⚡ <i>Scanning DexScreener + CoinGecko for alpha...</i>", parse_mode="HTML")
    
    # Get data from multiple sources
    dex_pairs = await get_trending_tokens(limit=5)
    cg_coins = await get_trending_coins()
    
    lines = [
        "⚡ <b>NEXUSBOT ALPHA SCANNER</b>",
        "━" * 28,
        "",
        "🔥 <b>DEXSCREENER HOT PAIRS</b>",
        "",
    ]
    
    if dex_pairs:
        for i, pair in enumerate(dex_pairs[:4], 1):
            if isinstance(pair, dict) and "baseToken" in pair:
                token = format_pair(pair)
            else:
                token = pair
            
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "?")
            mc = token.get("market_cap", 0)
            change = token.get("change_24h", 0)
            liq = token.get("liquidity_usd", 0)
            
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>  "
                f"{format_change(change)}\n"
                f"   MC: {format_number(mc)} | Liq: {format_number(liq)}"
            )
    else:
        lines.append("⚠️ DexScreener temporarily unavailable")
    
    lines.extend(["", "━" * 28, "🌊 <b>COINGECKO TRENDING</b>", ""])
    
    if cg_coins:
        for i, coin_data in enumerate(cg_coins[:4], 1):
            coin = format_coin(coin_data)
            lines.append(
                f"{i}. <b>{coin['name']}</b> <code>${coin['symbol']}</code>  "
                f"Rank #{coin['market_cap_rank']}"
            )
    else:
        lines.append("⚠️ CoinGecko temporarily unavailable")
    
    lines.extend([
        "",
        "━" * 28,
        "💡 <b>COMMANDS</b>",
        "• /checkproject [address] — Deep analysis",
        "• /trending — Real-time trends",
        "• /newprojects — Fresh launches",
        "",
        "⚡ <i>NexusBot • DYOR • Not financial advice</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=alpha_actions_keyboard("alpha"),
        disable_web_page_preview=True
    )


@router.message(Command("trending"))
async def cmd_trending(message: Message):
    """Show what's trending right now."""
    await message.answer("📡 <i>Fetching real-time trends...</i>", parse_mode="HTML")
    
    # Get top gainers from CoinGecko
    gainers = await get_top_gainers(limit=8)
    trending = await get_trending_coins()
    
    lines = ["🔥 <b>TRENDING NOW</b>", "━" * 28, ""]
    
    if gainers:
        lines.append("📈 <b>TOP GAINERS (24H)</b>")
        for i, coin in enumerate(gainers[:5], 1):
            change = coin.get("price_change_percentage_24h", 0)
            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "?").upper()
            mc = coin.get("market_cap", 0)
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>  "
                f"<b>+{change:.1f}%</b>  MC: {format_number(mc)}"
            )
    
    lines.extend(["", "━" * 28, "🌊 <b>COINGECKO TOP TRENDING</b>", ""])
    
    if trending:
        for i, coin_data in enumerate(trending[:5], 1):
            coin = format_coin(coin_data)
            lines.append(f"{i}. <b>{coin['name']}</b> <code>${coin['symbol']}</code>  Rank #{coin['market_cap_rank']}")
    
    lines.extend([
        "",
        "⏰ <i>Live data • Updates every 10 min</i>",
        "⚡ <i>Powered by CoinGecko • NexusBot</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh_trending"),
             InlineKeyboardButton(text="🆕 New Projects", callback_data="cmd_newprojects")],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("newprojects"))
async def cmd_new_projects(message: Message):
    """Show newly launched projects."""
    await message.answer("🆕 <i>Scanning for fresh launches...</i>", parse_mode="HTML")
    
    new_pairs = await get_new_pairs(limit=8)
    new_coins_cg = await get_trending_coins()
    
    lines = ["🆕 <b>NEW PROJECT LAUNCHES</b>", "━" * 28, ""]
    
    if new_pairs:
        lines.append("⚡ <b>DEXSCREENER NEW PAIRS</b>")
        for i, pair in enumerate(new_pairs[:5], 1):
            token = format_pair(pair)
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "?")
            chain = token.get("chain", "?").upper()
            mc = token.get("market_cap", 0)
            liq = token.get("liquidity_usd", 0)
            url = token.get("url", "")
            
            created = token.get("created_at", 0)
            age = "New" if not created else _format_age(created)
            
            link = f" | <a href='{url}'>Chart</a>" if url else ""
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code> [{chain}]\n"
                f"   MC: {format_number(mc)} | Liq: {format_number(liq)} | {age}{link}"
            )
    else:
        lines.append("⚠️ No new pairs found. Try /solana or /base for chain-specific results.")
    
    lines.extend([
        "",
        "━" * 28,
        "🚨 <b>ALWAYS DYOR ON NEW PROJECTS</b>",
        "Use /checkproject [address] for risk analysis",
        "",
        "⚡ <i>NexusBot New Launch Scanner</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_newprojects"),
             InlineKeyboardButton(text="🔬 Analyze", callback_data="menu_analyze")],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("memecoins"))
async def cmd_memecoins(message: Message):
    """Show trending meme coins."""
    await message.answer("🎭 <i>Loading meme coin radar...</i>", parse_mode="HTML")
    
    memes = await get_coins_by_category("meme-token", limit=10)
    
    lines = ["🎭 <b>MEME COIN RADAR</b>", "━" * 28, ""]
    
    if memes:
        for i, coin in enumerate(memes[:8], 1):
            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "?").upper()
            mc = coin.get("market_cap", 0)
            change_24h = coin.get("price_change_percentage_24h", 0) or 0
            vol = coin.get("total_volume", 0)
            
            sentiment = "🟢" if change_24h > 5 else "🔴" if change_24h < -5 else "🟡"
            lines.append(
                f"{i}. {sentiment} <b>{name}</b> <code>${symbol}</code>\n"
                f"   MC: {format_number(mc)} | 24h: {format_change(change_24h)}\n"
                f"   Vol: {format_number(vol)}"
            )
    else:
        lines.extend([
            "⚠️ CoinGecko temporarily rate-limited.",
            "Try again in 30 seconds.",
            "",
            "Meanwhile check: https://dexscreener.com/meme",
        ])
    
    lines.extend([
        "",
        "━" * 28,
        "⚠️ <i>Meme coins are high risk — always DYOR</i>",
        "💡 Use /checkproject for any token analysis",
        "⚡ <i>Powered by CoinGecko • NexusBot</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_memecoins"),
             InlineKeyboardButton(text="🎭 Pump.fun", url="https://pump.fun")],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("airdrops"))
async def cmd_airdrops(message: Message):
    """Show airdrop opportunities."""
    lines = [
        "🪂 <b>AIRDROP OPPORTUNITIES</b>",
        "━" * 28,
        "",
        "🔥 <b>HOW TO FARM AIRDROPS</b>",
        "",
        "1️⃣ <b>LAYER 2 BRIDGES</b>",
        "• Bridge ETH to Base, Arbitrum, Optimism",
        "• Bridge SOL between Solana protocols",
        "• Interact with contracts on new L2s",
        "",
        "2️⃣ <b>TESTNET PARTICIPATION</b>",
        "• Join new protocol testnets early",
        "• Complete testnet tasks (swaps, LP)",
        "• Report bugs via GitHu",
        "",
        "3️⃣ <b>DEFI INTERACTION</b>",
        "• Provide liquidity on new AMMs",
        "• Vote in protocol governance",
        "• Use protocols before token launches",
        "",
        "4️⃣ <b>NFT & COMMUNITY</b>",
        "• Hold protocol NFTs",
        "• Be active in Discord/Telegram",
        "• Engage on project Twitter/X",
        "",
        "━" * 28,
        "🎯 <b>CURRENT HOT AIRDROP HUNTING</b>",
        "• Solana ecosystem protocols (high season)",
        "• Base chain new dApps (Coinbase ecosystem)",
        "• ZK-rollup protocols (zkSync, StarkNet era)",
        "• Telegram mini-apps (TON ecosystem boom)",
        "",
        "━" * 28,
        "🔗 <b>AIRDROP TRACKERS</b>",
    ]
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🎯 Earndrop", url="https://earndrop.io"),
                InlineKeyboardButton(text="📊 Airdrops.io", url="https://airdrops.io"),
            ],
            [
                InlineKeyboardButton(text="🔍 DeFiLlama", url="https://defillama.com/airdrops"),
                InlineKeyboardButton(text="🪂 CoinMarketCap", url="https://coinmarketcap.com/airdrop/"),
            ],
            [InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main")],
        ]),
        disable_web_page_preview=True
    )


# ─── Callback handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "cmd_trending")
async def cb_trending(callback: CallbackQuery):
    await callback.answer("Loading trends...")
    await cmd_trending(callback.message)


@router.callback_query(F.data == "cmd_newprojects")
async def cb_new_projects(callback: CallbackQuery):
    await callback.answer("Loading new projects...")
    await cmd_new_projects(callback.message)


@router.callback_query(F.data == "cmd_memecoins")
async def cb_memecoins(callback: CallbackQuery):
    await callback.answer("Loading memecoins...")
    await cmd_memecoins(callback.message)


@router.callback_query(F.data == "cmd_airdrops")
async def cb_airdrops(callback: CallbackQuery):
    await callback.answer("Loading airdrops...")
    await cmd_airdrops(callback.message)


@router.callback_query(F.data.startswith("refresh_"))
async def cb_refresh(callback: CallbackQuery):
    context = callback.data.replace("refresh_", "")
    await callback.answer(f"Refreshing {context}...")
    
    if context == "trending":
        await cmd_trending(callback.message)
    elif context == "alpha":
        await cmd_alpha(callback.message)


def _format_age(timestamp_ms: int) -> str:
    """Format creation time as human-readable age."""
    import time
    if not timestamp_ms:
        return "Unknown age"
    
    age_seconds = (time.time() * 1000 - timestamp_ms) / 1000
    if age_seconds < 3600:
        return f"{int(age_seconds / 60)}m ago"
    elif age_seconds < 86400:
        return f"{int(age_seconds / 3600)}h ago"
    else:
        return f"{int(age_seconds / 86400)}d ago"
