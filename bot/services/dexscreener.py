"""
DexScreener API Client
======================
FREE — No API key required.
Fetches new token pairs, trending tokens, and token details.
"""
import aiohttp
from loguru import logger
from bot.config import DEXSCREENER_BASE


async def get_new_pairs(chain: str = None, limit: int = 10) -> list:
    """Fetch newly created token pairs."""
    try:
        # Use search endpoint with chain filter
        url = f"{DEXSCREENER_BASE}/dex/search"
        params = {"q": chain or "new"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                pairs = data.get("pairs", [])
                
                if chain:
                    pairs = [p for p in pairs if p.get("chainId", "").lower() == chain.lower()]
                
                # Sort by creation time (newest first) and filter for recent ones
                pairs = sorted(pairs, key=lambda x: x.get("pairCreatedAt", 0), reverse=True)
                return pairs[:limit]
    except Exception as e:
        logger.error(f"DexScreener new pairs error: {e}")
        return []


async def get_trending_tokens(limit: int = 10) -> list:
    """Get trending tokens by volume."""
    try:
        # Get boosted/trending tokens
        url = "https://api.dexscreener.com/token-boosts/top/v1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        return data[:limit]
        
        # Fallback: search for top volume
        url = f"{DEXSCREENER_BASE}/dex/search"
        params = {"q": "solana"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                pairs = data.get("pairs", [])
                pairs = sorted(pairs, key=lambda x: float(x.get("volume", {}).get("h24", 0) or 0), reverse=True)
                return pairs[:limit]
                
    except Exception as e:
        logger.error(f"DexScreener trending error: {e}")
        return []


async def get_token_info(address: str, chain: str = None) -> dict | None:
    """Get detailed info for a specific token."""
    try:
        if chain:
            url = f"{DEXSCREENER_BASE}/dex/tokens/{address}"
        else:
            url = f"{DEXSCREENER_BASE}/dex/tokens/{address}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                pairs = data.get("pairs", [])
                if not pairs:
                    return None
                # Return the pair with highest liquidity
                return max(pairs, key=lambda x: float(x.get("liquidity", {}).get("usd", 0) or 0))
    except Exception as e:
        logger.error(f"DexScreener token info error: {e}")
        return None


async def search_token(query: str) -> list:
    """Search for tokens by name or symbol."""
    try:
        url = f"{DEXSCREENER_BASE}/dex/search"
        params = {"q": query}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                return data.get("pairs", [])[:10]
    except Exception as e:
        logger.error(f"DexScreener search error: {e}")
        return []


def format_pair(pair: dict) -> dict:
    """Normalize a DexScreener pair into a clean dict."""
    base = pair.get("baseToken", {})
    price_usd = pair.get("priceUsd", "0") or "0"
    mc = pair.get("fdv", 0) or 0
    volume = pair.get("volume", {}).get("h24", 0) or 0
    liquidity = pair.get("liquidity", {}).get("usd", 0) or 0
    change_1h = pair.get("priceChange", {}).get("h1", 0) or 0
    change_24h = pair.get("priceChange", {}).get("h24", 0) or 0
    
    return {
        "name": base.get("name", "Unknown"),
        "symbol": base.get("symbol", "?"),
        "address": base.get("address", ""),
        "chain": pair.get("chainId", "unknown"),
        "price_usd": float(price_usd),
        "market_cap": float(mc),
        "volume_24h": float(volume),
        "liquidity_usd": float(liquidity),
        "change_1h": float(change_1h),
        "change_24h": float(change_24h),
        "pair_address": pair.get("pairAddress", ""),
        "dex": pair.get("dexId", ""),
        "url": pair.get("url", ""),
        "created_at": pair.get("pairCreatedAt", 0),
        "txns_24h": (pair.get("txns", {}).get("h24", {}).get("buys", 0) or 0) + 
                    (pair.get("txns", {}).get("h24", {}).get("sells", 0) or 0),
    }
