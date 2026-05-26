"""
Ecosystem Handlers
==================
/solana, /base, /eth, /memecoins (chain-specific)
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.coingecko import get_coins_by_category
from bot.services.dexscreener import get_new_pairs, format_pair
from bot.services.formatter import format_number, format_change

router = Router()


async def get_ecosystem_data(chain: str, cg_category: str):
    """Get ecosystem data from multiple sources."""
    dex_pairs = await get_new_pairs(chain=chain, limit=5)
    cg_coins = await get_coins_by_category(cg_category, limit=5)
    return dex_pairs, cg_coins


@router.message(Command("solana"))
async def cmd_solana(message: Message):
    """Show Solana ecosystem highlights."""
    await message.answer("◎ <i>Loading Solana ecosystem data...</i>", parse_mode="HTML")
    
    dex_pairs, cg_coins = await get_ecosystem_data("solana", "solana-ecosystem")
    
    lines = [
        "◎ <b>SOLANA ECOSYSTEM</b>",
        "━" * 28,
        "",
        "🔥 <b>TRENDING ON SOLANA</b>",
        "",
    ]
    
    if cg_coins:
        for i, coin in enumerate(cg_coins[:5], 1):
            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "?").upper()
            mc = coin.get("market_cap", 0)
            change = coin.get("price_change_percentage_24h", 0) or 0
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>  {format_change(change)}\n"
                f"   MC: {format_number(mc)}"
            )
    else:
        lines.append("⚠️ CoinGecko temporarily unavailable")
    
    if dex_pairs:
        lines.extend(["", "━" * 28, "🆕 <b>NEW SOLANA PAIRS (DexScreener)</b>", ""])
        for i, pair in enumerate(dex_pairs[:4], 1):
            token = format_pair(pair)
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "?")
            mc = token.get("market_cap", 0)
            liq = token.get("liquidity_usd", 0)
            url = token.get("url", "")
            link = f" | <a href='{url}'>Chart</a>" if url else ""
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>\n"
                f"   MC: {format_number(mc)} | Liq: {format_number(liq)}{link}"
            )
    
    lines.extend([
        "",
        "━" * 28,
        "🔗 <b>SOLANA RESOURCES</b>",
        "• pump.fun — New meme launches",
        "• birdeye.so — Token analytics",
        "• step.finance — Portfolio tracker",
        "• Jupiter — Best DEX aggregator",
        "",
        "⚡ <i>◎ Solana Ecosystem • NexusBot</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🎭 Pump.fun", url="https://pump.fun"),
                InlineKeyboardButton(text="📊 Birdeye", url="https://birdeye.so"),
            ],
            [
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_solana"),
                InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main"),
            ],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("base"))
async def cmd_base(message: Message):
    """Show Base chain ecosystem."""
    await message.answer("🔵 <i>Loading Base chain data...</i>", parse_mode="HTML")
    
    dex_pairs, cg_coins = await get_ecosystem_data("base", "base-ecosystem")
    
    lines = [
        "🔵 <b>BASE CHAIN ECOSYSTEM</b>",
        "━" * 28,
        "",
        "🌊 <b>BASE TRENDING</b>",
        "",
    ]
    
    if cg_coins:
        for i, coin in enumerate(cg_coins[:5], 1):
            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "?").upper()
            mc = coin.get("market_cap", 0)
            change = coin.get("price_change_percentage_24h", 0) or 0
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>  {format_change(change)}\n"
                f"   MC: {format_number(mc)}"
            )
    else:
        lines.append("⚠️ CoinGecko data unavailable")
    
    if dex_pairs:
        lines.extend(["", "━" * 28, "🆕 <b>NEW BASE PAIRS</b>", ""])
        for i, pair in enumerate(dex_pairs[:4], 1):
            token = format_pair(pair)
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "?")
            mc = token.get("market_cap", 0)
            liq = token.get("liquidity_usd", 0)
            url = token.get("url", "")
            link = f" | <a href='{url}'>Chart</a>" if url else ""
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>\n"
                f"   MC: {format_number(mc)} | Liq: {format_number(liq)}{link}"
            )
    
    lines.extend([
        "",
        "━" * 28,
        "🔗 <b>BASE RESOURCES</b>",
        "• base.org — Official Base portal",
        "• aerodrome.finance — Base DEX",
        "• basescan.org — Block explorer",
        "• superbridge.app — Bridge to Base",
        "",
        "💡 <b>WHY BASE?</b>",
        "• Coinbase-backed L2 (credibility)",
        "• Low fees ($0.001-0.01 per tx)",
        "• Growing memecoin season",
        "• Easy onboarding for normies",
        "",
        "⚡ <i>🔵 Base Chain • Coinbase L2 • NexusBot</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Base.org", url="https://base.org"),
                InlineKeyboardButton(text="✈️ Aerodrome", url="https://aerodrome.finance"),
            ],
            [
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_base"),
                InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main"),
            ],
        ]),
        disable_web_page_preview=True
    )


@router.message(Command("eth"))
async def cmd_eth(message: Message):
    """Show Ethereum ecosystem highlights."""
    await message.answer("⟠ <i>Loading Ethereum ecosystem data...</i>", parse_mode="HTML")
    
    dex_pairs, cg_coins = await get_ecosystem_data("ethereum", "ethereum-ecosystem")
    
    lines = [
        "⟠ <b>ETHEREUM ECOSYSTEM</b>",
        "━" * 28,
        "",
        "🏦 <b>ETH ECOSYSTEM HIGHLIGHTS</b>",
        "",
    ]
    
    if cg_coins:
        for i, coin in enumerate(cg_coins[:5], 1):
            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "?").upper()
            mc = coin.get("market_cap", 0)
            change = coin.get("price_change_percentage_24h", 0) or 0
            lines.append(
                f"{i}. <b>{name}</b> <code>${symbol}</code>  {format_change(change)}\n"
                f"   MC: {format_number(mc)}"
            )
    else:
        lines.append("⚠️ CoinGecko data unavailable")
    
    lines.extend([
        "",
        "━" * 28,
        "🔗 <b>ETHEREUM RESOURCES</b>",
        "• etherscan.io — Explore transactions",
        "• uniswap.org — Top ETH DEX",
        "• opensea.io — ETH NFT marketplace",
        "• dune.com — On-chain analytics",
        "",
        "💡 <b>ETH OPPORTUNITIES</b>",
        "• L2 airdrop farming (Arbitrum, zkSync)",
        "• DeFi yield on established protocols",
        "• ETH NFT flipping (low gas hours)",
        "• ERC-404 token experiments",
        "",
        "⚡ <i>⟠ Ethereum Ecosystem • NexusBot</i>",
    ])
    
    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Etherscan", url="https://etherscan.io"),
                InlineKeyboardButton(text="🦄 Uniswap", url="https://uniswap.org"),
            ],
            [
                InlineKeyboardButton(text="🔄 Refresh", callback_data="cmd_eth"),
                InlineKeyboardButton(text="🏠 Menu", callback_data="menu_main"),
            ],
        ]),
        disable_web_page_preview=True
    )


# ─── Callback Handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "cmd_solana")
async def cb_solana(callback: CallbackQuery):
    await callback.answer("Loading Solana data...")
    await cmd_solana(callback.message)


@router.callback_query(F.data == "cmd_base")
async def cb_base(callback: CallbackQuery):
    await callback.answer("Loading Base data...")
    await cmd_base(callback.message)


@router.callback_query(F.data == "cmd_eth")
async def cb_eth(callback: CallbackQuery):
    await callback.answer("Loading ETH data...")
    await cmd_eth(callback.message)
