import streamlit as st
import pandas as pd
from src.pipeline import process_email
from src.database import init_db, seed_demo_data, get_record_context

st.set_page_config(page_title="Email-to-Action Assistant", page_icon="✉️", layout="wide")
init_db()
seed_demo_data()

st.title("✉️ Email-to-Action Assistant")
st.caption("Turn trade emails into structured, reviewable actions — with human approval before execution.")

with st.sidebar:
    st.subheader("Configuration")
    use_llm = st.toggle("Use OpenAI LLM (optional)", value=False)
    st.caption("When disabled, the app uses a transparent rule-based fallback. Add OPENAI_API_KEY to .env to enable LLM assistance.")
    st.divider()
    st.markdown("**Workflow**")
    st.markdown("1. Classify the email\n2. Prioritise the request\n3. Retrieve shipment/invoice context\n4. Draft a response\n5. Approve manually")

sample = st.selectbox("Try a sample trade email", [
    "Choose a sample...",
    "Shipment status request",
    "Invoice discrepancy",
    "Urgent delivery delay"
])
samples = {
    "Shipment status request": "Hello team, could you share the latest status for shipment SHP-1002? Our customer is asking for an updated ETA. Regards, ABC Exports",
    "Invoice discrepancy": "We noticed a mismatch in invoice INV-2001. The billed quantity appears different from the purchase order. Please investigate and advise. Regards, XYZ Imports",
    "Urgent delivery delay": "URGENT: Shipment SHP-1003 is delayed and may miss the delivery window. Please confirm the revised ETA and next steps immediately. Regards, Global Trade"
}
default_email = samples.get(sample, "")
email_text = st.text_area("Paste the incoming trade email", value=default_email, height=190, placeholder="Paste an exporter/importer email here...")

if st.button("Process email", type="primary", disabled=not email_text.strip()):
    result = process_email(email_text, use_llm=use_llm)
    st.session_state["result"] = result
    st.session_state["email_text"] = email_text

if "result" in st.session_state:
    result = st.session_state["result"]
    st.divider()
    st.subheader("1 · Classification and prioritisation")
    c1, c2, c3 = st.columns(3)
    c1.metric("Category", result["category"])
    c2.metric("Priority", result["priority"])
    c3.metric("Confidence", f'{result["confidence"]:.0%}')
    st.write("**Reason:**", result["reason"])

    st.subheader("2 · Extracted identifiers")
    ids = result["identifiers"]
    st.write({"shipment_id": ids.get("shipment_id"), "invoice_id": ids.get("invoice_id")})
    context = get_record_context(ids)
    if context:
        st.subheader("3 · Retrieved SQL context")
        st.json(context)
    else:
        st.info("No matching shipment or invoice record was found in the demo database.")

    st.subheader("4 · Draft response")
    draft = st.text_area("Review and edit before approval", value=result["draft"], height=180, key="draft_response")
    st.subheader("5 · Human-in-the-loop approval")
    approver = st.text_input("Approver name", placeholder="Enter reviewer name")
    if st.button("Approve draft", type="primary", disabled=not approver.strip()):
        st.session_state["approved"] = {
            "approver": approver,
            "draft": draft,
            "category": result["category"],
            "priority": result["priority"]
        }
        st.success("Draft approved and recorded in this session. No email has been sent.")
    if "approved" in st.session_state:
        st.success(f'Approved by {st.session_state["approved"]["approver"]}. Copy the reviewed draft into your email client to send.')

st.divider()
st.caption("Demo application: approval is recorded locally in the current Streamlit session; outbound email sending is intentionally not enabled.")
