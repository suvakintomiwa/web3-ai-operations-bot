"""
Project Analyzer Service
========================
Analyzes crypto projects for legitimacy, scam risk, and potential.
Uses DexScreener, CoinGecko, and AI for comprehensive scoring.
"""
import re
import aiohttp
from loguru import logger
from bot.services.dexscreener import get_token_info, format_pair, search_token
from bot.services.ai_service import analyze_project_ai


# ─── Detection Patterns ────────────────────────────────────────────────────────
SCAM_KEYWORDS = [
    "100x guaranteed", "not a rug", "safu", "elon", "100% safe",
    "no team tokens", "based dev", "not financial advice but buy",
    "going to moon guaranteed", "next doge", "next shib", "1000x easy"
]

RUG_RED_FLAGS = [
    "mint function enabled",
    "transfer restrictions",
    "max wallet lock",
    "blacklist function",
    "honeypot",
]


async def analyze_address(address: str) -> dict:
    """Analyze a token by contract address."""
    result = {
        "input": address,
        "type": "token_address",
        "found": False,
        "data": {},
        "risk_score": 50,
        "red_flags": [],
        "green_flags": [],
    }
    
    try:
        pair = await get_token_info(address)
        if pair:
            result["found"] = True
            result["data"] = format_pair(pair)
            result = _score_token(result)
    except Exception as e:
        logger.error(f"Address analysis error: {e}")
    
    return result


async def analyze_url(url: str) -> dict:
    """Analyze a project by its URL."""
    result = {
        "input": url,
        "type": "url",
        "found": True,
        "data": {},
        "risk_score": 50,
        "red_flags": [],
        "green_flags": [],
        "url_checks": {},
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15),
                                    allow_redirects=True) as resp:
                result["url_checks"]["status"] = resp.status
                result["url_checks"]["https"] = url.startswith("https")
                
                if resp.status == 200:
                    html = await resp.text()
                    result["url_checks"]["has_whitepaper"] = "whitepaper" in html.lower()
                    result["url_checks"]["has_roadmap"] = "roadmap" in html.lower()
                    result["url_checks"]["has_team"] = "team" in html.lower()
                    result["url_checks"]["has_audit"] = "audit" in html.lower()
                    
                    # Check for scam keywords
                    for kw in SCAM_KEYWORDS:
                        if kw.lower() in html.lower():
                            result["red_flags"].append(f"Contains suspicious text: '{kw}'")
                    
                    # Build score
                    if result["url_checks"].get("has_whitepaper"):
                        result["green_flags"].append("Has whitepaper link")
                    if result["url_checks"].get("has_audit"):
                        result["green_flags"].append("Mentions audit")
                    if result["url_checks"].get("has_team"):
                        result["green_flags"].append("Has team section")
                    if not result["url_checks"]["https"]:
                        result["red_flags"].append("Not using HTTPS")
                        
    except aiohttp.ClientError:
        result["red_flags"].append("Website is unreachable or has errors")
        result["risk_score"] += 20
    except Exception as e:
        logger.error(f"URL analysis error: {e}")
    
    result = _calculate_url_score(result)
    return result


async def analyze_twitter(handle: str) -> dict:
    """Analyze a Twitter/X account (limited without API key)."""
    # Strip @ if present
    handle = handle.lstrip("@")
    
    result = {
        "input": f"@{handle}",
        "type": "twitter",
        "data": {
            "handle": handle,
            "url": f"https://twitter.com/{handle}",
        },
        "risk_score": 40,
        "red_flags": [],
        "green_flags": [],
        "notes": "Twitter API requires auth. Doing basic heuristic check.",
    }
    
    # Basic heuristics without API
    if len(handle) < 4:
        result["red_flags"].append("Very short handle — could be impersonation")
    if re.search(r"\d{4,}", handle):
        result["red_flags"].append("Handle has many numbers — possible fake account")
    if handle.lower() in ["crypto", "nft", "defi", "web3", "token"]:
        result["red_flags"].append("Generic handle — verify authenticity")
    else:
        result["green_flags"].append("Unique handle — less likely impersonator")
    
    return result


