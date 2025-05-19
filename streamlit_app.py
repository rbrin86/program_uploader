import streamlit as st
from datetime import datetime
from mock_data import program_data  # this imports the above mock

st.set_page_config(page_title="Program Extractor", layout="centered")

st.title("🧪 Provisional Program Review")

st.text_input("Program Name", value=program_data["Program Name"])
st.date_input("Start Date", value=datetime.strptime(program_data["Start Date"], "%Y-%m-%d"))
st.date_input("End Date", value=datetime.strptime(program_data["End Date"], "%Y-%m-%d"))
st.text_input("Segment", value=program_data["Segment"])

st.subheader("Incentives")
for i, rule in enumerate(program_data["Incentives"]):
    st.text_input(f"Product {i+1}", value=rule["Product"])
    st.text_input(f"Type {i+1}", value=rule["Type"])
    st.text_input(f"Payout {i+1}", value=rule["Payout"])

if st.button("Submit for Verification"):
    st.success("✅ Program submitted for verification!")
