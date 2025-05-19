import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("We Earn Programs")

    if st.session_state.get("show_success"):
        st.success("✅ Program submitted as Unverified.")
        st.session_state.show_success = False

    # Sample table data
    data = [
        {"Program Name": "Growth Boost", "Program Owner": "Bayer", "Segment": "Ag Chem", "Earnings $": 12000, "Earnings %": 12, "Originator": "Published by Supplier"},
        {"Program Name": "Seed Surge", "Program Owner": "Syngenta", "Segment": "Seed", "Earnings $": 8000, "Earnings %": 8, "Originator": "Created as unverified by my organization"},
    ]
    df = pd.DataFrame(data)

    # Filters
    st.selectbox("Program Year", ["2024", "2025"])
    st.selectbox("Segment", ["All", "Ag Chem", "Seed", "Fertilizer"])
    st.selectbox("Program Originator", ["All", "Published by Supplier", "Created as unverified by my organization"])

    st.dataframe(df)

    if st.button("➕ Create Program"):
        navigate_to("program_upload")
