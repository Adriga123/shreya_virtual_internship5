
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "raw" / "mozilla_bug_details.jsonl"
OUTPUT = ROOT / "data" / "processed" / "mozilla_cleaned.jsonl"


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

            record = {
                "bug_id": str(bug.get("id", "")),
                "title": clean_text(bug.get("summary", "")),
                "description": clean_text(bug.get("description", "")),
                "comments": comments,
                "product": clean_text(bug.get("product", "")),
                "component": clean_text(bug.get("component", "")),
                "severity": clean_text(bug.get("severity", "")),
                "priority": clean_text(bug.get("priority", "")),
                "status": clean_text(bug.get("status", "")),
                "resolution": clean_text(bug.get("resolution", "")),
                "source": "Mozilla Bugzilla",
                "source_url": bug.get("source_url", "")
            }

            record["content"] = " ".join([
                record["title"],
                record["description"],
                " ".join(record["comments"]),
                record["component"],
                record["product"]
            ]).strip()

            destination.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            processed += 1

print(f"Successfully cleaned {processed} Mozilla bug records.")
print(f"Cleaned dataset saved to: {OUTPUT}")
