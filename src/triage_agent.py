
import re


# --------------------------------------------------
# SEVERITY CLASSIFICATION RULES
# --------------------------------------------------

SEVERITY_RULES = {
    "Critical": [
        "data loss",
        "data corruption",
        "security breach",
        "remote code execution",
        "production outage",
        "system down",
        "service unavailable",
        "all users affected",
        "complete system failure",
    ],

    "High": [
        "application crash",
        "app crash",
        "crashes",
        "crashed",
        "cannot login",
        "authentication failure",
        "deadlock",
        "memory leak",
        "blocking issue",
        "major functionality",
        "payment failure",
    ],

    "Medium": [
        "timeout",
        "performance issue",
        "slow response",
        "loading slowly",
        "slowly",
        "high latency",
        "long response time",
        "incorrect result",
        "unexpected error",
        "intermittent failure",
        "not working",
        "does not work",
        "exception",
        "fails",
    ],

    "Low": [
        "typo",
        "cosmetic",
        "alignment issue",
        "minor ui",
        "spelling mistake",
        "tooltip",
        "documentation",
        "color issue",
        "formatting issue",
        "feature request",
        "please add",
        "enhancement",
        "new option",
        "optional feature",
    ],
}


# --------------------------------------------------
# COMPONENT IDENTIFICATION RULES
# --------------------------------------------------

COMPONENT_RULES = {

    "Authentication": [
        "login",
        "logout",
        "password",
        "authentication",
        "authorization",
        "session",
        "token",
    ],

    "Database": [
        "database",
        "sql",
        "query",
        "mysql",
        "postgresql",
        "connection pool",
        "transaction",
    ],

    "Network": [
        "network",
        "network connection",
        "connection refused",
        "connection timeout",
        "socket",
        "dns",
        "network request",
        "internet connection",
        "connection failed",
    ],

    "Performance": [
        "performance",
        "slow",
        "slowly",
        "loading time",
        "page load",
        "page loading",
        "response time",
        "high latency",
        "latency",
        "takes more than",
        "takes too long",
        "long time to load",
        "takes seconds",
        "takes minutes",
        "loading delay",
    ],

    "User Interface": [
        "user interface",
        "ui",
        "frontend",
        "visual appearance",
        "interface layout",
        "dropdown",
        "alignment",
        "menu",
        "toolbar",
        "window layout",
    ],

    "API": [
        "api",
        "endpoint",
        "rest api",
        "json",
        "http status",
    ],

    "Search": [
        "search",
        "search function",
        "search results",
        "search query",
        "search bar",
        "keyword search",
        "filter results",
    ],

    "File Handling": [
        "file",
        "files",
        "file handling",
        "save file",
        "save as",
        "file type",
        "file extension",
        "download",
        "download window",
        "upload",
        "pdf",
        "document",
        "directory",
        "filesystem",
        "uri loader",
        "uriloader",
        "line breaks",
    ],

    "Logging": [
        "logging",
        "logger",
        "log file",
        "log message",
    ],

    "Payment": [
        "payment",
        "transaction",
        "billing",
        "checkout",
        "refund",
        "invoice",
    ],

    "Memory Management": [
        "memory",
        "heap",
        "out of memory",
        "allocation",
        "garbage collection",
    ],

    "Build and Deployment": [
        "build",
        "deployment",
        "installation",
        "compiler",
        "dependency",
        "package",
    ],
}


# --------------------------------------------------
# KEYWORD MATCHING
# --------------------------------------------------

def keyword_matches(text, keywords):
    """Match complete words and phrases."""

    matched = []

    for keyword in keywords:

        pattern = (
            r"(?<![a-zA-Z0-9_])"
            + re.escape(keyword)
            + r"(?![a-zA-Z0-9_])"
        )

        if re.search(pattern, text, flags=re.IGNORECASE):
            matched.append(keyword)

    return matched


# --------------------------------------------------
# REPORT TEXT EXTRACTION
# --------------------------------------------------

def get_report_text(bug_report):
    """Combine available bug report fields into searchable text."""

    if isinstance(bug_report, str):
        return bug_report.lower()

    if not isinstance(bug_report, dict):
        return ""

    fields = [
        "title",
        "description",
        "stack_trace",
        "stacktrace",
        "logs",
        "error_logs",
        "error_message",
        "content",
    ]

    text_parts = []

    for field in fields:

        value = bug_report.get(field, "")

        if value:
            text_parts.append(str(value))

    return " ".join(text_parts).lower()


