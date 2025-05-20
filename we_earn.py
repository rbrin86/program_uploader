import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("💰 We Earn – Programs Overview")

    # Debug: Display current session state
    st.write(f"Debug: Current session state - page: {st.session_state.get('page')}, selected_program: {st.session_state.get('selected_program')}")

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

    # 💵 Format earnings for display
    display_data = filtered.copy()
    display_data["Earnings $"] = display_data["Earnings $"].apply(lambda x: f"${x:,.2f}")
    display_data["Earnings %"] = display_data["Earnings %"].apply(lambda x: f"{x:.1f}%")

    # Add a "View Details" column (for display only)
    display_data["View Details"] = [
        f"View {row['Program Name']}" for _, row in display_data.iterrows()
    ]

    # 🧾 Display table
    display_columns = ["Status", "Program Name", "Program Owner", "Segment", "Earnings $", "Earnings %", "View Details"]
    st.dataframe(
        display_data[display_columns],
        use_container_width=True,
        column_config={
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Program Name": st.column_config.TextColumn("Program Name", width="medium"),
            "View Details": st.column_config.TextColumn("View Details", width="small")
        },
        hide_index=True
    )

    # Handle navigation for View Details buttons
    st.markdown("### Select a Program to View Details")
    for i, row in filtered.iterrows():
        program_data = {
            "Program": {
                "Name": row["Program Name"],
                "Owner": row["Program Owner"],
                "Segment": row["Segment"],
                "Start Date": f"{row['Program Year']}-01-01",  # Placeholder date
                "End Date": f"{row['Program Year']}-12-31",    # Placeholder date
            },
            "Status": row["Status"]
        }
        button_key = f"view_details_{row['Program Name'].replace(' ', '_')}_{i}"
        if st.button(f"View {row['Program Name']}", key=button_key):
            st.write(f"Debug: Clicked 'View {row['Program Name']}' with key {button_key}")
            st.write(f"Debug: Setting selected_program to {program_data}")
            st.session_state.selected_program = program_data
            st.session_state.page = "program_details"
            st.write(f"Debug: Triggering navigation to program_details with selected_program: {st.session_state.selected_program}")
            st.rerun()

    st.markdown("---")
    if st.button("➕ Create Program"):
        st.write("Debug: Navigating to program_upload")
        navigate_to("program_upload")