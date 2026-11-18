
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "raw" / "mozilla_bugs.jsonl"
OUTPUT = ROOT / "data" / "raw" / "mozilla_bug_details.jsonl"

with INPUT.open("r", encoding="utf-8") as file:
    bugs = [json.loads(line) for line in file if line.strip()]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

successful = 0

with OUTPUT.open("w", encoding="utf-8") as output:

    for bug in bugs:

        bug_id = bug["id"]

        url = f"https://bugzilla.mozilla.org/rest/bug/{bug_id}/comment"

        request = Request(
            url,
            headers={"User-Agent": "IntelligentBugDiagnosisProject/1.0"}
        )

        try:
            with urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))

            comments = data.get("bugs", {}).get(
                str(bug_id), {}
            ).get("comments", [])

            public_comments = [
                comment["text"]
                for comment in comments
                if not comment.get("is_private", False)
            ]

            record = {
                **bug,
                "description": public_comments[0] if public_comments else "",
                "comments": public_comments,
                "source_url": f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug_id}"
            }

            output.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            successful += 1

            print(f"Retrieved bug {bug_id}")

            time.sleep(0.2)

        except Exception as error:
            print(f"Failed to retrieve bug {bug_id}: {error}")

print(f"\nSuccessfully processed {successful} of {len(bugs)} bugs.")
print(f"Output saved to: {OUTPUT}")
