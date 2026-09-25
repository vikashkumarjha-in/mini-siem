import sqlite3

from flask import Flask, jsonify, render_template

from config import DATABASE_FILE

app = Flask(__name__)


def query_database(query, parameters=()):
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(query, parameters)

    rows = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return rows


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/summary")
def summary_api():
    total_events = query_database(
        "SELECT COUNT(*) AS count FROM events"
    )[0]["count"]

    total_alerts = query_database(
        "SELECT COUNT(*) AS count FROM alerts"
    )[0]["count"]

    high_alerts = query_database("""
        SELECT COUNT(*) AS count
        FROM alerts
        WHERE severity = 'HIGH'
    """)[0]["count"]

    suspicious_ips = query_database("""
        SELECT COUNT(DISTINCT ip) AS count
        FROM alerts
    """)[0]["count"]

    return jsonify({
        "total_events": total_events,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "suspicious_ips": suspicious_ips,
    })


@app.route("/api/alerts")
def alerts_api():
    alerts = query_database("""
        SELECT id, created_at, ip, source, rule_name,
               evidence, score, severity, status
        FROM alerts
        ORDER BY id DESC
        LIMIT 100
    """)

    return jsonify(alerts)


@app.route("/api/charts")
def charts_api():
    web_404s = query_database("""
        SELECT ip, COUNT(*) AS count
        FROM events
        WHERE source = 'apache'
          AND http_status = 404
        GROUP BY ip
        ORDER BY count DESC
    """)

    severity = query_database("""
        SELECT severity, COUNT(*) AS count
        FROM alerts
        GROUP BY severity
    """)

    return jsonify({
        "web_404s": web_404s,
        "severity": severity,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
