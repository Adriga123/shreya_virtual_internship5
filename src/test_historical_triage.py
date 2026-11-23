
import json
from pathlib import Path

from triage_agent import run_triage_agent


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mozilla_cleaned.jsonl"
)

SEVERITY_MAP = {
    "normal": "Medium",
    "minor": "Low",
    "S3": "Medium",
}

COMPONENT_MAP = {
    "File Handling": "File Handling",
}


def load_records():
    records = []

    with open(DATASET_PATH, encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def main():

    records = load_records()

    severity_checked = 0
    severity_correct = 0

    component_checked = 0
    component_correct = 0

    print("\nHISTORICAL MOZILLA TRIAGE VALIDATION")
    print("=" * 65)
    print("Input fields: Title and Description only")

    for record in records:

        # Exclude comments and combined historical content.
        report = {
            "title": record.get("title", ""),
            "description": record.get("description", ""),
        }

        result = run_triage_agent(report)

        original_severity = str(
            record.get("severity", "")
        ).strip()

        expected_severity = SEVERITY_MAP.get(
            original_severity
        )

        original_component = str(
            record.get("component", "")
        ).strip()

        expected_component = COMPONENT_MAP.get(
            original_component
        )

        # Severity comparison
        if expected_severity:

            severity_checked += 1

            if result["severity"] == expected_severity:
                severity_correct += 1
                severity_status = "PASS"
            else:
                severity_status = "FAIL"

        else:
            severity_status = "NOT COMPARED"

        # Component comparison
        if expected_component:

            component_checked += 1

            if (
                result["affected_component"]
                == expected_component
            ):
                component_correct += 1
                component_status = "PASS"
            else:
                component_status = "FAIL"

        else:
            component_status = "NOT COMPARED"

        print(f"\nBug ID: {record.get('bug_id')}")
        print(f"Title: {record.get('title')}")

        print(
            f"Severity: Original={original_severity} | "
            f"Expected={expected_severity or 'Unavailable'} | "
            f"Predicted={result['severity']} | "
            f"{severity_status}"
        )

        print(
            f"Component: Original={original_component} | "
            f"Expected={expected_component or 'Unavailable'} | "
            f"Predicted={result['affected_component']} | "
            f"{component_status}"
        )

        if severity_status == "FAIL":
            print(
                "Matched severity signals:",
                result["matched_severity_signals"]
            )

        if component_status == "FAIL":
            print(
                "Matched component signals:",
                result["matched_component_signals"]
            )

    print("\n" + "=" * 65)
    print("VALIDATION SUMMARY")
    print("=" * 65)

    print(
        f"Severity: {severity_correct}/{severity_checked} correct"
    )

    print(
        f"Component: {component_correct}/{component_checked} correct"
    )

    if severity_checked:
        print(
            "Severity agreement:",
            f"{severity_correct / severity_checked * 100:.2f}%"
        )

    if component_checked:
        print(
            "Component agreement:",
            f"{component_correct / component_checked * 100:.2f}%"
        )

    print("\nNote:")
    print("Only historical title and description were evaluated.")
    print("Scores represent agreement with provisional label mappings.")


if __name__ == "__main__":
    main()
