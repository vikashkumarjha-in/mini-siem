import sqlite3

from config import DATABASE_FILE


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            ip TEXT,
            username TEXT,
            event_type TEXT NOT NULL,
            status TEXT,
            path TEXT,
            http_status INTEGER,
            raw_log TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            ip TEXT NOT NULL,
            source TEXT NOT NULL,
            rule_name TEXT NOT NULL,
            evidence TEXT NOT NULL,
            score INTEGER NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'OPEN'
        )
    """)

    connection.commit()
    connection.close()


def insert_event(event):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events (
            timestamp,
            source,
            ip,
            username,
            event_type,
            status,
            path,
            http_status,
            raw_log
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["timestamp"],
        event["source"],
        event.get("ip"),
        event.get("username"),
        event["event_type"],
        event.get("status"),
        event.get("path"),
        event.get("http_status"),
        event["raw_log"],
    ))

    connection.commit()
    connection.close()


def insert_alert(alert):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            ip,
            source,
            rule_name,
            evidence,
            score,
            severity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        alert["ip"],
        alert["source"],
        alert["rule_name"],
        alert["evidence"],
        alert["score"],
        alert["severity"],
    ))

    connection.commit()
    connection.close()
