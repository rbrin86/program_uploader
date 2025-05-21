import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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
            "Earnings %": 12.5,
            "Status": "Verified"
        },
        {
            "Program Name": "Spring Push",
            "Program Owner": "Bayer",
            "Segment": "Fertilizer",
            "Program Year": "2025",
            "Originator": "Created as Unverified by My Org",
            "Earnings $": 8700,
            "Earnings %": 9.2,
            "Status": "Verified"
        },
        {
            "Program Name": "Growth Incentive Q1",
            "Program Owner": "BASF",
            "Segment": "Seed",
            "Program Year": "2024",
            "Originator": "Supplier provided",
            "Earnings $": 22100,
            "Earnings %": 14.0,
            "Status": "Verified"
        }
    ])

    # Append unverified programs from session state
    unverified_programs = st.session_state.get("unverified_programs", [])
    if unverified_programs:
        unverified_data = pd.DataFrame([
            {
                "Program Name": program["Program"]["Name"],
                "Program Owner": program["Program"]["Owner"],
                "Segment": program["Program"]["Segment"],
                "Program Year": program["Program"]["Start Date"][:4],
                "Originator": "Created as Unverified by My Org",
                "Earnings $": 0,
                "Earnings %": 0.0,
                "Status": program["Status"]
            } for program in unverified_programs
        ])
        data = pd.concat([data, unverified_data], ignore_index=True)

    # 🔍 Filters
    st.sidebar.header("🔎 Filter Programs")
    selected_year = st.sidebar.selectbox("Program Year", ["All"] + sorted(data["Program Year"].unique()), index=0)
    selected_owner = st.sidebar.selectbox("Program Owner", ["All"] + sorted(data["Program Owner"].unique()), index=0)
    selected_segment = st.sidebar.selectbox("Segment", ["All"] + sorted(data["Segment"].unique()), index=0)
    selected_originator = st.sidebar.selectbox("Program Originator", ["All"] + sorted(data["Originator"].unique()), index=0)
    selected_status = st.sidebar.selectbox("Status", ["All"] + sorted(data["Status"].unique()), index=0)

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
    if selected_status != "All":
        filtered = filtered[filtered["Status"] == selected_status]

    # Format earnings
    filtered["Earnings $"] = filtered["Earnings $"].apply(lambda x: f"${x:,.2f}")
    filtered["Earnings %"] = filtered["Earnings %"].apply(lambda x: f"{x:.1f}%")

    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(filtered)
    gb.configure_pagination()
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    # Show interactive table
    response = AgGrid(
        filtered,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=400,
        use_container_width=True,
    )

    # Navigate on row selection
    selected_rows = response["selected_rows"]
    if selected_rows:
        row = selected_rows[0]
        program_data = {
            "Program": {
                "Name": row["Program Name"],
                "Owner": row["Program Owner"],
                "Segment": row["Segment"],
                "Start Date": f"{row['Program Year']}-01-01",
                "End Date": f"{row['Program Year']}-12-31",
            },
            "Status": row["Status"]
        }
        navigate_to("program_details", program_data)

    st.markdown("---")
    if st.button("➕ Create Program"):
        navigate_to("program_upload")
