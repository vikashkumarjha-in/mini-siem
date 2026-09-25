import re


WEB_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) .*?'
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) '
    r'(?P<path>\S+) [^"]+" '
    r'(?P<http_status>\d{3})'
)


def parse_web_line(line):
    match = WEB_PATTERN.search(line)

    if not match:
        return None

    item = match.groupdict()

    return {
        "timestamp": item["timestamp"],
        "source": "apache",
        "ip": item["ip"],
        "username": None,
        "event_type": "http_request",
        "status": item["http_status"],
        "path": item["path"],
        "http_status": int(item["http_status"]),
        "raw_log": line.strip(),
    }
