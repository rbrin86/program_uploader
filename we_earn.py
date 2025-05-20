import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("💰 We Earn – Programs Overview")

    # Sample data
    data = pd.DataFrame([
        {"Program Name": "Early Order Bonus 2025", "Program Owner": "BASF", "Segment": "Ag Chem", "Earnings $": 15000, "Status": "Verified"},
        {"Program Name": "Spring Push", "Program Owner": "Bayer", "Segment": "Fertilizer", "Earnings $": 8700, "Status": "Verified"},
        {"Program Name": "Growth Incentive Q1", "Program Owner": "BASF", "Segment": "Seed", "Earnings $": 22100, "Status": "Verified"}
    ])

    # Append unverified programs from session state
    unverified_programs = st.session_state.get("unverified_programs", [])
    if unverified_programs:
        unverified_data = pd.DataFrame([
            {"Program Name": program["Program"]["Name"], "Program Owner": program["Program"]["Owner"], 
             "Segment": program["Program"]["Segment"], "Earnings $": 0, "Status": program["Status"]}
            for program in unverified_programs
        ])
        data = pd.concat([data, unverified_data], ignore_index=True)

    # Filters
    st.sidebar.header("🔎 Filter Programs")
    selected_owner = st.sidebar.selectbox("Program Owner", ["All"] + sorted(data["Program Owner"].unique()), index=0)
    selected_segment = st.sidebar.selectbox("Segment", ["All"] + sorted(data["Segment"].unique()), index=0)
    selected_status = st.sidebar.selectbox("Status", ["All"] + sorted(data["Status"].unique()), index=0)

    # Apply filters
    filtered = data.copy()
    if selected_owner != "All":
        filtered = filtered[filtered["Program Owner"] == selected_owner]
    if selected_segment != "All":
        filtered = filtered[filtered["Segment"] == selected_segment]
    if selected_status != "All":
        filtered = filtered[filtered["Status"] == selected_status]

    # Format earnings
    filtered["Earnings $"] = filtered["Earnings $"].apply(lambda x: f"${x:,.2f}")

    # Display table
    st.write("#### Programs Overview")
    if filtered.empty:
        st.write("No programs match the selected filters.")
    else:
        # Make Program Name clickable
        def make_clickable(name, idx):
            return f'<a href="#" onclick="window.parent.location.hash=\'program_{idx}\';">{name}</a>'

        filtered_with_links = filtered.copy()
        filtered_with_links["Program Name"] = [make_clickable(name, idx) for idx, name in enumerate(filtered["Program Name"])]
        st.dataframe(filtered_with_links, use_container_width=True, hide_index=True)

        # Handle navigation on click
        selected_program_idx = st.query_params.get("program", None)
        if selected_program_idx:
            idx = int(selected_program_idx.replace("program_", ""))
            if 0 <= idx < len(data):
                selected_program = {
                    "Program": {
                        "Name": data.iloc[idx]["Program Name"],
                        "Owner": data.iloc[idx]["Program Owner"],
                        "Start Date": "2025-01-01",  # Placeholder
                        "End Date": "2025-12-31",    # Placeholder
                        "Segment": data.iloc[idx]["Segment"]
                    },
                    "Incentives": [],  # Placeholder
                    "Status": data.iloc[idx]["Status"]
                }
                st.write(f"Debug: Navigating to program_details with {selected_program['Program']['Name']}")
                navigate_to("program_details", selected_program)
            elif idx < len(data) + len(unverified_programs):
                unverified_idx = idx - len(data)
                selected_program = unverified_programs[unverified_idx]
                st.write(f"Debug: Navigating to program_details with {selected_program['Program']['Name']}")
                navigate_to("program_details", selected_program)
            st.query_params.clear()

    st.markdown("---")
    if st.button("➕ Create Program", key="create_program"):
        st.write("Debug: Create Program clicked")
        navigate_to("program_upload")