# --------------------------------------------------
# SEVERITY CLASSIFICATION
# --------------------------------------------------

def find_severity(text):
    """Identify severity using matching evidence."""

    for severity in ["Critical", "High", "Medium", "Low"]:

        matched_keywords = keyword_matches(
            text,
            SEVERITY_RULES[severity]
        )

        if matched_keywords:
            return severity, matched_keywords

    return "Medium", []


# --------------------------------------------------
# COMPONENT IDENTIFICATION
# --------------------------------------------------

def find_component(text):
    """Identify the most likely affected component."""

    component_scores = {}

    for component, keywords in COMPONENT_RULES.items():

        matches = keyword_matches(text, keywords)

        if matches:
            component_scores[component] = matches

    if not component_scores:
        return "Unknown / Unclassified", []

    best_component = max(
        component_scores,
        key=lambda component: len(component_scores[component])
    )

    return best_component, component_scores[best_component]


# --------------------------------------------------
# PRIORITY ASSIGNMENT
# --------------------------------------------------

def assign_priority(severity, text):
    """Assign priority based on impact and urgency."""

    priority_map = {
        "Critical": "P1",
        "High": "P2",
        "Medium": "P3",
        "Low": "P4",
    }

    priority = priority_map[severity]

    urgent_keywords = [
        "urgent",
        "immediately",
        "production",
        "release blocker",
        "critical deadline",
    ]

    urgent_matches = keyword_matches(text, urgent_keywords)

    if urgent_matches:

        priority_number = int(priority[1])

        if priority_number > 1:
            priority = f"P{priority_number - 1}"

    return priority


# --------------------------------------------------
# CONFIDENCE CALCULATION
# --------------------------------------------------

def calculate_confidence(
    severity_matches,
    component_matches,
    bug_report
):
    """
    Calculate a heuristic confidence score.
    This is not a machine-learning probability.
    """

    score = 40

    if severity_matches:
        score += 20

    if component_matches:
        score += 20

    if isinstance(bug_report, dict):

        if bug_report.get("stack_trace") or bug_report.get("stacktrace"):
            score += 10

        if bug_report.get("logs") or bug_report.get("error_logs"):
            score += 10

    return min(score, 95)


# --------------------------------------------------
# MAIN TRIAGE AGENT
# --------------------------------------------------

def run_triage_agent(bug_report):
    """Classify severity, priority, and affected component."""

    text = get_report_text(bug_report)

    if not text.strip():

        return {
            "agent": "Triage Agent",
            "severity": "Unknown",
            "priority": "Unassigned",
            "affected_component": "Unknown / Unclassified",
            "confidence_score": 0,
            "reasoning": "Insufficient bug report information.",
            "matched_severity_signals": [],
            "matched_component_signals": [],
            "status": "Incomplete",
        }

    severity, severity_matches = find_severity(text)

    component, component_matches = find_component(text)

    priority = assign_priority(severity, text)

    confidence = calculate_confidence(
        severity_matches,
        component_matches,
        bug_report
    )

    reasoning = (
        f"Severity classified as {severity} based on "
        f"{', '.join(severity_matches) if severity_matches else 'limited impact evidence'}. "
        f"Priority assigned as {priority}. "
        f"Affected component identified as {component}."
    )

    return {
        "agent": "Triage Agent",
        "severity": severity,
        "priority": priority,
        "affected_component": component,
        "confidence_score": confidence,
        "reasoning": reasoning,
        "matched_severity_signals": severity_matches,
        "matched_component_signals": component_matches,
        "status": "Completed",
    }


# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample_bug = {
        "title": "Application crashes during login",

        "description": (
            "Users cannot login because the authentication "
            "service crashes unexpectedly."
        ),

        "stack_trace": (
            "NullPointerException at LoginService.authenticate()"
        ),

        "logs": (
            "Authentication failure during login request."
        )
    }

    result = run_triage_agent(sample_bug)

    print("\nTRIAGE AGENT RESULT")
    print("=" * 50)

    for key, value in result.items():
        print(f"{key}: {value}")
