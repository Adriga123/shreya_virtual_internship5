import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KB = ROOT / "data" / "sample" / "historical_defects.jsonl"

def load_defects(path=DEFAULT_KB):
    records = []
    path = Path(path)
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
