import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from src.knowledge_base import load_defects
from src.retrieval import find_similar
from src.storage import initialize_db, save_report, list_reports
from src.agents import run_pipeline

st.set_page_config(page_title="Intelligent Bug Diagnosis", page_icon="🐞", layout="wide")
initialize_db()
st.title("🐞 Intelligent Bug Diagnosis Platform")
st.caption("Milestone 1 working prototype — local retrieval and a five-stage rule-based workflow.")

with st.form("bug_form"):
    st.subheader("Submit a bug report")
    title = st.text_input("Bug title *")
    description = st.text_area("Bug description *", height=130)
    stack_trace = st.text_area("Stack trace (optional)", height=100)
    error_logs = st.text_area("Error logs (optional)", height=100)
    upload = st.file_uploader(
        "Attach .txt, .log, .md, or .pdf file (optional)",
        type=["txt", "log", "md", "pdf"]
    )
    submit = st.form_submit_button("Submit and diagnose", type="primary")

if submit:
    if not title.strip() or not description.strip():
        st.error("Please enter both a title and a description.")
    else:
        attachment_text, attachment_name = "", ""
        if upload is not None:
            attachment_name = upload.name
            raw = upload.getvalue()
            if upload.name.lower().endswith(".pdf"):
                try:
                    import fitz
                    pdf = fitz.open(stream=raw, filetype="pdf")
                    attachment_text = "\n".join(page.get_text() for page in pdf)
                except Exception as exc:
                    st.error(f"PDF extraction failed: {exc}")
            else:
                attachment_text = raw.decode("utf-8", errors="replace")

        merged_logs = "\n".join(x for x in (error_logs.strip(), attachment_text.strip()) if x)
        report = {
            "title": title.strip(),
            "description": description.strip(),
            "stack_trace": stack_trace.strip(),
            "error_logs": merged_logs
        }
        bug_id = save_report(
            report["title"], report["description"], report["stack_trace"],
            report["error_logs"], attachment_name
        )
        matches = find_similar(" ".join(report.values()), load_defects())
        diagnosis = run_pipeline(report, matches)
        st.session_state["diagnosis"] = (bug_id, diagnosis)
        st.success(f"Report saved. Bug ID: {bug_id}")

if "diagnosis" in st.session_state:
    bug_id, result = st.session_state["diagnosis"]
    st.divider()
    st.subheader("Diagnosis results")
    st.caption(f"Bug ID: {bug_id}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Triage")
        st.write(f"**Category:** {result['triage']['category']}")
        st.write(f"**Priority:** {result['triage']['priority']}")
        st.caption(result["triage"]["note"])
        st.markdown("### Log analysis")
        st.write(result["log_analysis"]["detected_clues"] or "No recognizable error signature found.")
        st.markdown("### Root-cause hypotheses")
        for item in result["root_cause"]["hypotheses"]:
            st.write("• " + item)
    with col2:
        st.markdown("### Similar historical defects")
        if result["similar_defects"]:
            for item in result["similar_defects"]:
                st.write(f"**{item['title']}** — {item['project']} — similarity {item['similarity']}")
                st.caption(item["resolution"])
        else:
            st.info("No similar sample records found.")
        st.markdown("### Recommended debugging actions")
        for item in result["remediation"]["recommended_actions"]:
            st.write("• " + item)
        st.caption(result["remediation"]["caution"])

st.divider()
st.subheader("Recent submissions")
history = list_reports()
if history:
    st.json(history)
else:
    st.info("No reports submitted yet.")
