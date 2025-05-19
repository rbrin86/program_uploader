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

    # 💵 Format earnings
    filtered["Earnings $"] = filtered["Earnings $"].apply(lambda x: f"${x:,.2f}")
    filtered["Earnings %"] = filtered["Earnings %"].apply(lambda x: f"{x:.1f}%")

    # 🧾 Display table with multi-select and navigation
    st.write("#### Programs Overview")
    if filtered.empty:
        st.write("No programs match the selected filters.")
    else:
        # Initialize selection state
        if "selected_indices" not in st.session_state:
            st.session_state.selected_indices = []

        # Prepare table data
        table_data = filtered.reset_index().to_dict("records")
        cols = st.columns([0.5, 2, 1, 1, 1, 1, 1])  # Checkbox, Program Name, Owner, Segment, Earnings $, Earnings %, Status
        headers = ["", "Program Name", "Owner", "Segment", "Earnings $", "Earnings %", "Status"]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        for i, row in enumerate(table_data):
            cols = st.columns([0.5, 2, 1, 1, 1, 1, 1])
            cols[0].checkbox("", key=f"select_{i}", value=i in st.session_state.selected_indices, on_change=lambda x=i: update_selection(x))
            # Make Program Name clickable to navigate to program details
            if cols[1].button(row["Program Name"], key=f"program_{i}"):
                # Find the corresponding program in data or unverified_programs
                program_idx = i
                if i >= len(data) and unverified_programs:
                    program_idx = i - len(data)
                    selected_program = unverified_programs[program_idx]
                else:
                    selected_program = {
                        "Program": {
                            "Name": row["Program Name"],
                            "Owner": row["Program Owner"],
                            "Start Date": f"{row['Program Year']}-01-01",  # Placeholder date
                            "End Date": f"{row['Program Year']}-12-31",    # Placeholder date
                            "Segment": row["Segment"]
                        },
                        "Incentives": [],  # Placeholder, to be expanded
                        "Status": row["Status"]
                    }
                navigate_to("program_details", selected_program)
            cols[2].write(row["Program Owner"])
            cols[3].write(row["Segment"])
            cols[4].write(row["Earnings $"])
            cols[5].write(row["Earnings %"])
            cols[6].write(row["Status"])

        # Bulk update form
        with st.form(key="bulk_update_form"):
            new_segment = st.selectbox("Update Segment To", [""] + sorted(data["Segment"].unique()), index=0)
            if st.form_submit_button("Apply Bulk Update"):
                if new_segment and st.session_state.selected_indices:
                    for idx in st.session_state.selected_indices:
                        if idx < len(data):  # Update sample data
                            data.loc[idx, "Segment"] = new_segment
                        if idx < len(data) and idx < len(unverified_programs):  # Update unverified programs
                            unverified_programs[idx]["Program"]["Segment"] = new_segment
                    st.session_state.selected_indices = []  # Clear selection after update
                    st.success("Segment updated successfully for selected programs.")
                    st.rerun()
                else:
                    st.error("Please select at least one program and choose a segment.")

def update_selection(index):
    if index in st.session_state.selected_indices:
        st.session_state.selected_indices.remove(index)
    else:
        st.session_state.selected_indices.append(index)
    st.session_state.selected_indices = sorted(list(set(st.session_state.selected_indices)))

st.markdown("---")
if st.button("➕ Create Program"):
    navigate_to("program_upload")