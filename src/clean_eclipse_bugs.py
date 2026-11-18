
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "raw" / "eclipse_bugs.jsonl"
OUTPUT = ROOT / "data" / "processed" / "eclipse_cleaned.jsonl"


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

            record = {
                "bug_id": str(bug.get("number", "")),
                "title": clean_text(bug.get("title", "")),
                "description": clean_text(bug.get("description", "")),
                "comments_count": bug.get("comments_count", 0),
                "status": clean_text(bug.get("state", "")),
                "created_at": bug.get("created_at", ""),
                "updated_at": bug.get("updated_at", ""),
                "source": "Eclipse Platform GitHub",
                "source_url": bug.get("source_url", "")
            }

            record["content"] = " ".join([
                record["title"],
                record["description"]
            ]).strip()

            destination.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            processed += 1

print(f"Successfully cleaned {processed} Eclipse bug records.")
print(f"Cleaned dataset saved to: {OUTPUT}")
