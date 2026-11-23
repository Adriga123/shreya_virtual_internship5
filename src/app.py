
import streamlit as st
import pandas as pd
import json
import fitz

from src.storage import (
    initialize_db,
    save_report,
    list_reports,
    get_report
)
from src.knowledge_base import load_defects
from src.retrieval import find_similar
from src.agents import run_pipeline
from src.agent_orchestrator import run_agent_orchestrator


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BugScope | Intelligent Bug Diagnosis",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

initialize_db()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main page */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #F7F9FC !important;
    color: #172033 !important;
}

/* Main page text */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label,
[data-testid="stMain"] span,
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMetricLabel"],
[data-testid="stMain"] [data-testid="stMetricValue"],
[data-testid="stMain"] [data-testid="stCaptionContainer"] {
    color: #172033 !important;
}

/* Input fields */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    background: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    border: 1.5px solid #334155 !important;
    border-radius: 8px !important;
}

/* Dropdowns */
[data-testid="stMain"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1.5px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stMain"] div[data-baseweb="select"] *,
div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
div[role="option"] * {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[role="listbox"],
div[role="option"] {
    background: #FFFFFF !important;
}

/* Sidebar */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #14213D !important;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    color: #172033 !important;
    border: 2px solid #334155 !important;
    padding: 18px !important;
    border-radius: 12px !important;
}

/* Containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #F1F5F9 !important;
    color: #172033 !important;
    border: 2px solid #334155 !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: #3157A4 !important;
    color: #FFFFFF !important;
    border: 1.5px solid #334155 !important;
    border-radius: 8px !important;
}

.stButton > button *,
.stFormSubmitButton > button * {
    color: #FFFFFF !important;
}

/* --------------------------------------------------
   FILE UPLOADER - SPECIFIC STYLING
   -------------------------------------------------- */

/* Main uploader area */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] section {
    background: #FFFFFF !important;
    color: #172033 !important;
}

/* Drag and drop area */
[data-testid="stFileUploaderDropzone"] {
    background: #EAF0F8 !important;
    border: 2px dashed #3157A4 !important;
    border-radius: 12px !important;
}

/* Uploader text and instructions */
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* Browse files button */
[data-testid="stFileUploader"] button {
    background: #3157A4 !important;
    color: #FFFFFF !important;
    border: 1.5px solid #243F78 !important;
    border-radius: 7px !important;
}

