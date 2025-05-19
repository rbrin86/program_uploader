import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("💰 We Earn")

    # Hardcoded table (simulate actual program data)
    data = {
        "Program Name": ["Q1 Growth Bonus", "Seed Loyalty", "Premium Chem"],
        "Program Owner": ["AgroCorp", "SeedCo", "AgroCorp"],
        "Segment": ["Fertilizer", "Seed", "Ag Chem"],
        "Earnings $": [4500, 6200, 3100],
        "Earnings %": [0.12, 0.18, 0.09]
    }
    df = pd.DataFrame(data)

    # Filters and search placeholder
    st.text_input("🔍 Search Program Name", key="search")
    st.selectbox("Filter by Segment", options=["All", "Fertilizer", "Seed", "Ag Chem"], key="segment_filter")

    st.dataframe(df)

    # Upload Program CTA
    if st.button("📤 Create Program"):
        navigate_to("program_upload")
