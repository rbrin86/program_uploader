import streamlit as st
import pandas as pd

def render_program_upload(navigate_to):
    st.title("Upload Unverified Program")

    uploaded_file = st.file_uploader("Upload a PDF Program", type=["pdf"])

    if uploaded_file:
        st.info("Simulating field extraction from PDF...")
        extracted_data = {
            "Program Name": "Spring Discount",
            "Start Date": "2025-03-01",
            "End Date": "2025-06-30",
            "Segment": "Seed",
            "Region": "Midwest",
            "Incentive Type": "Volume Rebate",
            "Payout Method": "ACH",
        }

        st.write("📄 Extracted Fields (editable):")
        for field, value in extracted_data.items():
            extracted_data[field] = st.text_input(field, value)

        if st.button("✅ Submit Program"):
            st.session_state.show_success = True
            navigate_to("we_earn")

    if st.button("⬅️ Back to Programs"):
        navigate_to("we_earn")
