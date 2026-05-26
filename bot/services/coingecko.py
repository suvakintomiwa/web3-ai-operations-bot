"""
CoinGecko API Client
====================
FREE tier — 30 calls/minute, no API key needed for basic endpoints.
Fetches trending coins, new listings, and ecosystem data.
"""
import aiohttp
import asyncio
from loguru import logger
from bot.config import COINGECKO_BASE


async def get_trending_coins() -> list:
    """Get top trending coins from CoinGecko search."""
    try:
        url = f"{COINGECKO_BASE}/search/trending"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 429:
                    logger.warning("CoinGecko rate limited, waiting...")
                    await asyncio.sleep(10)
                    return []
                if resp.status != 200:
                    return []
                data = await resp.json()
                return data.get("coins", [])
    except Exception as e:
        logger.error(f"CoinGecko trending error: {e}")
        return []


async def get_new_coins(limit: int = 10) -> list:
    """Get recently added coins."""
    try:
        url = f"{COINGECKO_BASE}/coins/list/new"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 429:
                    await asyncio.sleep(10)
                    return []
                if resp.status != 200:
                    return []
                data = await resp.json()
                return data[:limit] if isinstance(data, list) else []
    except Exception as e:
        logger.error(f"CoinGecko new coins error: {e}")
        return []


async def get_coins_by_category(category: str, limit: int = 10) -> list:
    """Get top coins in a category (e.g., 'meme-token', 'solana-ecosystem', 'base-ecosystem')."""
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": "usd",
            "category": category,
            "order": "volume_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "1h,24h,7d"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 429:
                    await asyncio.sleep(10)
                    return []
                if resp.status != 200:
                    return []
                return await resp.json()
    except Exception as e:
        logger.error(f"CoinGecko category error: {e}")
        return []


async def get_coin_details(coin_id: str) -> dict | None:
    """Get detailed information about a specific coin."""
    try:
        url = f"{COINGECKO_BASE}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "true"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception as e:
        logger.error(f"CoinGecko coin details error: {e}")
        return None


async def get_global_stats() -> dict:
    """Get global crypto market stats."""
    try:
        url = f"{COINGECKO_BASE}/global"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return {}
                data = await resp.json()
                return data.get("data", {})
    except Exception as e:
        logger.error(f"CoinGecko global stats error: {e}")
        return {}


async def get_top_gainers(limit: int = 10) -> list:
    """Get top gainers in last 24h."""
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "volume_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                # Filter and sort by 24h change
                gainers = [c for c in data if c.get("price_change_percentage_24h", 0) and c["price_change_percentage_24h"] > 0]
                gainers.sort(key=lambda x: x.get("price_change_percentage_24h", 0), reverse=True)
                return gainers[:limit]
    except Exception as e:
        logger.error(f"CoinGecko top gainers error: {e}")
        return []


def format_coin(coin: dict) -> dict:
    """Normalize a CoinGecko coin into clean format."""
    item = coin.get("item", coin)  # Handle trending format vs market format
    return {
        "name": item.get("name", "Unknown"),
        "symbol": item.get("symbol", "?").upper(),
        "market_cap_rank": item.get("market_cap_rank", 0),
        "price": item.get("current_price", item.get("data", {}).get("price", 0)),
        "market_cap": item.get("market_cap", 0),
        "change_24h": item.get("price_change_percentage_24h", 0),
        "volume_24h": item.get("total_volume", 0),
        "coingecko_url": f"https://coingecko.com/en/coins/{item.get('id', '')}",
        "thumb": item.get("thumb", item.get("image", "")),
    }
