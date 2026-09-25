from config import WEB_404_THRESHOLD, ALERT_COOLDOWN_MINUTES
from database.db import get_connection
from detection.scoring import web_scanning_score, severity_from_score


def recent_similar_alert_exists(ip, rule_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM alerts
        WHERE ip = ?
          AND rule_name = ?
          AND datetime(created_at) >= datetime('now', ?)
        ORDER BY id DESC
        LIMIT 1
    """, (
        ip,
        rule_name,
        f"-{ALERT_COOLDOWN_MINUTES} minutes"
    ))

    row = cursor.fetchone()
    connection.close()

    return row is not None


def check_web_rules(event):
    if event["source"] != "apache":
        return []

    if event["http_status"] != 404:
        return []

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS error_count
        FROM events
        WHERE source = 'apache'
          AND ip = ?
          AND http_status = 404
    """, (event["ip"],))

    error_count = cursor.fetchone()["error_count"]
    connection.close()

    if error_count < WEB_404_THRESHOLD:
        return []

    rule_name = "Possible Web Scanning"

    if recent_similar_alert_exists(event["ip"], rule_name):
        return []

    score = web_scanning_score(error_count)

    return [{
        "ip": event["ip"],
        "source": "apache",
        "rule_name": rule_name,
        "evidence": (
            f"{error_count} HTTP 404 responses "
            f"from {event['ip']}"
        ),
        "score": score,
        "severity": severity_from_score(score),
    }]
