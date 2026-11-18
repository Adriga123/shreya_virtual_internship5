
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "eclipse_bugs.jsonl"

BASE_URL = (
    "https://api.github.com/repos/"
    "eclipse-platform/eclipse.platform.ui/issues"
)

params = "?state=all&per_page=100"

request = Request(
    BASE_URL + params,
    headers={
        "User-Agent": "IntelligentBugDiagnosisProject/1.0",
        "Accept": "application/vnd.github+json"
    }
)

try:
    with urlopen(request, timeout=60) as response:
        issues = json.loads(response.read().decode("utf-8"))

    records = []

    for issue in issues:
        # Skip pull requests; retain actual issues only.
        if "pull_request" in issue:
            continue

        record = {
            "id": issue.get("id", ""),
            "number": issue.get("number", ""),
            "title": issue.get("title", ""),
            "description": issue.get("body") or "",
            "state": issue.get("state", ""),
            "created_at": issue.get("created_at", ""),
            "updated_at": issue.get("updated_at", ""),
            "comments_count": issue.get("comments", 0),
            "source": "Eclipse Platform GitHub",
            "source_url": issue.get("html_url", "")
        }

        records.append(record)

        if len(records) == 20:
            break

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    print(f"Successfully processed {len(records)} Eclipse issues.")
    print(f"Output saved to: {OUTPUT}")

except Exception as error:
    print("Download failed:", error)