async def full_analysis(user_input: str) -> str:
    """
    Main analysis function.
    Detects input type (address, URL, Twitter) and runs appropriate checks.
    Returns formatted Telegram message.
    """
    user_input = user_input.strip()
    
    # Detect input type
    if re.match(r"^0x[a-fA-F0-9]{40}$", user_input):
        # Ethereum address
        data = await analyze_address(user_input)
        return _format_token_analysis(data)
    
    elif re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", user_input) and not user_input.startswith("http"):
        # Possible Solana address
        data = await analyze_address(user_input)
        return _format_token_analysis(data)
    
    elif user_input.startswith("http") or "." in user_input[:20]:
        # URL
        if not user_input.startswith("http"):
            user_input = f"https://{user_input}"
        data = await analyze_url(user_input)
        
        # Also try AI analysis
        ai_response, _ = await analyze_project_ai(f"Website URL: {user_input}\nURL analysis: {data}")
        return _format_url_analysis(data, ai_response)
    
    elif user_input.startswith("@") or re.match(r"^[a-zA-Z0-9_]{3,50}$", user_input.lstrip("@")):
        # Twitter handle
        data = await analyze_twitter(user_input)
        ai_response, _ = await analyze_project_ai(f"Twitter account: @{user_input.lstrip('@')}")
        return _format_twitter_analysis(data, ai_response)
    
    else:
        # General text — do AI analysis
        ai_response, _ = await analyze_project_ai(user_input)
        return f"🔬 <b>AI PROJECT ANALYSIS</b>\n{'━'*25}\n\n{ai_response}"


def _score_token(result: dict) -> dict:
    """Score a token based on on-chain data."""
    data = result["data"]
    score = 50  # Start neutral
    
    mc = data.get("market_cap", 0)
    liq = data.get("liquidity_usd", 0)
    vol = data.get("volume_24h", 0)
    txns = data.get("txns_24h", 0)
    change = data.get("change_24h", 0)
    
    # Liquidity checks
    if liq > 100000:
        result["green_flags"].append(f"Good liquidity: ${liq:,.0f}")
        score -= 15
    elif liq > 50000:
        result["green_flags"].append(f"Decent liquidity: ${liq:,.0f}")
        score -= 5
    elif liq < 10000:
        result["red_flags"].append(f"Very low liquidity: ${liq:,.0f} — easy to manipulate")
        score += 25
    elif liq < 25000:
        result["red_flags"].append(f"Low liquidity: ${liq:,.0f}")
        score += 10
    
    # Volume checks
    if vol > 0 and mc > 0:
        vol_mc_ratio = vol / mc if mc > 0 else 0
        if vol_mc_ratio > 5:
            result["red_flags"].append("Volume/MC ratio extremely high — wash trading likely")
            score += 20
        elif vol_mc_ratio > 0.1:
            result["green_flags"].append("Healthy trading volume relative to market cap")
            score -= 10
    
    # Transaction count
    if txns > 1000:
        result["green_flags"].append(f"High transaction count: {txns:,} in 24h")
        score -= 10
    elif txns < 50:
        result["red_flags"].append(f"Very low transactions: {txns} in 24h — low activity")
        score += 15
    
    # Extreme price movements
    if abs(change) > 200:
        result["red_flags"].append(f"Extreme price movement: {change:.1f}% — possible pump and dump")
        score += 20
    elif change > 50:
        result["red_flags"].append(f"Very high pump: {change:.1f}% — verify sustainability")
        score += 10
    
    result["risk_score"] = max(0, min(100, score))
    return result


def _calculate_url_score(result: dict) -> dict:
    checks = result["url_checks"]
    score = 50
    
    if checks.get("https"):
        score -= 5
    else:
        score += 15
    
    if checks.get("status") != 200:
        score += 30
    
    positives = sum([
        checks.get("has_whitepaper", False),
        checks.get("has_roadmap", False),
        checks.get("has_team", False),
        checks.get("has_audit", False),
    ])
    score -= positives * 8
    score += len(result["red_flags"]) * 5
    
    result["risk_score"] = max(0, min(100, score))
    return result


def _get_risk_label(score: int) -> str:
    if score <= 25:
        return "🟢 LOW RISK"
    elif score <= 50:
        return "🟡 MODERATE RISK"
    elif score <= 75:
        return "🟠 HIGH RISK"
    else:
        return "🔴 VERY HIGH RISK / LIKELY SCAM"


