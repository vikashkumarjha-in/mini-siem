# Contributing to Mini-SIEM

Thanks for contributing! To keep five people working in parallel without conflicts, please follow these rules.

## Branching

```
main
develop
feature/backend-abhay
feature/parser-shivani
feature/detection-aditya
feature/dashboard-bhanu
feature/testing-vikash
```

- **Never** commit directly to `main`.
- Work only inside your assigned module folder unless coordinating with its owner.
- Rebase/pull `develop` regularly to avoid large conflicts.

## Commit Messages

Use clear, action-based messages:

```
git commit -m "Add SSH authentication log parser"
git commit -m "Fix false positive in web_scan.py threshold"
```

## Pull Request Flow

```
feature branch → commit → push → Pull Request → review → tests → develop → integration test → main
```

Before opening a PR, confirm:

1. Does this change only affect your assigned module?
2. Does it follow the common event schema?
3. Does it break another module?
4. Does the application still run end-to-end (`uvicorn backend.app:app --reload`)?

Only open the PR once 1–3 are "no" and 4 is "yes".

## Code Ownership

| Folder | Owner |
|---|---|
| `backend/`, `database/` | Abhay |
| `parser/`, `data/` | Shivani |
| `detection/` | Aditya |
| `dashboard/` | Bhanu |
| `tests/`, `docs/`, `reports/`, `presentation/`, `.github/`, `README.md` | Vikash |

Only **Vikash** (QA/Release Lead) and **Abhay** (Integration Lead) approve merges into `main`.

## Running the App Locally

```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Dashboard: http://127.0.0.1:8000
API docs:  http://127.0.0.1:8000/docs

## Testing

Run the full suite before opening a PR:

```bash
pytest
```

## Common Event Schema

All parsers (SSH, web, firewall, Windows, network) must output events in this shape so detection code stays decoupled from parsing code:

```json
{
    "timestamp": "2026-09-25 10:22:41",
    "source": "ssh",
    "event_type": "authentication",
    "ip": "192.168.1.50",
    "username": "admin",
    "action": "login",
    "result": "failed",
    "url": null,
    "status_code": null
}
```

## Detection Rule Format

New rules go in `detection/` and should register with `rule_id`, `severity`, `threshold`, and `time_window` so they surface correctly on the Rules page and in `rules` table.
