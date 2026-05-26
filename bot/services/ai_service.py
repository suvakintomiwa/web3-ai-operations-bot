"""
NexusBot AI Service
====================
Multi-model AI with automatic fallback chain:
  1. Groq (LLaMA 3 70B) — Primary: fastest, best quality on free tier
  2. OpenRouter (Mistral 7B free) — Fallback 1
  3. Google Gemini Pro — Fallback 2
  4. DeepSeek Chat — Fallback 3 (last resort)
"""
import asyncio
import aiohttp
import json
from loguru import logger
from bot.config import (
    GROQ_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY,
    GROQ_MODEL, OPENROUTER_MODEL, GEMINI_MODEL, DEEPSEEK_MODEL,
    AI_MAX_TOKENS, AI_TEMPERATURE
)

# ─── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are NexusBot — a futuristic Web3 AI assistant for a solo crypto operator.

Your user is a community manager, raid leader, KOL outreach specialist, NFT artist, and crypto alpha hunter.

You help with:
- Writing raid messages, shill threads, and KOL DMs
- Analyzing crypto projects for legitimacy and potential
- Finding Web3 job opportunities and drafting applications
- Creating engagement strategies for Telegram/Discord/Twitter
- Summarizing tokenomics, whitepapers, and launch details
- Alpha hunting insights and market trend analysis
- Community growth tactics and moderation strategies

Tone: Confident, direct, cyberpunk-flavored. Use emojis strategically. Be helpful and concise.
Format: Use Telegram-compatible markdown. Bold key terms with **. Use bullet points liberally.
Always end with an actionable tip or next step."""


# ─── Groq Client ──────────────────────────────────────────────────────────────
async def _call_groq(messages: list, max_tokens: int = AI_MAX_TOKENS) -> str:
    if not GROQ_API_KEY:
        raise ValueError("No Groq API key")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": AI_TEMPERATURE,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Groq error {resp.status}: {text[:200]}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


# ─── OpenRouter Client ─────────────────────────────────────────────────────────
async def _call_openrouter(messages: list, max_tokens: int = AI_MAX_TOKENS) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("No OpenRouter API key")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nexusbot.app",
        "X-Title": "NexusBot"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": AI_TEMPERATURE,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=40)) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"OpenRouter error {resp.status}: {text[:200]}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


# ─── Gemini Client ─────────────────────────────────────────────────────────────
async def _call_gemini(messages: list, max_tokens: int = AI_MAX_TOKENS) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("No Gemini API key")

    # Convert messages to Gemini format
    contents = []
    for msg in messages:
        if msg["role"] == "system":
            continue  # Gemini handles system via first user message
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Add system prompt to first user message if no user message yet
    if contents and contents[0]["role"] == "user":
        sys_content = next((m["content"] for m in messages if m["role"] == "system"), "")
        if sys_content:
            contents[0]["parts"][0]["text"] = f"{sys_content}\n\n{contents[0]['parts'][0]['text']}"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": AI_TEMPERATURE,
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=40)) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Gemini error {resp.status}: {text[:200]}")
            data = await resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]


# ─── DeepSeek Client ───────────────────────────────────────────────────────────
async def _call_deepseek(messages: list, max_tokens: int = AI_MAX_TOKENS) -> str:
    if not DEEPSEEK_API_KEY:
        raise ValueError("No DeepSeek API key")

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": AI_TEMPERATURE,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=40)) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"DeepSeek error {resp.status}: {text[:200]}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


# ─── Main AI Function (with fallback) ──────────────────────────────────────────
async def ask_ai(prompt: str, context: list = None, max_tokens: int = AI_MAX_TOKENS) -> tuple[str, str]:
    """
    Ask the AI with automatic fallback chain.
    Returns: (response_text, model_used)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation context
    if context:
        messages.extend(context[-8:])  # Keep last 8 messages for context

    messages.append({"role": "user", "content": prompt})

    providers = [
        ("Groq (LLaMA3)", _call_groq),
        ("OpenRouter (Mistral)", _call_openrouter),
        ("Google Gemini", _call_gemini),
        ("DeepSeek", _call_deepseek),
    ]

    for name, func in providers:
        try:
            logger.info(f"🤖 Trying AI provider: {name}")
            response = await func(messages, max_tokens)
            logger.success(f"✅ AI response from {name}")
            return response, name
        except Exception as e:
            logger.warning(f"⚠️ {name} failed: {str(e)[:100]}")
            await asyncio.sleep(1)
            continue

    # All providers failed
    return (
        "⚠️ All AI services are temporarily unavailable. Please try again in a moment. "
        "This is rare — usually resolves within 60 seconds.",
        "none"
    )