/* Browse files button text */
[data-testid="stFileUploader"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Uploaded file information */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div {
    background: #F1F5F9 !important;
    color: #172033 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

/* Uploaded file name and details */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* Upload area hover effect */
[data-testid="stFileUploaderDropzone"]:hover {
    background: #DCE7F5 !important;
    border-color: #1D4ED8 !important;
}

/* Expanders */
[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background: #F1F5F9 !important;
    color: #172033 !important;
    border: 2px solid #334155 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] * {
    color: #172033 !important;
}

/* Code blocks and logs */
[data-testid="stCode"],
[data-testid="stCodeBlock"],
[data-testid="stCodeBlock"] pre,
[data-testid="stCode"] pre,
pre,
code {
    background: #F1F5F9 !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    border: 2px solid #334155 !important;
    border-radius: 8px !important;
}

pre span,
code span {
    color: #172033 !important;
}

/* ALL MESSAGE BOXES */
[data-testid="stAlert"] {
    background: #DCFCE7 !important;
    border: 2px solid #166534 !important;
    border-radius: 10px !important;
}

[data-testid="stAlert"] *,
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    color: #14532D !important;
    -webkit-text-fill-color: #14532D !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    color: #172033 !important;
    border: 2px solid #334155 !important;
    border-radius: 8px !important;
}

/* Dividers */
hr {
    border-color: #334155 !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def metric_card(label, value, help_text=None):
    st.metric(
        label=label,
        value=value,
        help=help_text
    )


def show_severity(severity):
    colors = {
        "Critical": "#B42318",
        "High": "#D97706",
        "Medium": "#2563EB",
        "Low": "#15803D"
    }

    color = colors.get(severity, "#596579")

    st.markdown(
        f"""
        <span style="
            background-color:{color};
            color:white;
            padding:6px 13px;
            border-radius:20px;
            font-weight:600;
            font-size:13px;">
            {severity or "Unknown"}
        </span>
        """,
        unsafe_allow_html=True
    )


def display_report_details(report):
    st.markdown("### Bug Details")

    st.write("**Title:**", report.get("title", "Not available"))
    st.write("**Description:**", report.get("description", "Not available"))

    if report.get("stack_trace"):
        with st.expander("View Stack Trace"):
            st.code(report["stack_trace"])

    if report.get("error_logs"):
        with st.expander("View Error Logs"):
            st.code(report["error_logs"])

    if report.get("attachment_name"):
        st.write("**Attachment:**", report["attachment_name"])


def display_diagnosis(diagnosis):

    if not diagnosis:
        st.warning("No diagnosis information is available for this report.")
        return

    orchestration = diagnosis.get("agent_orchestration", {})
    legacy = diagnosis.get("legacy_pipeline", {})

    triage = orchestration.get("triage") or {}
    log_analysis = orchestration.get("log_analysis") or {}

    st.markdown("### Triage Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Severity**")
        show_severity(triage.get("severity", "Unknown"))

    with col2:
        metric_card(
            "Priority",
            triage.get("priority", "Unknown")
        )

    with col3:
        metric_card(
            "Confidence",
            f'{triage.get("confidence_score", 0)}%'
        )

    if triage:
        st.write(
            "**Affected component:**",
            triage.get("affected_component", "Unknown")
        )

        st.write(
            "**Reasoning:**",
            triage.get("reasoning", "Not available")
        )

        with st.expander("View Triage Signals"):
            st.write(
                "Severity signals:",
                triage.get("matched_severity_signals", [])
            )
            st.write(
                "Component signals:",
                triage.get("matched_component_signals", [])
            )

    st.divider()

    st.markdown("### Log Analysis")

    if log_analysis:

        if log_analysis.get("status") == "Incomplete" or not (
            log_analysis.get("exception_type")
            or log_analysis.get("error_message")
            or log_analysis.get("code_path")
        ):
            st.info(
                "No stack trace or useful error-log evidence was provided. "
                "Log analysis is limited; this does not mean the application has no errors."
            )

        st.write(
            "**Exception type:**",
            log_analysis.get("exception_type") or "Not identified"
        )

        st.write(
            "**Error message:**",
            log_analysis.get("error_message") or "Not identified"
        )

        failure = log_analysis.get("failure_point") or {}

        st.write("**Failure point**")

        failure_col1, failure_col2 = st.columns(2)

        with failure_col1:
            st.write(
                "File:",
                failure.get("file_name") or "Not identified"
            )
            st.write(
                "Class:",
                failure.get("class") or "Not identified"
            )

        with failure_col2:
            st.write(
                "Method:",
                failure.get("method") or "Not identified"
            )
            st.write(
                "Line number:",
                failure.get("line_number") or "Not identified"
            )

        code_path = log_analysis.get("code_path", [])

        if code_path:
            with st.expander("View Code Path"):
                for index, frame in enumerate(code_path, start=1):
                    st.write(f"{index}. {frame}")
        else:
            st.info("No code path could be extracted.")

        st.write(
            "**Log analysis confidence:**",
            f'{log_analysis.get("confidence_score", 0)}%'
        )

    else:
        st.info("Log analysis was not completed for this report.")

    st.divider()

    st.markdown("### Similar Historical Defects")

    similar_defects = legacy.get("similar_defects", [])

    if similar_defects:

        for defect in similar_defects:
            with st.expander(
                defect.get("title", "Historical defect")
            ):
                st.write(
                    "**Project:**",
                    defect.get("project", "Unknown")
                )
                st.write(
                    "**Component:**",
                    defect.get("component", "Unknown")
                )
                st.write(
                    "**Similarity score:**",
                    defect.get("similarity", 0)
                )
                st.write(
                    "**Resolution:**",
                    defect.get("resolution", "Not available")
                )

    else:
        st.info("No similar historical defects were retrieved.")

    st.divider()

    st.markdown("### Root Cause Hypotheses")

    root_cause = legacy.get("root_cause", {})
    hypotheses = root_cause.get("hypotheses", [])

    if hypotheses:
        for hypothesis in hypotheses:
            st.write("•", hypothesis)
    else:
        st.info("No root cause hypotheses are available.")

    st.divider()

    st.markdown("### Recommended Debugging Actions")

    remediation = legacy.get("remediation", {})
    actions = remediation.get("recommended_actions", [])

    if actions:
        for index, action in enumerate(actions, start=1):
            st.write(f"**{index}.** {action}")

    if remediation.get("caution"):
        st.caption(remediation["caution"])

    st.caption(
        "The diagnosis is a prototype analysis. "
        "Suggestions should be reviewed by a developer."
    )


# --------------------------------------------------
# LOAD REPORTS
# --------------------------------------------------

reports = list_reports(limit=1000)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🐞 BugScope")
    st.caption("Intelligent Bug Diagnosis Platform")

    st.divider()

    selected_page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Submit a Bug",
            "Analysis Reports",
            "Bug History"
        ],
        label_visibility="visible"
    )

    st.divider()


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if selected_page == "Overview":

    st.title("Dashboard")
    st.write("Monitor bug reports and view diagnosis activity.")

    total_reports = len(reports)

    severity_counts = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for report in reports:
        severity = report.get("severity")

        if severity in severity_counts:
            severity_counts[severity] += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Bug Reports", total_reports)

    with col2:
        metric_card("Critical Issues", severity_counts["Critical"])

    with col3:
        metric_card("High Priority Issues", severity_counts["High"])

    with col4:
        diagnosed_count = sum(
            1 for report in reports
            if report.get("has_diagnosis")
        )
        metric_card("Analysis Reports", diagnosed_count)

    st.divider()

    st.markdown("### Recent Bug Reports")

    if reports:

        recent_data = []

        for report in reports[:5]:
            recent_data.append({
                "Title": report.get("title", ""),
                "Severity": report.get("severity") or "Unknown",
                "Component": report.get("affected_component") or "Unknown",
                "Priority": report.get("priority") or "Unknown",
                "Date": report.get("created_at", "")
            })

        st.dataframe(
            pd.DataFrame(recent_data),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No bug reports have been submitted yet.")

    st.caption("Dashboard data is based on locally saved reports.")


# --------------------------------------------------
# SUBMIT A BUG PAGE
# --------------------------------------------------

elif selected_page == "Submit a Bug":

    st.title("Submit a Bug")
    st.write(
        "Enter the bug details or upload a report "
        "to start the diagnosis process."
    )

    with st.form("bug_submission_form"):

        title = st.text_input(
            "Bug Title *",
            placeholder="Example: Application crashes during login"
        )

        description = st.text_area(
            "Bug Description *",
            placeholder="Describe the issue, steps to reproduce, and expected behaviour.",
            height=150
        )

        stack_trace = st.text_area(
            "Stack Trace",
            placeholder="Paste the stack trace here...",
            height=130
        )

        error_logs = st.text_area(
            "Application Logs",
            placeholder="Paste application logs here...",
            height=130
        )

        uploaded_file = st.file_uploader(
            "Upload Bug Report",
            type=["txt", "log", "md", "pdf"]
        )

        submitted = st.form_submit_button(
            "Analyse Bug",
            use_container_width=True
        )

    if submitted:

        if not title.strip() or not description.strip():
            st.error("Please enter both the bug title and description.")

        else:

            attachment_name = ""
            extracted_text = ""

            if uploaded_file is not None:

                attachment_name = uploaded_file.name
                file_bytes = uploaded_file.read()

                try:

                    if uploaded_file.name.lower().endswith(".pdf"):

                        pdf_document = fitz.open(
                            stream=file_bytes,
                            filetype="pdf"
                        )

                        extracted_text = "\n".join(
                            page.get_text()
                            for page in pdf_document
                        )

                        pdf_document.close()

                    else:
                        extracted_text = file_bytes.decode(
                            "utf-8",
                            errors="replace"
                        )

                except Exception as exc:
                    st.error(f"Could not read the uploaded file: {exc}")

            bug_report = {
                "title": title.strip(),
                "description": description.strip(),
                "stack_trace": stack_trace.strip(),
                "error_logs": "\n".join(
                    item for item in [error_logs, extracted_text]
                    if item.strip()
                ),
                "attachment_name": attachment_name
            }

            with st.spinner("Analysing bug report..."):

                try:

                    # Run M2 agents
                    orchestration = run_agent_orchestrator(
                        bug_report
                    )

                    # Retrieve historical defects
                    defects = load_defects()

                    matches = find_similar(
                        bug_report,
                        defects
                    )

                    # Run existing five-stage workflow
                    legacy_result = run_pipeline(
                        bug_report,
                        matches
                    )

                    complete_diagnosis = {
                        "agent_orchestration": orchestration,
                        "legacy_pipeline": legacy_result
                    }

                    bug_id = save_report(
                        title=title.strip(),
                        description=description.strip(),
                        stack_trace=stack_trace.strip(),
                        error_logs=bug_report["error_logs"],
                        attachment_name=attachment_name,
                        triage_result=orchestration.get("triage"),
                        diagnosis=complete_diagnosis
                    )

                    st.success("Bug report analysed and saved successfully!")

                    st.write("**Bug ID:**", bug_id)

                    st.divider()

                    st.markdown("## Diagnosis Results")

                    display_diagnosis(complete_diagnosis)

                    st.info(
                        "You can view this report later under "
                        "**Analysis Reports** or **Bug History**."
                    )

                    st.cache_data.clear()

                except Exception as exc:

                    st.error(
                        f"An error occurred during diagnosis: {exc}"
                    )


# --------------------------------------------------
# ANALYSIS REPORTS PAGE
# --------------------------------------------------

elif selected_page == "Analysis Reports":

    st.title("Analysis Reports")
    st.write("Select a saved report to view its diagnosis.")

    diagnosed_reports = [
        report for report in reports
        if report.get("has_diagnosis")
    ]

    if diagnosed_reports:

        report_options = {
            f'{report.get("title", "Untitled")} | '
            f'{report.get("bug_id", "")[:8]}': report.get("bug_id")
            for report in diagnosed_reports
        }

        selected_report_label = st.selectbox(
            "Choose a Bug Report",
            list(report_options.keys())
        )

        selected_bug_id = report_options[selected_report_label]

        selected_report = get_report(selected_bug_id)

        if selected_report:

            st.divider()

            display_report_details(selected_report)

            st.divider()

            diagnosis = selected_report.get("diagnosis")

            display_diagnosis(diagnosis)

    else:

        st.info(
            "No saved analysis reports are available yet. "
            "Submit a bug to generate an analysis report."
        )


# --------------------------------------------------
# BUG HISTORY PAGE
# --------------------------------------------------

elif selected_page == "Bug History":

    st.title("Bug History")
    st.write("Search and explore previously submitted bug reports.")

    if reports:

        search_text = st.text_input(
            "Search by bug title",
            placeholder="Enter a title or keyword..."
        )

        severity_options = [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low",
            "Unknown"
        ]

        selected_severity = st.selectbox(
            "Filter by Severity",
            severity_options
        )

        filtered_reports = []

        for report in reports:

            report_title = report.get("title", "").lower()
            severity = report.get("severity") or "Unknown"

            matches_search = (
                search_text.lower() in report_title
            )

            matches_severity = (
                selected_severity == "All"
                or severity == selected_severity
            )

            if matches_search and matches_severity:
                filtered_reports.append(report)

        st.write(
            f"**{len(filtered_reports)} report(s) found**"
        )

        history_data = []

        for report in filtered_reports:

            history_data.append({
                "Bug ID": report.get("bug_id", "")[:8],
                "Title": report.get("title", ""),
                "Severity": report.get("severity") or "Unknown",
                "Component": report.get("affected_component") or "Unknown",
                "Priority": report.get("priority") or "Unknown",
                "Created At": report.get("created_at", "")
            })

        if history_data:

            st.dataframe(
                pd.DataFrame(history_data),
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            history_options = {
                f'{report.get("title", "Untitled")} | '
                f'{report.get("bug_id", "")[:8]}': report.get("bug_id")
                for report in filtered_reports
            }

            selected_history_label = st.selectbox(
                "View Report Details",
                list(history_options.keys())
            )

            selected_history_id = history_options[
                selected_history_label
            ]

            history_report = get_report(selected_history_id)

            if history_report:

                display_report_details(history_report)

                st.write(
                    "**Severity:**",
                    history_report.get("severity") or "Unknown"
                )

                st.write(
                    "**Priority:**",
                    history_report.get("priority") or "Unknown"
                )

                if history_report.get("diagnosis"):

                    with st.expander("View Full Diagnosis"):
                        display_diagnosis(
                            history_report["diagnosis"]
                        )

        else:
            st.info("No reports match your search and filter.")

    else:
        st.info("No bug reports have been submitted yet.")
