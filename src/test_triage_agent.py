
from triage_agent import run_triage_agent

# --------------------------------------------------
# TRIAGE AGENT VALIDATION DATASET
# --------------------------------------------------

test_cases = [

    {
        "name": "Critical production outage",
        "report": {
            "title": "Production system down",
            "description": "Complete production outage affecting all users."
        },
        "severity": "Critical",
        "priority": "P1",
        "component": "Unknown / Unclassified"
    },

    {
        "name": "High authentication failure",
        "report": {
            "title": "Application crashes during login",
            "description": "Users cannot login due to authentication failure."
        },
        "severity": "High",
        "priority": "P2",
        "component": "Authentication"
    },

    {
        "name": "Medium network timeout",
        "report": {
            "title": "Network connection timeout",
            "description": "API request sometimes fails due to network timeout."
        },
        "severity": "Medium",
        "priority": "P3",
        "component": "Network"
    },

    {
        "name": "Low UI alignment issue",
        "report": {
            "title": "Button alignment issue",
            "description": "Minor cosmetic issue in the user interface."
        },
        "severity": "Low",
        "priority": "P4",
        "component": "User Interface"
    },

    {
        "name": "Medium performance issue",
        "report": {
            "title": "Profile Page Loading Slowly",
            "description": "The user profile page takes more than 20 seconds to load."
        },
        "severity": "Medium",
        "priority": "P3",
        "component": "Performance"
    },

    {
        "name": "Medium search failure",
        "report": {
            "title": "Search Function Not Working",
            "description": "The application search function does not return any results."
        },
        "severity": "Medium",
        "priority": "P3",
        "component": "Search"
    },

    {
        "name": "High payment failure",
        "report": {
            "title": "Payment failure during checkout",
            "description": "Users cannot complete payment transactions."
        },
        "severity": "High",
        "priority": "P2",
        "component": "Payment"
    },

    {
        "name": "Medium database query failure",
        "report": {
            "title": "Database query fails",
            "description": "SQL query fails intermittently when accessing the database."
        },
        "severity": "Medium",
        "priority": "P3",
        "component": "Database"
    },

    {
        "name": "Medium file upload failure",
        "report": {
            "title": "PDF upload not working",
            "description": "Users cannot upload PDF documents."
        },
        "severity": "Medium",
        "priority": "P3",
        "component": "File Handling"
    },

    {
        "name": "High memory failure",
        "report": {
            "title": "Application memory leak",
            "description": "The application experiences a memory leak and eventually crashes."
        },
        "severity": "High",
        "priority": "P2",
        "component": "Memory Management"
    }
]


# --------------------------------------------------
# RUN VALIDATION
# --------------------------------------------------

total_checks = 0
passed_checks = 0
failed_cases = []

print("\nTRIAGE AGENT VALIDATION")
print("=" * 65)

for test in test_cases:

    result = run_triage_agent(test["report"])

    print(f"\nTest: {test['name']}")

    checks = {
        "severity": test["severity"],
        "priority": test["priority"],
        "affected_component": test["component"]
    }

    case_failed = False

    for field, expected in checks.items():

        actual = result[field]
        success = actual == expected

        total_checks += 1

        if success:
            passed_checks += 1
        else:
            case_failed = True

        print(
            f"{field}: Expected={expected} | "
            f"Actual={actual} | "
            f"{'PASS' if success else 'FAIL'}"
        )

    if case_failed:
        failed_cases.append(test["name"])

    print("Confidence:", result["confidence_score"])
    print("Reasoning:", result["reasoning"])


# --------------------------------------------------
# VALIDATION SUMMARY
# --------------------------------------------------

accuracy = (
    (passed_checks / total_checks) * 100
    if total_checks > 0 else 0
)

print("\n" + "=" * 65)
print("VALIDATION SUMMARY")
print("=" * 65)

print("Test cases:", len(test_cases))
print("Total checks:", total_checks)
print("Checks passed:", passed_checks)
print("Checks failed:", total_checks - passed_checks)
print(f"Field-level accuracy: {accuracy:.2f}%")

if failed_cases:
    print("\nFailed test cases:")
    for name in failed_cases:
        print("-", name)
else:
    print("\nAll test cases passed.")

print("\nValidation completed.")
