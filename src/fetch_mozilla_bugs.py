
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "mozilla_bugs.jsonl"

BASE_URL = "https://bugzilla.mozilla.org/rest/bug"

params = {
    "product": "Firefox",
    "limit": 20,
    "order": "last_change_time DESC",
    "include_fields": (
        "id,summary,status,resolution,product,component,"
        "severity,priority,creation_time,last_change_time"
    )
}

url = BASE_URL + "?" + urlencode(params)

request = Request(
    url,
    headers={"User-Agent": "IntelligentBugDiagnosisProject/1.0"}
)

try:
    with urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    bugs = data.get("bugs", [])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as file:
        for bug in bugs:
            file.write(json.dumps(bug, ensure_ascii=False) + "\n")

    print(f"Successfully downloaded {len(bugs)} Mozilla bug records.")
    print(f"Saved to: {OUTPUT}")

except Exception as error:
    print("Download failed:", error)
