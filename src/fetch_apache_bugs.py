
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "apache_bugs.jsonl"

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"

params = {
    "jql": "project = HADOOP ORDER BY updated DESC",
    "startAt": 0,
    "maxResults": 20,
    "fields": (
        "summary,description,status,resolution,project,"
        "components,priority,issuetype,created,updated,comment"
    )
}

url = BASE_URL + "?" + urlencode(params)

request = Request(
    url,
    headers={"User-Agent": "IntelligentBugDiagnosisProject/1.0"}
)

try:
    with urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    issues = data.get("issues", [])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as file:

        for issue in issues:
            fields = issue.get("fields", {})

            comment_data = fields.get("comment") or {}
            comments = [
                comment.get("body", "")
                for comment in comment_data.get("comments", [])
                if comment.get("body")
            ]

            record = {
                "id": issue.get("id", ""),
                "key": issue.get("key", ""),
                "summary": fields.get("summary", ""),
                "description": fields.get("description") or "",
                "status": (fields.get("status") or {}).get("name", ""),
                "resolution": (
                    (fields.get("resolution") or {}).get("name", "")
                ),
                "project": (fields.get("project") or {}).get("name", ""),
                "components": [
                    component.get("name", "")
                    for component in fields.get("components", [])
                ],
                "priority": (fields.get("priority") or {}).get("name", ""),
                "issue_type": (fields.get("issuetype") or {}).get("name", ""),
                "created": fields.get("created", ""),
                "updated": fields.get("updated", ""),
                "comments": comments,
                "source_url": (
                    f"https://issues.apache.org/jira/browse/{issue.get('key', '')}"
                )
            }

            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            print(f"Retrieved Apache issue {issue.get('key')}")

    print(f"\nSuccessfully processed {len(issues)} Apache issues.")
    print(f"Output saved to: {OUTPUT}")

except Exception as error:
    print("Download failed:", error)
