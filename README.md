# ⚡ NexusBot — Web3 AI Telegram Assistant

> Your personal cyberpunk AI co-pilot for crypto operations, Web3 job hunting, alpha discovery, and community management. Built entirely on **FREE** infrastructure.

![NexusBot Banner](https://img.shields.io/badge/NexusBot-v1.0.0-cyan?style=for-the-badge&logo=telegram)
![Free Stack](https://img.shields.io/badge/Cost-$0%2Fmonth-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Railway](https://img.shields.io/badge/Deploy-Railway-purple?style=for-the-badge)

---

## 🎯 What is NexusBot?

NexusBot is a fully-featured Telegram bot built for solo Web3 operators — community managers, raid leaders, alpha hunters, KOL outreach specialists, and crypto freelancers.

**Total monthly cost: $0.00** — runs on Railway free tier with free API tiers.

---

## ✨ Features

### 🔍 Alpha Discovery
- DexScreener new pair scanning (every 5 min)
- CoinGecko trending + top gainers
- New project launches across Solana, Base, Ethereum
- Meme coin radar with momentum scoring
- Airdrop opportunity tracker

### 💼 Web3 Job Hunting
- Community Manager role aggregator
- Moderator opening scanner
- NFT artist & designer gig finder
- Protocol testing & bug bounty tracker
- AI-written custom application DMs

### 🤖 Multi-Model AI (Auto-Fallback)
```
Groq (LLaMA 3 70B) → OpenRouter (Mistral) → Gemini Pro → DeepSeek
```
- Raid message writer
- KOL outreach DM composer
- Shill thread generator
- Project analysis engine
- Mod reply templates
- Engagement strategy planner

### 🔔 Auto Alerts
- New alpha token alerts
- Trending project updates
- Whale activity monitoring
- Job opening notifications
- Airdrop alerts

### 🔬 Project Analyzer
Paste any of these:
- `0x1234...abcd` — Token address analysis
- `https://project.com` — Website audit
- `@twitterhandle` — Social presence check
- Project name/description — AI full review

### 🗂️ Personal Organizer
- Reminders (`/reminder 2h check this project`)
- Project watchlist
- Note saver for links/alpha
- Outreach history tracker

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Telegram account (to get bot token)
- Free accounts on: Groq, OpenRouter, Google AI Studio, DeepSeek

### 2. Get Free API Keys

| Service | URL | Limit |
|---------|-----|-------|
| Telegram Bot | [t.me/BotFather](https://t.me/BotFather) | Unlimited |
| Groq (LLaMA 3) | [console.groq.com](https://console.groq.com) | 14,400 req/day FREE |
| OpenRouter | [openrouter.ai](https://openrouter.ai) | Free models available |
| Google Gemini | [aistudio.google.com](https://aistudio.google.com) | 60 RPM FREE |
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com) | Generous free tier |
| CoinMarketCap | [coinmarketcap.com/api](https://coinmarketcap.com/api/) | 333 calls/day FREE |
| DexScreener | [docs.dexscreener.com](https://docs.dexscreener.com) | **NO KEY NEEDED** |
| CoinGecko | [coingecko.com/api](https://coingecko.com/api/documentation) | **NO KEY NEEDED** |

### 3. Clone & Setup

```bash
git clone https://github.com/yourusername/nexusbot.git
cd nexusbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Fill in your API keys
```

### 4. Initialize Database

```bash
python -c "import asyncio; from bot.database import init_db; asyncio.run(init_db())"
```

### 5. Run Locally

```bash
python -m bot.main
```

You should see:
```
✅ Database initialized
✅ Background scheduler started
📡 Starting NexusBot polling...
```

---

## 🚂 Deploy to Railway (Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "🚀 NexusBot deploy"
git remote add origin https://github.com/YOUR_USERNAME/nexusbot.git
git push -u origin main
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app) → Sign up free
2. New Project → Deploy from GitHub repo
3. Select your nexusbot repository

### Step 3: Add Environment Variables
In Railway dashboard → Variables tab, add all variables from `.env.example`:
```
BOT_TOKEN = your_bot_token
GROQ_API_KEY = your_groq_key
OPENROUTER_API_KEY = your_openrouter_key
GEMINI_API_KEY = your_gemini_key
DEEPSEEK_API_KEY = your_deepseek_key
CMC_API_KEY = your_cmc_key
ADMIN_USER_ID = your_telegram_id
DB_PATH = data/nexusbot.db
```

### Step 4: Deploy!
Railway auto-detects Python and runs:
```
pip install -r requirements.txt
python -m bot.main
```

**Railway Free Tier: 500 hours/month** — more than enough for a personal bot!

---

## 📋 Commands Reference

### 🚀 Core
| Command | Description |
|---------|-------------|
| `/start` | Initialize bot, show dashboard |
| `/help` | Full command reference |
| `/ai [prompt]` | Chat with AI assistant |
| `/settings` | Configure preferences |
| `/alerts` | Manage push alerts |

### 🔍 Alpha Hunting
| Command | Description |
|---------|-------------|
| `/alpha` | Top trending tokens from multiple sources |
| `/newprojects` | Fresh launches in last 24h |
| `/trending` | What's pumping right now |
| `/memecoins` | New meme coin launches |
| `/airdrops` | Active airdrop opportunities |
| `/solana` | Solana ecosystem highlights |
| `/base` | Base chain projects |
| `/eth` | Ethereum ecosystem |

### 💼 Job Hunting
| Command | Description |
|---------|-------------|
| `/jobs` | All remote Web3 jobs |
| `/cmjobs` | Community Manager roles |
| `/modjobs` | Moderator openings |
| `/nftjobs` | NFT art gigs |
| `/tester` | Protocol testing opportunities |

### 🔬 Analysis
| Command | Description |
|---------|-------------|
| `/checkproject [input]` | Quick analysis (address/URL/handle) |
| `/analyze [input]` | Deep AI-powered audit |

### 📬 Outreach
| Command | Description |
|---------|-------------|
| `/outreach [project]` | AI-written KOL outreach DMs |
| `/raid [project]` | Generate raid messages |
| `/shill [project]` | Create Twitter shill threads |
| `/network` | View outreach history |

### 🗂️ Organizer
| Command | Description |
|---------|-------------|
| `/reminder [time] [msg]` | Set custom reminder |
| `/watchlist` | View tracked projects |
| `/save [text]` | Save note or link |
| `/notes` | View all notes |

---

## 🛠️ Project Structure

```
nexusbot/
├── bot/
│   ├── main.py              ← Entry point
│   ├── config.py            ← Settings & env vars
│   ├── database.py          ← SQLite async layer
│   ├── handlers/
│   │   ├── start.py         ← /start /help + main menu
│   │   ├── alpha.py         ← /alpha /trending /newprojects
│   │   ├── jobs.py          ← /jobs /cmjobs /modjobs
│   │   ├── ai_chat.py       ← /ai + conversation mode
│   │   ├── analysis.py      ← /checkproject /analyze
│   │   ├── outreach.py      ← /outreach /raid /shill
│   │   ├── organizer.py     ← /reminder /watchlist /save /notes
│   │   ├── ecosystem.py     ← /solana /base /eth
│   │   └── settings.py      ← /settings /alerts
│   └── services/
│       ├── ai_service.py    ← Multi-model AI fallback chain
│       ├── dexscreener.py   ← DexScreener API client (FREE)
│       ├── coingecko.py     ← CoinGecko API client (FREE)
│       ├── jobs_scraper.py  ← Web3 job board scraper
│       ├── project_analyzer.py ← Scam/legit analyzer
│       ├── formatter.py     ← Telegram message builder
│       └── scheduler.py     ← APScheduler background jobs
├── data/                    ← SQLite database files
├── logs/                    ← Log files
├── .env.example             ← Environment template
├── requirements.txt         ← Python dependencies
├── Procfile                 ← Railway/Heroku process
├── railway.json             ← Railway deployment config
└── README.md                ← This file
```

---

## 🧠 AI Fallback Chain

```
Request → Groq (LLaMA3 70B)
             ↓ (if fails)
         OpenRouter (Mistral 7B free)
             ↓ (if fails)
         Google Gemini Pro
             ↓ (if fails)
         DeepSeek Chat
             ↓ (if all fail)
         Friendly error message
```

---

## 🗄️ Database Schema

SQLite tables:
- `users` — User profiles and settings
- `notes` — Saved notes and links
- `reminders` — Scheduled reminders
- `watchlist` — Tracked projects
- `outreach` — Outreach history
- `conversations` — AI chat history
- `alert_subs` — Alert subscriptions
- `saved_jobs` — Bookmarked job listings

---

## 💰 Cost Breakdown

| Service | Free Limit | Monthly Cost |
|---------|-----------|--------------|
| Railway | 500 hrs/month | $0 |
| Groq API | 14,400 req/day | $0 |
| OpenRouter | Free models | $0 |
| Gemini API | 60 RPM | $0 |
| DeepSeek | Generous | $0 |
| DexScreener | Unlimited | $0 |
| CoinGecko | 30 RPM | $0 |
| SQLite | Unlimited | $0 |
| **TOTAL** | | **$0.00** |

---

## 🔮 Future SaaS Expansion

This architecture is designed to scale:
- Add PostgreSQL → swap SQLite connection
- Add Redis → add caching layer to services
- Add web dashboard → FastAPI + frontend
- Add multiple users → extend auth middleware
- Add premium features → add subscription check middleware
- Add webhooks → swap polling for webhook mode

---

## 📝 License

MIT License — use this freely, build your empire.

---

**⚡ Built for Web3 operators who play to win. Zero budget required.**
