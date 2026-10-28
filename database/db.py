import sqlite3
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash


DATABASE_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    connection = get_db()
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def seed_db():
    connection = get_db()
    try:
        existing_user = connection.execute(
            "SELECT 1 FROM users LIMIT 1"
        ).fetchone()
        if existing_user:
            return

        cursor = connection.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                "Demo User",
                "demo@spendly.com",
                generate_password_hash("demo123"),
            ),
        )
        user_id = cursor.lastrowid

        today = date.today()
        days_elapsed = (today - today.replace(day=1)).days
        dates = [
            today.replace(day=1 + round(days_elapsed * index / 7)).isoformat()
            for index in range(8)
        ]
        expenses = [
            (user_id, 250.0, "Food", dates[0], "Lunch"),
            (user_id, 120.0, "Transport", dates[1], "Metro fare"),
            (user_id, 850.0, "Bills", dates[2], "Internet bill"),
            (user_id, 400.0, "Health", dates[3], "Pharmacy"),
            (user_id, 350.0, "Entertainment", dates[4], "Movie ticket"),
            (user_id, 1200.0, "Shopping", dates[5], "Household items"),
            (user_id, 180.0, "Other", dates[6], "Miscellaneous"),
            (user_id, 320.0, "Food", dates[7], "Groceries"),
        ]
        connection.executemany(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            expenses,
        )
        connection.commit()
    finally:
        connection.close()
