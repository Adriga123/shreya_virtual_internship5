
from agent_orchestrator import run_agent_orchestrator


# --------------------------------------------------
# ORCHESTRATOR VALIDATION DATASET
# --------------------------------------------------

test_cases = [

    {
        "name": "Complete bug report",
        "report": {
            "title": "Application crashes during login",
            "description": "Users cannot login because authentication fails.",
            "stack_trace": """
            java.lang.NullPointerException: User object is null
            at com.example.LoginService.authenticate(LoginService.java:45)
            at com.example.LoginController.login(LoginController.java:22)
            """,
            "error_logs": "Authentication failure during login request."
        },
        "overall": "Completed",
        "triage": "Completed",
        "log_analysis": "Completed"
    },

    {
        "name": "Report without logs",
        "report": {
            "title": "Profile page loading slowly",
            "description": "The user profile page takes more than 20 seconds to load."
        },
        "overall": "Partial",
        "triage": "Completed",
        "log_analysis": "Incomplete"
    },

    {
        "name": "Logs without description",
        "report": {
            "logs": """
            ValueError: Invalid input
            Traceback (most recent call last):
              File "app.py", line 28, in process_data
                int("hello")
            """
        },
        "overall": "Completed",
        "triage": "Completed",
        "log_analysis": "Completed"
    },

    {
        "name": "Empty bug report",
        "report": {},
        "overall": "Partial",
        "triage": "Incomplete",
        "log_analysis": "Incomplete"
    },

    {
        "name": "Invalid report input",
        "report": None,
        "overall": "Partial",
        "triage": "Incomplete",
        "log_analysis": "Incomplete"
    }
]


# --------------------------------------------------
# RUN VALIDATION
# --------------------------------------------------

total_checks = 0
passed_checks = 0
failed_cases = []

print("\nAGENT ORCHESTRATOR VALIDATION")
print("=" * 65)


for test in test_cases:

    result = run_agent_orchestrator(test["report"])

    print(f"\nTest: {test['name']}")

    checks = {
        "overall_status": test["overall"],
        "triage_status": test["triage"],
        "log_analysis_status": test["log_analysis"]
    }

    actual_values = {
        "overall_status": result["overall_status"],
        "triage_status": result["agent_status"].get("triage"),
        "log_analysis_status": result["agent_status"].get("log_analysis")
    }

    case_failed = False

    for field, expected in checks.items():

        actual = actual_values[field]
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
