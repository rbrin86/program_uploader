import streamlit as st
import pdfplumber
import re
from datetime import datetime

st.set_page_config(page_title="Program Extractor", layout="centered")

st.title("📄 Rebate Program Extractor (Simulated)")

uploaded_file = st.file_uploader("Upload a rebate program PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    st.subheader("Extracted Text")
    st.text_area("PDF Text", text, height=300)

    # Simulate field extraction
    st.subheader("Program Fields")

    def find_date(pattern, fallback):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return datetime.strptime(match.group(1), "%B %d, %Y").date()
            except:
                return fallback
        return fallback

    def find_field(pattern, fallback):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else fallback

    program_name = find_field(r"Program Name[:\-]\s*(.*)", "")
    start_date = find_date(r"Start Date[:\-]\s*([A-Za-z]+ \d{1,2}, \d{4})", None)
    end_date = find_date(r"End Date[:\-]\s*([A-Za-z]+ \d{1,2}, \d{4})", None)
    segment = find_field(r"Segment[:\-]\s*(.*)", "")
    incentive_type = find_field(r"Incentive Type[:\-]\s*(.*)", "")
    payout = find_field(r"Payout[:\-]\s*(.*)", "")

    # Form for manual review
    program_name = st.text_input("Program Name", value=program_name)
    start_date = st.date_input("Start Date", value=start_date) if start_date else st.date_input("Start Date")
    end_date = st.date_input("End Date", value=end_date) if end_date else st.date_input("End Date")
    segment = st.text_input("Segment", value=segment)
    incentive_type = st.text_input("Incentive Type", value=incentive_type)
    payout = st.text_input("Payout", value=payout)

    st.subheader("Review Status")
    missing_fields = []
    if not program_name: missing_fields.append("Program Name")
    if not start_date: missing_fields.append("Start Date")
    if not end_date: missing_fields.append("End Date")
    if not incentive_type: missing_fields.append("Incentive Type")
    if not payout: missing_fields.append("Payout")

    if missing_fields:
        st.warning(f"⚠️ Missing or unclear: {', '.join(missing_fields)}")
    else:
        st.success("✅ All fields look complete!")

    if st.button("Submit for Verification"):
        st.success("🎉 Program submitted for verification queue!")
