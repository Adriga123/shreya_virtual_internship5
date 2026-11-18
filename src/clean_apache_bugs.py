
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "raw" / "apache_bugs.jsonl"
OUTPUT = ROOT / "data" / "processed" / "apache_cleaned.jsonl"


def clean_text(value):
    if not value:
        return ""

    value = re.sub(r"\s+", " ", str(value))
    return value.strip()


OUTPUT.parent.mkdir(parents=True, exist_ok=True)

processed = 0

with INPUT.open("r", encoding="utf-8") as source:
    with OUTPUT.open("w", encoding="utf-8") as destination:

        for line in source:
            if not line.strip():
                continue

            bug = json.loads(line)

            comments = [
                clean_text(comment)
                for comment in bug.get("comments", [])
                if clean_text(comment)
            ]

            components = bug.get("components", [])

            record = {
                "bug_id": bug.get("key", ""),
                "title": clean_text(bug.get("summary", "")),
                "description": clean_text(bug.get("description", "")),
                "comments": comments,
                "component": ", ".join(components),
                "project": clean_text(bug.get("project", "")),
                "priority": clean_text(bug.get("priority", "")),
                "status": clean_text(bug.get("status", "")),
                "resolution": clean_text(bug.get("resolution", "")),
                "issue_type": clean_text(bug.get("issue_type", "")),
                "source": "Apache Jira",
                "source_url": bug.get("source_url", "")
            }

            record["content"] = " ".join([
                record["title"],
                record["description"],
                " ".join(record["comments"]),
                record["component"],
                record["project"]
            ]).strip()

            destination.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            processed += 1

print(f"Successfully cleaned {processed} Apache bug records.")
print(f"Cleaned dataset saved to: {OUTPUT}")
