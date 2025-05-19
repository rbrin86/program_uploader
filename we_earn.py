import streamlit as st
import pandas as pd

def render_we_earn():
    st.title("We Earn: Program Summary")

    # Example data — you can replace this with a Snowflake or other DB pull
    data = pd.DataFrame([
        {"Program Name": "Growth Rebate", "Program Owner": "BASF", "Segment": "Ag Chem", "Program Year": "2025", "Originator": "Published by Supplier", "Earnings $": 15000, "Earnings %": 35},
        {"Program Name": "Seed Starter", "Program Owner": "Bayer", "Segment": "Seed", "Program Year": "2025", "Originator": "Created as Unverified by My Org", "Earnings $": 9000, "Earnings %": 20},
        {"Program Name": "Fert Bonus", "Program Owner": "Nutrien", "Segment": "Fertilizer", "Program Year": "2024", "Originator": "Published by Supplier", "Earnings $": 7000, "Earnings %": 15},
        {"Program Name": "Promo Boost", "Program Owner": "Syngenta", "Segment": "Promarket", "Program Year": "2025", "Originator": "Created as Unverified by My Org", "Earnings $": 4000, "Earnings %": 10},
    ])

    # 🔍 Filters
    st.subheader("Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name_filter = st.text_input("Search Program Name")
    with col2:
        year_filter = st.selectbox("Program Year", options=["All"] + sorted(data["Program Year"].unique().tolist()))
    with col3:
        owner_filter = st.selectbox("Program Owner", options=["All"] + sorted(data["Program Owner"].unique().tolist()))
    with col4:
        segment_filter = st.selectbox("Segment", options=["All"] + sorted(data["Segment"].unique().tolist()))

    originator_filter = st.radio(
        "Originator",
        options=["All", "Published by Supplier", "Created as Unverified by My Org"],
        horizontal=True
    )

    # 🧠 Apply filters
    filtered = data.copy()
    if name_filter:
        filtered = filtered[filtered["Program Name"].str.contains(name_filter, case=False)]
    if year_filter != "All":
        filtered = filtered[filtered["Program Year"] == year_filter]
    if owner_filter != "All":
        filtered = filtered[filtered["Program Owner"] == owner_filter]
    if segment_filter != "All":
        filtered = filtered[filtered["Segment"] == segment_filter]
    if originator_filter != "All":
        filtered = filtered[filtered["Originator"] == originator_filter]

    # 📊 Sort by highest Earnings $
    filtered = filtered.sort_values(by="Earnings $", ascending=False)

    # 💵 Format for display
    filtered["Earnings $"] = filtered["Earnings $"].apply(lambda x: f"${x:,.2f}")
    filtered["Earnings %"] = filtered["Earnings %"].apply(lambda x: f"{x:.1f}%")

    # 📋 Show table
    st.subheader("Your Programs")
    st.dataframe(
        filtered[["Program Name", "Program Owner", "Segment", "Earnings $", "Earnings %"]],
        use_container_width=True
    )

    # ➕ Create Program button
    st.markdown("---")
    if st.button("➕ Create Program"):
        st.session_state["page"] = "upload"
        st.experimental_rerun()
