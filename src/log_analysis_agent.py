
import re


def extract_exception(text):
    """Identify exception or error type."""

    patterns = [
        r"\b([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))\b",
        r"\b(ERROR|FATAL|CRITICAL)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return "Unknown"


def extract_error_message(text):
    """Extract the most relevant error message."""

    patterns = [
        r"(?:Caused by:\s*)?([A-Za-z_][A-Za-z0-9_.]*(?:Exception|Error):[^\r\n]*)",
        r"(?:ERROR|FATAL|CRITICAL)\s*[:\-]\s*([^\r\n]+)",
        r"(?:Error message|Message)\s*[:=]\s*([^\r\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return "No clear error message found"


def extract_failure_point(text):
    """Extract file, class, method and line number."""

    patterns = [
        r"at\s+([\w.$]+)\(([^():]+\.java):(\d+)\)",
        r"""File\s+['"]([^'"]+)['"],\s+line\s+(\d+),\s+in\s+(\w+)""",
        r"((?:[A-Za-z]:)?[\w./\\-]+\.(?:py|js|ts|cpp|c|cs)):(\d+)",
    ]

    for index, pattern in enumerate(patterns):
        match = re.search(pattern, text)

        if not match:
            continue

        if index == 0:
            method = match.group(1)
            filename = match.group(2)
            line = match.group(3)

            return {
                "file_name": filename,
                "class": method.rsplit(".", 1)[0]
                if "." in method else "Unknown",
                "method": method.rsplit(".", 1)[-1],
                "line_number": int(line)
            }

        if index == 1:
            return {
                "file_name": match.group(1),
                "class": "Unknown",
                "method": match.group(3),
                "line_number": int(match.group(2))
            }

        if index == 2:
            return {
                "file_name": match.group(1),
                "class": "Unknown",
                "method": "Unknown",
                "line_number": int(match.group(2))
            }

    return {
        "file_name": "Unknown",
        "class": "Unknown",
        "method": "Unknown",
        "line_number": None
    }


def extract_code_path(text):
    """Extract stack trace entries as a probable code path."""

    entries = []

    patterns = [
        r"at\s+([\w.$]+)\(([^():]+\.java):(\d+)\)",
        r"""File\s+["']([^"']+)["'],\s+line\s+(\d+),\s+in\s+(\w+)""",
    ]

    for line in text.splitlines():

        for index, pattern in enumerate(patterns):
            match = re.search(pattern, line)

            if not match:
                continue

            if index == 0:
                entries.append(
                    f"{match.group(1)} "
                    f"({match.group(2)}:{match.group(3)})"
                )
            else:
                entries.append(
                    f"{match.group(3)} "
                    f"({match.group(1)}:{match.group(2)})"
                )

            break

    return entries


def calculate_confidence(exception_type, failure_point, code_path):
    """Calculate heuristic analysis confidence."""

    score = 20

    if exception_type != "Unknown":
        score += 30

    if failure_point["file_name"] != "Unknown":
        score += 20

    if failure_point["line_number"] is not None:
        score += 15

    if code_path:
        score += 15

    return min(score, 95)


def run_log_analysis_agent(bug_report):
    """Main Log Analysis Agent."""

    log_fields = [
        "stack_trace",
        "stacktrace",
        "logs",
        "error_logs",
        "error_message",
    ]

    if isinstance(bug_report, dict):

        text = "\n".join(
            str(bug_report.get(field) or "")
            for field in log_fields
        )

    elif isinstance(bug_report, str):
        text = bug_report

    else:
        text = ""

    # Check whether actual log evidence was provided.
    if not text.strip():

        return {
            "agent": "Log Analysis Agent",
            "exception_type": "Unknown",
            "error_message": "No logs or stack trace provided",
            "failure_point": {
                "file_name": "Unknown",
                "class": "Unknown",
                "method": "Unknown",
                "line_number": None
            },
            "code_path": [],
            "confidence_score": 0,
            "status": "Incomplete"
        }

    exception_type = extract_exception(text)
    error_message = extract_error_message(text)
    failure_point = extract_failure_point(text)
    code_path = extract_code_path(text)

    confidence = calculate_confidence(
        exception_type,
        failure_point,
        code_path
    )

    return {
        "agent": "Log Analysis Agent",
        "exception_type": exception_type,
        "error_message": error_message,
        "failure_point": failure_point,
        "code_path": code_path,
        "confidence_score": confidence,
        "status": "Completed"
    }


# Standalone test
if __name__ == "__main__":

    sample_logs = """
    java.lang.NullPointerException: User object is null
        at com.example.LoginService.authenticate(LoginService.java:45)
        at com.example.LoginController.login(LoginController.java:22)
        at com.example.Application.main(Application.java:10)
    """

    result = run_log_analysis_agent(sample_logs)

    print("\nLOG ANALYSIS AGENT RESULT")
    print("=" * 55)

    for key, value in result.items():
        print(f"{key}: {value}")
