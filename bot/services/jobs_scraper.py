"""
Web3 Jobs Scraper
=================
Scrapes multiple free job boards for Web3/crypto jobs.
Uses BeautifulSoup + requests/aiohttp.
"""
import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from loguru import logger
from datetime import datetime


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def scrape_cryptojobslist(job_type: str = "community-manager") -> list:
    """Scrape CryptoJobsList for specific job types."""
    url = f"https://cryptojobslist.com/{job_type}"
    jobs = []
    
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return []
                html = await resp.text()
        
        soup = BeautifulSoup(html, "lxml")
        job_cards = soup.find_all("tr", class_=re.compile(r"job")) or \
                    soup.find_all("div", class_=re.compile(r"job"))
        
        for card in job_cards[:10]:
            title_el = card.find("h2") or card.find("h3") or card.find("a")
            company_el = card.find(class_=re.compile(r"company"))
            link_el = card.find("a", href=True)
            
            if title_el:
                jobs.append({
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "Unknown",
                    "url": f"https://cryptojobslist.com{link_el['href']}" if link_el and link_el["href"].startswith("/") else (link_el["href"] if link_el else url),
                    "source": "CryptoJobsList",
                    "type": job_type,
                    "remote": True,
                    "scraped_at": datetime.utcnow().isoformat(),
                })
    except Exception as e:
        logger.error(f"CryptoJobsList scrape error: {e}")
    
    return jobs


async def scrape_web3_career(category: str = "community") -> list:
    """Scrape web3.career for jobs."""
    url = f"https://web3.career/{category}-jobs"
    jobs = []
    
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return []
                html = await resp.text()
        
        soup = BeautifulSoup(html, "lxml")
        
        # web3.career uses table rows for jobs
        rows = soup.find_all("tr")
        for row in rows[:15]:
            title_el = row.find("h2") or row.find("h3") or row.find("a", class_=re.compile(r"job"))
            company_el = row.find(class_=re.compile(r"company"))
            link_el = row.find("a", href=True)
            
            if title_el and link_el:
                href = link_el.get("href", "")
                full_url = f"https://web3.career{href}" if href.startswith("/") else href
                jobs.append({
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "Web3 Company",
                    "url": full_url,
                    "source": "web3.career",
                    "type": category,
                    "remote": True,
                    "scraped_at": datetime.utcnow().isoformat(),
                })
    except Exception as e:
        logger.error(f"web3.career scrape error: {e}")
    
    return jobs


async def scrape_remote3() -> list:
    """Scrape remote3.co for remote Web3 jobs."""
    url = "https://remote3.co/web3-jobs"
    jobs = []
    
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return []
                html = await resp.text()
        
        soup = BeautifulSoup(html, "lxml")
        cards = soup.find_all("div", class_=re.compile(r"job|card|listing"))
        
        for card in cards[:10]:
            title_el = card.find(["h2", "h3", "h4"])
            company_el = card.find(class_=re.compile(r"company|employer"))
            link_el = card.find("a", href=True)
            
            if title_el:
                href = link_el.get("href", "") if link_el else ""
                full_url = f"https://remote3.co{href}" if href.startswith("/") else href or url
                jobs.append({
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "Anonymous",
                    "url": full_url,
                    "source": "remote3.co",
                    "type": "web3",
                    "remote": True,
                    "scraped_at": datetime.utcnow().isoformat(),
                })
    except Exception as e:
        logger.error(f"remote3.co scrape error: {e}")
    
    return jobs


async def get_all_cm_jobs() -> list:
    """Aggregate CM jobs from all sources."""
    results = await asyncio.gather(
        scrape_cryptojobslist("community-manager"),
        scrape_web3_career("community"),
        scrape_remote3(),
        return_exceptions=True
    )
    
    jobs = []
    for result in results:
        if isinstance(result, list):
            jobs.extend(result)
    
    # Add some curated mock data if scraping fails (fallback)
    if not jobs:
        jobs = _get_fallback_cm_jobs()
    
    return jobs[:20]


async def get_all_mod_jobs() -> list:
    """Aggregate moderator jobs from all sources."""
    results = await asyncio.gather(
        scrape_cryptojobslist("moderator"),
        scrape_web3_career("moderator"),
        return_exceptions=True
    )
    
    jobs = []
    for result in results:
        if isinstance(result, list):
            jobs.extend(result)
    
    if not jobs:
        jobs = _get_fallback_mod_jobs()
    
    return jobs[:15]


async def get_nft_jobs() -> list:
    """Get NFT art and design jobs."""
    results = await asyncio.gather(
        scrape_cryptojobslist("design"),
        scrape_web3_career("design"),
        return_exceptions=True
    )
    
    jobs = []
    for result in results:
        if isinstance(result, list):
            jobs.extend(result)
    
    if not jobs:
        jobs = _get_fallback_nft_jobs()
    
    return jobs[:15]


async def get_tester_jobs() -> list:
    """Get protocol testing and QA jobs."""
    results = await asyncio.gather(
        scrape_cryptojobslist("qa"),
        scrape_web3_career("testing"),
        return_exceptions=True
    )
    
    jobs = []
    for result in results:
        if isinstance(result, list):
            jobs.extend(result)
    
    if not jobs:
        jobs = _get_fallback_tester_jobs()
    
    return jobs[:15]


# ─── Fallback Data (when scraping fails) ───────────────────────────────────────

def _get_fallback_cm_jobs() -> list:
    return [
        {
            "title": "Community Manager — Solana DeFi Protocol",
            "company": "AnonymousDAO",
            "url": "https://cryptojobslist.com/community-manager",
            "source": "Direct",
            "type": "CM",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
        {
            "title": "Telegram Community Lead — NFT Project",
            "company": "NFT Studio",
            "url": "https://web3.career/community-manager-jobs",
            "source": "Direct",
            "type": "CM",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
        {
            "title": "Discord Server Manager — GameFi",
            "company": "GameFi Protocol",
            "url": "https://remote3.co/web3-jobs",
            "source": "Direct",
            "type": "CM",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
    ]


def _get_fallback_mod_jobs() -> list:
    return [
        {
            "title": "Telegram Moderator — Meme Coin Community",
            "company": "MemeCoin Project",
            "url": "https://cryptojobslist.com/moderator",
            "source": "Direct",
            "type": "Mod",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
        {
            "title": "Discord Moderator — L2 Protocol",
            "company": "Layer2 DAO",
            "url": "https://web3.career/moderator-jobs",
            "source": "Direct",
            "type": "Mod",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
    ]


def _get_fallback_nft_jobs() -> list:
    return [
        {
            "title": "NFT Artist — PFP Collection",
            "company": "ArtDAO",
            "url": "https://cryptojobslist.com/design",
            "source": "Direct",
            "type": "NFT",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
    ]


def _get_fallback_tester_jobs() -> list:
    return [
        {
            "title": "DeFi Protocol Tester — Bug Bounty",
            "company": "Security DAO",
            "url": "https://immunefi.com",
            "source": "Immunefi",
            "type": "Tester",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
        {
            "title": "Smart Contract QA Tester",
            "company": "Audit Firm",
            "url": "https://cryptojobslist.com/qa",
            "source": "Direct",
            "type": "Tester",
            "remote": True,
            "scraped_at": datetime.utcnow().isoformat(),
        },
    ]
