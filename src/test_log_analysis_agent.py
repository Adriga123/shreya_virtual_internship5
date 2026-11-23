
from log_analysis_agent import run_log_analysis_agent


# --------------------------------------------------
# LOG ANALYSIS VALIDATION DATASET
# --------------------------------------------------

test_cases = [

    {
        "name": "Java NullPointerException",
        "report": {
            "logs": """
            java.lang.NullPointerException: User object is null
            at com.example.LoginService.authenticate(LoginService.java:45)
            at com.example.LoginController.login(LoginController.java:22)
            """
        },
        "exception": "NullPointerException",
        "file": "LoginService.java",
        "line": 45,
        "status": "Completed"
    },

    {
        "name": "Java ArrayIndexOutOfBoundsException",
        "report": {
            "logs": """
            java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds
            at com.example.ArrayService.getValue(ArrayService.java:72)
            """
        },
        "exception": "ArrayIndexOutOfBoundsException",
        "file": "ArrayService.java",
        "line": 72,
        "status": "Completed"
    },

    {
        "name": "Python ValueError",
        "report": {
            "logs": """
            Traceback (most recent call last):
              File "app.py", line 28, in process_data
                int("hello")
            ValueError: invalid literal for int()
            """
        },
        "exception": "ValueError",
        "file": "app.py",
        "line": 28,
        "status": "Completed"
    },

    {
        "name": "JavaScript TypeError",
        "report": {
            "logs": """
            TypeError: Cannot read properties of undefined
                at loginUser (C:/project/login.js:35:10)
            """
        },
        "exception": "TypeError",
        "file": "C:/project/login.js",
        "line": 35,
        "status": "Completed"
    },

    {
        "name": "Logs without stack trace",
        "report": {
            "logs": """
            ERROR: Database connection failed
            FATAL: Service unavailable
            """
        },
        "exception": "ERROR",
        "file": "Unknown",
        "line": None,
        "status": "Completed"
    },

    {
        "name": "Logs without bug description",
        "report": {
            "logs": """
            ERROR: Cache service unavailable
            """
        },
        "exception": "ERROR",
        "file": "Unknown",
        "line": None,
        "status": "Completed"
    },

    {
        "name": "Messy Python logs",
        "report": {
            "logs": """
            2026-11-23 10:30:15 INFO Application started
            2026-11-23 10:30:18 WARNING Invalid input received
            2026-11-23 10:30:20 ERROR ValueError: Invalid integer value
            Traceback (most recent call last):
              File "app.py", line 28, in process_data
                int("hello")
            ValueError: invalid literal for int()
            """
        },
        "exception": "ValueError",
        "file": "app.py",
        "line": 28,
        "status": "Completed"
    },

    {
        "name": "Empty bug report",
        "report": {},
        "exception": "Unknown",
        "file": "Unknown",
        "line": None,
        "status": "Incomplete"
    }
]


# --------------------------------------------------
# RUN VALIDATION
# --------------------------------------------------

total_checks = 0
passed_checks = 0
failed_cases = []

print("\nLOG ANALYSIS AGENT VALIDATION")
print("=" * 65)


for test in test_cases:

    result = run_log_analysis_agent(test["report"])

    print(f"\nTest: {test['name']}")

    checks = {
        "exception_type": test["exception"],
        "file_name": test["file"],
        "line_number": test["line"],
        "status": test["status"]
    }

    actual_values = {
        "exception_type": result["exception_type"],
        "file_name": result["failure_point"]["file_name"],
        "line_number": result["failure_point"]["line_number"],
        "status": result["status"]
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

    print("Code path entries:", len(result["code_path"]))
    print("Confidence:", result["confidence_score"])


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
