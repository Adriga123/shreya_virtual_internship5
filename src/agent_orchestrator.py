
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.triage_agent import run_triage_agent
from src.log_analysis_agent import run_log_analysis_agent


def run_agent_orchestrator(bug_report):
    """Coordinate the Triage and Log Analysis Agents."""

    result = {
        "bug_report": bug_report,
        "triage": None,
        "log_analysis": None,
        "agent_status": {},
        "overall_status": "Completed"
    }

    # Run Triage Agent
    try:
        result["triage"] = run_triage_agent(bug_report)

        result["agent_status"]["triage"] = (
            result["triage"].get("status", "Completed")
        )

    except Exception as exc:
        result["agent_status"]["triage"] = "Failed"
        result["agent_status"]["triage_error"] = str(exc)

    # Run Log Analysis Agent
    try:
        result["log_analysis"] = run_log_analysis_agent(bug_report)

        result["agent_status"]["log_analysis"] = (
            result["log_analysis"].get("status", "Completed")
        )

    except Exception as exc:
        result["agent_status"]["log_analysis"] = "Failed"
        result["agent_status"]["log_analysis_error"] = str(exc)

    statuses = [
        result["agent_status"].get("triage"),
        result["agent_status"].get("log_analysis")
    ]

    if all(status == "Failed" for status in statuses):
        result["overall_status"] = "Failed"

    elif any(status != "Completed" for status in statuses):
        result["overall_status"] = "Partial"

    return result


if __name__ == "__main__":

    sample_report = {
        "title": "Application crashes during login",
        "description": "Users cannot login because authentication fails.",
        "stack_trace": """
        java.lang.NullPointerException: User object is null
        at com.example.LoginService.authenticate(LoginService.java:45)
        at com.example.LoginController.login(LoginController.java:22)
        """,
        "error_logs": "Authentication failure during login request."
    }

    output = run_agent_orchestrator(sample_report)

    print("\nAGENT ORCHESTRATOR RESULT")
    print("=" * 55)

    print("Overall status:", output["overall_status"])

    print("\nTriage Agent:")
    print(output["triage"])

    print("\nLog Analysis Agent:")
    print(output["log_analysis"])

    print("\nAgent statuses:")
    print(output["agent_status"])
