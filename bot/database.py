"""
NexusBot Database Layer
=======================
SQLite with aiosqlite for async operations.
Tables: users, notes, reminders, watchlist, outreach, conversations, alerts
"""
import os
import aiosqlite
import asyncio
from datetime import datetime
from loguru import logger
from bot.config import DB_PATH


async def init_db():
    """Initialize all database tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                joined_at   TEXT DEFAULT (datetime('now')),
                settings    TEXT DEFAULT '{}',
                is_active   INTEGER DEFAULT 1
            )
        """)

        # Notes table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                content     TEXT NOT NULL,
                tags        TEXT DEFAULT '',
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Reminders table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                message     TEXT NOT NULL,
                remind_at   TEXT NOT NULL,
                is_sent     INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Watchlist table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                project     TEXT NOT NULL,
                token       TEXT DEFAULT '',
                chain       TEXT DEFAULT '',
                url         TEXT DEFAULT '',
                notes       TEXT DEFAULT '',
                added_at    TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Outreach history table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS outreach (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                project     TEXT NOT NULL,
                contact     TEXT DEFAULT '',
                message     TEXT NOT NULL,
                platform    TEXT DEFAULT 'telegram',
                status      TEXT DEFAULT 'sent',
                notes       TEXT DEFAULT '',
                sent_at     TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Conversations table (AI chat history)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                role        TEXT NOT NULL,
                content     TEXT NOT NULL,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Alert subscriptions
        await db.execute("""
            CREATE TABLE IF NOT EXISTS alert_subs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                alert_type  TEXT NOT NULL,
                is_active   INTEGER DEFAULT 1,
                created_at  TEXT DEFAULT (datetime('now')),
                UNIQUE(user_id, alert_type),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Saved jobs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS saved_jobs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT NOT NULL,
                company     TEXT DEFAULT '',
                url         TEXT DEFAULT '',
                job_type    TEXT DEFAULT 'web3',
                saved_at    TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()
        logger.success("✅ Database initialized successfully")


# ─── User Operations ───────────────────────────────────────────────────────────

async def upsert_user(user_id: int, username: str = "", first_name: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name
        """, (user_id, username, first_name))
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_all_users() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT user_id FROM users WHERE is_active = 1") as cur:
            rows = await cur.fetchall()
            return [row["user_id"] for row in rows]


# ─── Notes Operations ──────────────────────────────────────────────────────────

async def save_note(user_id: int, content: str, tags: str = "") -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO notes (user_id, content, tags) VALUES (?, ?, ?)",
            (user_id, content, tags)
        )
        await db.commit()
        return cur.lastrowid


async def get_notes(user_id: int, limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def delete_note(note_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)
        )
        await db.commit()
        return True


# ─── Reminders Operations ──────────────────────────────────────────────────────

async def add_reminder(user_id: int, message: str, remind_at: datetime) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO reminders (user_id, message, remind_at) VALUES (?, ?, ?)",
            (user_id, message, remind_at.isoformat())
        )
        await db.commit()
        return cur.lastrowid


async def get_due_reminders() -> list:
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM reminders WHERE remind_at <= ? AND is_sent = 0",
            (now,)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def mark_reminder_sent(reminder_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE reminders SET is_sent = 1 WHERE id = ?", (reminder_id,)
        )
        await db.commit()


# ─── Watchlist Operations ──────────────────────────────────────────────────────

async def add_to_watchlist(user_id: int, project: str, token: str = "",
                            chain: str = "", url: str = "", notes: str = "") -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO watchlist (user_id, project, token, chain, url, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, project, token, chain, url, notes)
        )
        await db.commit()
        return cur.lastrowid


async def get_watchlist(user_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM watchlist WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def remove_from_watchlist(item_id: int, user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM watchlist WHERE id = ? AND user_id = ?", (item_id, user_id)
        )
        await db.commit()


# ─── Outreach Operations ───────────────────────────────────────────────────────

async def log_outreach(user_id: int, project: str, contact: str,
                        message: str, platform: str = "telegram") -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO outreach (user_id, project, contact, message, platform) VALUES (?, ?, ?, ?, ?)",
            (user_id, project, contact, message, platform)
        )
        await db.commit()
        return cur.lastrowid


async def get_outreach_history(user_id: int, limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM outreach WHERE user_id = ? ORDER BY sent_at DESC LIMIT ?",
            (user_id, limit)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


# ─── Conversation Operations ───────────────────────────────────────────────────

async def save_message(user_id: int, role: str, content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        await db.commit()


async def get_conversation(user_id: int, limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT role, content FROM conversations 
               WHERE user_id = ? ORDER BY created_at DESC LIMIT ?""",
            (user_id, limit)
        ) as cur:
            rows = [dict(r) for r in await cur.fetchall()]
            return list(reversed(rows))


async def clear_conversation(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        await db.commit()


# ─── Alert Subscriptions ───────────────────────────────────────────────────────

ALERT_TYPES = ["alpha", "jobs", "whale", "memecoins", "airdrops", "trending"]


async def subscribe_alert(user_id: int, alert_type: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO alert_subs (user_id, alert_type) VALUES (?, ?)
               ON CONFLICT(user_id, alert_type) DO UPDATE SET is_active = 1""",
            (user_id, alert_type)
        )
        await db.commit()


async def unsubscribe_alert(user_id: int, alert_type: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE alert_subs SET is_active = 0 WHERE user_id = ? AND alert_type = ?",
            (user_id, alert_type)
        )
        await db.commit()


async def get_alert_subscribers(alert_type: str) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT user_id FROM alert_subs WHERE alert_type = ? AND is_active = 1",
            (alert_type,)
        ) as cur:
            return [r["user_id"] for r in await cur.fetchall()]


async def get_user_alerts(user_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT alert_type, is_active FROM alert_subs WHERE user_id = ?",
            (user_id,)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]
