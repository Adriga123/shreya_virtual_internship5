
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from src.knowledge_base import load_defects
from src.retrieval import find_similar
from src.storage import initialize_db, save_report, list_reports
from src.agents import run_pipeline


# Page configuration
st.set_page_config(
    page_title="Intelligent Bug Diagnosis",
    page_icon="🐞",
    layout="wide"
)

initialize_db()

st.title("🐞 Intelligent Bug Diagnosis Platform")
st.caption(
    "Milestone 1 working prototype — local retrieval and a "
    "five-stage rule-based workflow."
)


# Bug submission form
with st.form("bug_form"):

    st.subheader("Submit a bug report")

    title = st.text_input("Bug title *")

    description = st.text_area(
        "Bug description *",
        height=130
    )

    stack_trace = st.text_area(
        "Stack trace (optional)",
        height=100
    )

    error_logs = st.text_area(
        "Error logs (optional)",
        height=100
    )

    upload = st.file_uploader(
        "Attach .txt, .log, .md, or .pdf file (optional)",
        type=["txt", "log", "md", "pdf"]
    )

    submit = st.form_submit_button(
        "Submit and diagnose",
        type="primary"
    )


# Process submitted bug report
if submit:

    if not title.strip() or not description.strip():

        st.error("Please enter both a title and a description.")

    else:

        attachment_text = ""
        attachment_name = ""

        if upload is not None:

            attachment_name = upload.name
            raw = upload.getvalue()

            if upload.name.lower().endswith(".pdf"):

                try:
                    import fitz

                    pdf = fitz.open(
                        stream=raw,
                        filetype="pdf"
                    )

                    attachment_text = "\n".join(
                        page.get_text() for page in pdf
                    )

                except Exception as exc:

                    st.error(f"PDF extraction failed: {exc}")

            else:

                attachment_text = raw.decode(
                    "utf-8",
                    errors="replace"
                )

        merged_logs = "\n".join(
            x for x in (
                error_logs.strip(),
                attachment_text.strip()
            ) if x
        )

        report = {
            "title": title.strip(),
            "description": description.strip(),
            "stack_trace": stack_trace.strip(),
            "error_logs": merged_logs
        }

        # Save bug report
        bug_id = save_report(
            report["title"],
            report["description"],
            report["stack_trace"],
            report["error_logs"],
            attachment_name
        )

        # Retrieve similar historical defects
        matches = find_similar(
            " ".join(report.values()),
            load_defects()
        )

        # Run five-stage diagnosis workflow
        diagnosis = run_pipeline(report, matches)

        st.session_state["diagnosis"] = (
            bug_id,
            diagnosis
        )

        st.success(f"Report saved. Bug ID: {bug_id}")


# Display diagnosis results
if "diagnosis" in st.session_state:

    bug_id, result = st.session_state["diagnosis"]

    st.divider()
    st.subheader("Diagnosis results")
    st.caption(f"Bug ID: {bug_id}")

    col1, col2 = st.columns(2)

    # Left column
    with col1:

        st.markdown("### Triage")

        st.text(
            f"Category: {result['triage']['category']}"
        )

        st.text(
            f"Priority: {result['triage']['priority']}"
        )

        st.caption(
            str(result["triage"]["note"])
        )

        st.markdown("### Log analysis")

        detected_clues = result["log_analysis"]["detected_clues"]

        if isinstance(detected_clues, list):

            st.text(
                "\n".join(str(item) for item in detected_clues)
                if detected_clues
                else "No recognizable error signature found."
            )

        else:

            st.text(
                str(detected_clues)
                if detected_clues
                else "No recognizable error signature found."
            )

        st.markdown("### Root-cause hypotheses")

        hypotheses = result["root_cause"]["hypotheses"]

        if hypotheses:

            for item in hypotheses:
                st.text("• " + str(item))

        else:

            st.text("No root-cause hypotheses available.")

    # Right column
    with col2:

        st.markdown("### Similar historical defects")

        similar_defects = result["similar_defects"]

        if similar_defects:

            for item in similar_defects:

                score = item.get("similarity", 0) * 100

                project = item.get(
                    "project",
                    item.get("source", "Unknown")
                )

                st.text(
                    f"{item.get('title', 'Untitled')} — "
                    f"{project} — Similarity: {score:.2f}%"
                )

                st.caption(
                    str(item.get("resolution", "No resolution available"))
                )

        else:

            st.info("No similar sample records found.")

        st.markdown("### Recommended debugging actions")

        actions = result["remediation"]["recommended_actions"]

        if actions:

            for item in actions:
                st.text("• " + str(item))

        else:

            st.text("No recommended actions available.")

        st.caption(
            str(result["remediation"]["caution"])
        )


# Recent submissions
st.divider()
st.subheader("Recent submissions")

history = list_reports()

if history:

    st.text(
        json.dumps(
            history,
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )

else:

    st.info("No reports submitted yet.")