def _format_token_analysis(data: dict) -> str:
    if not data["found"]:
        return (
            "❌ <b>Token not found on DexScreener</b>\n\n"
            "This could mean:\n"
            "• Token is not yet listed on any DEX\n"
            "• Invalid contract address\n"
            "• Chain not supported\n\n"
            "🚨 <b>HIGH RISK</b> — verify independently before investing."
        )
    
    d = data["data"]
    score = data["risk_score"]
    
    msg = [
        f"🔬 <b>TOKEN ANALYSIS</b>",
        f"{'━'*28}",
        f"🏷️ <b>{d['name']} (${d['symbol']})</b>",
        f"⛓️ Chain: <code>{d['chain'].upper()}</code>",
        f"💰 Price: <code>${d['price_usd']:.8f}</code>",
        f"📊 Market Cap: <code>${d['market_cap']:,.0f}</code>",
        f"💧 Liquidity: <code>${d['liquidity_usd']:,.0f}</code>",
        f"📈 Volume 24h: <code>${d['volume_24h']:,.0f}</code>",
        f"🔄 Transactions 24h: <code>{d['txns_24h']:,}</code>",
        f"📉 Price Change 24h: <code>{d['change_24h']:+.2f}%</code>",
        f"{'━'*28}",
        f"⚠️ <b>RISK SCORE: {score}/100</b>",
        f"Status: {_get_risk_label(score)}",
    ]
    
    if data["green_flags"]:
        msg.append(f"\n✅ <b>GREEN FLAGS</b>")
        for flag in data["green_flags"]:
            msg.append(f"  • {flag}")
    
    if data["red_flags"]:
        msg.append(f"\n🚩 <b>RED FLAGS</b>")
        for flag in data["red_flags"]:
            msg.append(f"  • {flag}")
    
    if d.get("url"):
        msg.append(f"\n🔗 <a href='{d['url']}'>View on DexScreener</a>")
    
    msg.append(f"\n⚡ <i>NexusBot Analysis · DYOR · Not financial advice</i>")
    
    return "\n".join(msg)


def _format_url_analysis(data: dict, ai_analysis: str) -> str:
    score = data["risk_score"]
    checks = data.get("url_checks", {})
    
    msg = [
        f"🔬 <b>WEBSITE ANALYSIS</b>",
        f"{'━'*28}",
        f"🌐 URL: <code>{data['input']}</code>",
        f"",
        f"<b>📋 WEBSITE CHECKS</b>",
        f"{'✅' if checks.get('https') else '❌'} HTTPS: {'Yes' if checks.get('https') else 'No'}",
        f"{'✅' if checks.get('status') == 200 else '❌'} Website Live: {'Yes' if checks.get('status') == 200 else 'No'}",
        f"{'✅' if checks.get('has_whitepaper') else '⚠️'} Whitepaper: {'Found' if checks.get('has_whitepaper') else 'Not found'}",
        f"{'✅' if checks.get('has_roadmap') else '⚠️'} Roadmap: {'Found' if checks.get('has_roadmap') else 'Not found'}",
        f"{'✅' if checks.get('has_team') else '⚠️'} Team Info: {'Found' if checks.get('has_team') else 'Not found'}",
        f"{'✅' if checks.get('has_audit') else '⚠️'} Audit Mention: {'Found' if checks.get('has_audit') else 'Not found'}",
        f"",
        f"⚠️ <b>RISK SCORE: {score}/100</b>",
        f"Status: {_get_risk_label(score)}",
    ]
    
    if data["green_flags"]:
        msg.append(f"\n✅ <b>POSITIVES</b>")
        for flag in data["green_flags"]:
            msg.append(f"  • {flag}")
    
    if data["red_flags"]:
        msg.append(f"\n🚩 <b>CONCERNS</b>")
        for flag in data["red_flags"]:
            msg.append(f"  • {flag}")
    
    msg.extend([
        f"\n{'━'*28}",
        f"🤖 <b>AI ASSESSMENT</b>",
        ai_analysis[:800] + ("..." if len(ai_analysis) > 800 else ""),
        f"\n⚡ <i>NexusBot Analysis · DYOR · Not financial advice</i>",
    ])
    
    return "\n".join(msg)


def _format_twitter_analysis(data: dict, ai_analysis: str) -> str:
    score = data["risk_score"]
    
    msg = [
        f"🔬 <b>TWITTER/X ANALYSIS</b>",
        f"{'━'*28}",
        f"🐦 Account: <a href='{data['data']['url']}'>{data['input']}</a>",
        f"",
        f"⚠️ <b>PRELIMINARY RISK: {score}/100</b>",
        f"Status: {_get_risk_label(score)}",
    ]
    
    if data["green_flags"]:
        msg.append(f"\n✅ <b>GOOD SIGNS</b>")
        for flag in data["green_flags"]:
            msg.append(f"  • {flag}")
    
    if data["red_flags"]:
        msg.append(f"\n🚩 <b>CONCERNS</b>")
        for flag in data["red_flags"]:
            msg.append(f"  • {flag}")
    
    msg.extend([
        f"\n⚠️ <i>Note: {data.get('notes', '')}</i>",
        f"\n{'━'*28}",
        f"🤖 <b>AI ASSESSMENT</b>",
        ai_analysis[:600] + ("..." if len(ai_analysis) > 600 else ""),
        f"\n⚡ <i>NexusBot Analysis · Verify manually · DYOR</i>",
    ])
    
    return "\n".join(msg)
