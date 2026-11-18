import re

def triage_agent(report):
    text = " ".join(str(v) for v in report.values()).lower()
    if any(w in text for w in ("crash", "fatal", "data loss", "security")):
        priority = "High"
    elif any(w in text for w in ("slow", "timeout", "freeze", "failed", "exception")):
        priority = "Medium"
    else:
        priority = "Low"
    if any(w in text for w in ("database", "sql", "query")):
        category = "Database"
    elif any(w in text for w in ("network", "http", "connection", "timeout")):
        category = "Network"
    elif any(w in text for w in ("ui", "screen", "button", "render", "editor")):
        category = "User Interface"
    else:
        category = "Application / General"
    return {"category": category, "priority": priority,
            "note": "Provisional keyword-based classification; confirm with a developer."}

def log_analysis_agent(report):
    text = " ".join(str(v) for v in report.values())
    patterns = [
        r"\b[A-Za-z_][A-Za-z0-9_]*Error\b",
        r"\b[A-Za-z_][A-Za-z0-9_]*Exception\b",
        r"\bHTTP\s?\d{3}\b",
        r"\btimeout\b",
        r"\bconnection refused\b",
        r"\bout of memory\b",
    ]
    clues = []
    for pattern in patterns:
        clues.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return {"detected_clues": list(dict.fromkeys(clues))[:12],
            "note": "Extracted text clues only; no clue does not imply the logs are healthy."}

def duplicate_detection_agent(matches):
    return [{
        "title": m.get("title", "Untitled"),
        "project": m.get("project", "Sample"),
        "component": m.get("component", "Unknown"),
        "similarity": round(m.get("similarity", 0.0), 3),
        "resolution": m.get("resolution", "")
    } for m in matches]

def root_cause_agent(report, matches, log_result):
    hypotheses = []
    if log_result["detected_clues"]:
        hypotheses.append("Inspect the extracted error signature and the first relevant application stack frame.")
    if matches:
        hypotheses.append("Compare the affected component and reproduction conditions with the retrieved historical examples.")
    if not hypotheses:
        hypotheses.append("Evidence is insufficient for a specific cause; collect reproduction steps, environment/version details, and a complete stack trace.")
    return {"hypotheses": hypotheses, "evidence_count": len(matches)}

def remediation_agent(report, matches):
    actions = [
        "Reproduce the issue using the same input, software version, and environment.",
        "Inspect the first application-owned stack-trace frame and nearby code.",
        "Create a focused regression test that fails before the fix and passes after it."
    ]
    if matches:
        actions.append("Review the retrieved examples and verify whether their resolution applies to this report.")
    else:
        actions.append("Collect relevant historical issues and additional logs before selecting a fix.")
    return {"recommended_actions": actions,
            "caution": "These are debugging suggestions, not a verified code patch."}

def run_pipeline(report, matches):
    triage = triage_agent(report)
    logs = log_analysis_agent(report)
    duplicates = duplicate_detection_agent(matches)
    root_cause = root_cause_agent(report, matches, logs)
    remediation = remediation_agent(report, matches)
    return {
        "triage": triage,
        "log_analysis": logs,
        "similar_defects": duplicates,
        "root_cause": root_cause,
        "remediation": remediation
    }
