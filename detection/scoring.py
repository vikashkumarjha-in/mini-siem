def web_scanning_score(error_count):
    return min(100, error_count * 10)


def severity_from_score(score):
    if score >= 60:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"
