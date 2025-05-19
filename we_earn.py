import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("💰 We Earn – Programs Overview")

    # Sample data
    data = pd.DataFrame([
        {
            "Program Name": "Early Order Bonus 2025",
            "Program Owner": "BASF",
            "Segment": "Ag Chem",
            "Program Year": "2025",
            "Originator": "Supplier provided",
            "Earnings $": 15000,
            "Earnings %": 12.5
        },
        {
            "Program Name": "Spring Push",
            "Program Owner": "Bayer",
            "Segment": "Fertilizer",
            "Program Year": "2025",
            "Originator": "Created as Unverified by My Org",
            "Earnings $": 8700,
            "Earnings %": 9.2
        },
        {
            "Program Name": "Growth Incentive Q1",
            "Program Owner": "BASF",
            "Segment": "Seed",
            "Program Year": "2024",
            "Originator": "Supplier provided",
            "Earnings $": 22100,
            "Earnings %": 14.0
        }
    ])

    # 🔍 Filters
    st.sidebar.header("🔎 Filter Programs")
    selected_year = st.sidebar.selectbox("Program Year", ["All"] + sorted(data["Program Year"].unique()), index=0)
    selected_owner = st.sidebar.selectbox("Program Owner", ["All"] + sorted(data["Program Owner"].unique()), index=0)
    selected_segment = st.sidebar.selectbox("Segment", ["All"] + sorted(data["Segment"].unique()), index=0)
    selected_originator = st.sidebar.selectbox("Program Originator", ["All"] + sorted(data["Originator"].unique()), index=0)

    # Apply filters
    filtered = data.copy()
    if selected_year != "All":
        filtered = filtered[filtered["Program Year"] == selected_year]
    if selected_owner != "All":
        filtered = filtered[filtered["Program Owner"] == selected_owner]
    if selected_segment != "All":
        filtered = filtered[filtered["Segment"] == selected_segment]
    if selected_originator != "All":
        filtered = filtered[filtered["Originator"] == selected_originator]

    # 💵 Format earnings
    filtered["Earnings $"] = filtered["Earnings $"].apply(lambda x: f"${x:,.2f}")
    filtered["Earnings %"] = filtered["Earnings %"].apply(lambda x: f"{x:.1f}%")

    # 🧾 Display table
    st.dataframe(
        filtered[[
            "Program Name", "Program Owner", "Segment", "Program Year",
            "Originator", "Earnings $", "Earnings %"
        ]],
        use_container_width=True
    )

    st.markdown("---")
    if st.button("➕ Create Program"):
        navigate_to("program_upload")