# ─── Specialized AI Functions ──────────────────────────────────────────────────

async def generate_raid_message(project_name: str, chain: str, context: str = "") -> str:
    prompt = f"""Write a HIGH-ENERGY raid message for {project_name} on {chain}.

Additional context: {context}

Requirements:
- Start with 🚀 or similar hype emoji
- Include strong call to action (LIKE/RETWEET/COMMENT)
- Add relevant hashtags (3-5)
- Max 2 sentences for impact
- Cyberpunk / degen tone
- Include the project name prominently
- End with a rallying cry

Format it ready to paste directly into Telegram/Twitter."""

    response, _ = await ask_ai(prompt, max_tokens=300)
    return response


async def generate_kol_dm(project_name: str, my_role: str, target: str = "KOL") -> str:
    prompt = f"""Write a professional but crypto-native KOL outreach DM.

Project to pitch: {project_name}
My role/services: {my_role}
Target: {target}

Requirements:
- Start with their name placeholder [Name]
- Keep it under 150 words
- Mention specific value I can provide
- Crypto-native language (not corporate)
- Include a clear ask (collab, shoutout, partnership)
- End with a question to drive response
- Make it feel personal, not copy-paste

Write the DM ready to send."""

    response, _ = await ask_ai(prompt, max_tokens=400)
    return response


async def generate_shill_thread(project_name: str, details: str) -> str:
    prompt = f"""Create a Twitter/X shill thread for: {project_name}

Project details: {details}

Format as a numbered thread:
Tweet 1: Hook (most important — make them stop scrolling)
Tweet 2: What makes it unique
Tweet 3: Tokenomics or opportunity 
Tweet 4: Community & socials
Tweet 5: Call to action + hashtags

Use emojis. Keep each tweet under 280 chars. Make it VIRAL-worthy.
Crypto-degen tone but factual."""

    response, _ = await ask_ai(prompt, max_tokens=600)
    return response


async def analyze_project_ai(project_info: str) -> str:
    prompt = f"""Analyze this crypto project and give a structured assessment:

{project_info}

Provide:
📊 **LEGITIMACY SCORE**: X/100
🚨 **SCAM RISK**: LOW/MEDIUM/HIGH  
💎 **POTENTIAL**: X/10
📈 **MARKET ANALYSIS**: Brief assessment
✅ **GREEN FLAGS**: List 3 positives (if any)
🚩 **RED FLAGS**: List concerns (be specific)
🎯 **VERDICT**: GO / WAIT / AVOID
💡 **ACTION**: What should I do right now?

Be direct and honest. Lives and wallets depend on accuracy."""

    response, _ = await ask_ai(prompt, max_tokens=600)
    return response


async def generate_mod_reply(situation: str) -> str:
    prompt = f"""As a professional Telegram/Discord moderator, write a firm but fair reply for:

Situation: {situation}

Requirements:
- Professional but clear
- Match crypto community tone
- Include action taken (if warning/ban)
- Keep under 100 words
- Use appropriate emojis
- End with community reminder if needed"""

    response, _ = await ask_ai(prompt, max_tokens=200)
    return response


async def generate_engagement_strategy(project: str, platform: str, goal: str) -> str:
    prompt = f"""Create a 7-day engagement strategy for: {project}
Platform: {platform}
Goal: {goal}

Include:
- Daily posting schedule
- Content types for each day
- Hashtag strategy
- Engagement tactics (polls, AMAs, contests)
- KPIs to track
- Community growth hacks specific to Web3

Make it actionable and realistic for a solo operator."""

    response, _ = await ask_ai(prompt, max_tokens=800)
    return response
