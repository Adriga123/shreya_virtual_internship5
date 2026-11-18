
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SAMPLE_KB = ROOT / "data" / "sample" / "historical_defects.jsonl"
MOZILLA_KB = ROOT / "data" / "processed" / "mozilla_cleaned.jsonl"
APACHE_KB = ROOT / "data" / "processed" / "apache_cleaned.jsonl"
ECLIPSE_KB = ROOT / "data" / "processed" / "eclipse_cleaned.jsonl"


def load_jsonl(path):
    records = []

    if not path.exists():
        return records

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def load_defects():
    records = []

    records.extend(load_jsonl(SAMPLE_KB))
    records.extend(load_jsonl(MOZILLA_KB))
    records.extend(load_jsonl(APACHE_KB))
    records.extend(load_jsonl(ECLIPSE_KB))

    return records
