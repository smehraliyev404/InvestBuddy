# Database module for InvestBuddy
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

# SQLite database file path
DATABASE_PATH = "investbuddy.db"

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create all tables
def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table - stores basic user session information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Conversations table - stores chat messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES users(session_id)
        )
    """)

    # Recommendations table - stores investment recommendations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            salary REAL,
            savings REAL,
            monthly_expenses REAL,
            debt REAL,
            goal TEXT,
            time_horizon INTEGER,
            portfolio JSON,
            recommendation_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES users(session_id)
        )
    """)

    # Create indexes for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversations_session
        ON conversations(session_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_recommendations_session
        ON recommendations(session_id)
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Create or get user session
def create_or_get_user(session_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Try to get existing user
    cursor.execute("SELECT id FROM users WHERE session_id = ?", (session_id,))
    user = cursor.fetchone()

    if user:
        # Update last active time
        cursor.execute(
            "UPDATE users SET last_active = ? WHERE session_id = ?",
            (datetime.now(), session_id)
        )
        user_id = user[0]
    else:
        # Create new user
        cursor.execute(
            "INSERT INTO users (session_id) VALUES (?)",
            (session_id,)
        )
        user_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return user_id

# Save conversation message
def save_message(session_id: str, role: str, content: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )

    conn.commit()
    conn.close()

# Get conversation history
def get_conversation_history(session_id: str, limit: int = 50) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT role, content, timestamp
           FROM conversations
           WHERE session_id = ?
           ORDER BY timestamp ASC
           LIMIT ?""",
        (session_id, limit)
    )

    messages = []
    for row in cursor.fetchall():
        messages.append({
            "role": row[0],
            "content": row[1],
            "timestamp": row[2]
        })

    conn.close()
    return messages

# Save investment recommendation
def save_recommendation(
    session_id: str,
    salary: float,
    savings: float,
    monthly_expenses: float,
    debt: float,
    goal: str,
    time_horizon: int,
    portfolio: Dict,
    recommendation_text: str
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO recommendations
           (session_id, salary, savings, monthly_expenses, debt, goal,
            time_horizon, portfolio, recommendation_text)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (session_id, salary, savings, monthly_expenses, debt, goal,
         time_horizon, json.dumps(portfolio), recommendation_text)
    )

    conn.commit()
    conn.close()

# Get user's latest recommendation
def get_latest_recommendation(session_id: str) -> Optional[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM recommendations
           WHERE session_id = ?
           ORDER BY created_at DESC
           LIMIT 1""",
        (session_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "session_id": row[1],
            "salary": row[2],
            "savings": row[3],
            "monthly_expenses": row[4],
            "debt": row[5],
            "goal": row[6],
            "time_horizon": row[7],
            "portfolio": json.loads(row[8]) if row[8] else {},
            "recommendation_text": row[9],
            "created_at": row[10]
        }
    return None

# Clear conversation history
def clear_conversation(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))

    conn.commit()
    conn.close()

# Initialize database on module import
if __name__ == "__main__":
    init_database()
