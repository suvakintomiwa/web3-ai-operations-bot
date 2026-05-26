"""
NexusBot Configuration
======================
Loads all environment variables and defines global constants.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Telegram ──────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", "0"))

# ─── AI API Keys ───────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

# ─── Crypto Data APIs ──────────────────────────────────────────────────────────
CMC_API_KEY: str = os.getenv("CMC_API_KEY", "")
# DexScreener & CoinGecko: NO API KEY NEEDED

# ─── Database ──────────────────────────────────────────────────────────────────
DB_PATH: str = os.getenv("DB_PATH", "data/nexusbot.db")

# ─── Bot Settings ──────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
ALERT_INTERVAL_MINUTES: int = int(os.getenv("ALERT_INTERVAL_MINUTES", "30"))
MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "10"))
BOT_NAME: str = os.getenv("BOT_NAME", "NexusBot")

# ─── AI Model Config ───────────────────────────────────────────────────────────
GROQ_MODEL: str = "llama3-70b-8192"
GROQ_MODEL_FAST: str = "llama3-8b-8192"
OPENROUTER_MODEL: str = "mistralai/mistral-7b-instruct:free"
GEMINI_MODEL: str = "gemini-pro"
DEEPSEEK_MODEL: str = "deepseek-chat"

AI_MAX_TOKENS: int = 1024
AI_TEMPERATURE: float = 0.7

# ─── Scheduler Intervals ───────────────────────────────────────────────────────
ALPHA_SCAN_INTERVAL: int = 5          # minutes
JOB_SCAN_INTERVAL: int = 60           # minutes
WHALE_SCAN_INTERVAL: int = 15         # minutes
REMINDER_CHECK_INTERVAL: int = 1      # minutes
TRENDING_SCAN_INTERVAL: int = 10      # minutes

# ─── URLs ──────────────────────────────────────────────────────────────────────
DEXSCREENER_BASE: str = "https://api.dexscreener.com/latest"
COINGECKO_BASE: str = "https://api.coingecko.com/api/v3"
CMC_BASE: str = "https://pro-api.coinmarketcap.com/v1"
GITHUB_API: str = "https://api.github.com"
REDDIT_BASE: str = "https://www.reddit.com"

# ─── Web3 Job Sources ──────────────────────────────────────────────────────────
JOB_SOURCES: list = [
    "https://cryptojobslist.com/community-manager",
    "https://web3.career/community-manager-jobs",
    "https://remote3.co/web3-jobs",
    "https://useWeb3.xyz/jobs",
]

# ─── Validation ────────────────────────────────────────────────────────────────
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is required! Set it in your .env file.")

# ─── Theme / Formatting ────────────────────────────────────────────────────────
SEPARATOR: str = "━" * 30
CYBER_HEADER: str = "⚡ NEXUSBOT"
