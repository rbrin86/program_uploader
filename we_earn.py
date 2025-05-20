import streamlit as st
import pandas as pd

def render_we_earn(navigate_to):
    st.title("💰 We Earn – Programs Overview")

    # Test navigation with a simple button
    st.write("### Navigation Test")
    if st.button("Go to Program Details (Test)", key="test_navigate"):
        st.write("Debug: Test button clicked")
        selected_program = {
            "Program": {
                "Name": "Test Program",
                "Owner": "Test Owner",
                "Start Date": "2025-01-01",
                "End Date": "2025-12-31",
                "Segment": "Test Segment"
            },
            "Incentives": [],
            "Status": "Test Status"
        }
        st.write("Debug: Calling navigate_to with program: Test Program")
        navigate_to("program_details", selected_program)

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

    # 🧾 Display table with Status in Column A using st.columns for reliable row clicks
    st.write("#### Programs Overview")
    if filtered.empty:
        st.write("No programs match the selected filters.")
    else:
        # Display table headers
        cols = st.columns([1, 2, 1, 1, 1, 1])
        headers = ["Status", "Program Name", "Program Owner", "Segment", "Earnings $", "Earnings %"]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        # Display table rows with clickable functionality
        for idx, row in filtered.iterrows():
            cols = st.columns([1, 2, 1, 1, 1, 1])
            cols[0].write(row["Status"])
            if cols[1].button(row["Program Name"], key=f"program_{idx}"):
                st.write(f"Debug: Clicked program at index {idx}")
                if idx < len(data):
                    selected_program = {
                        "Program": {
                            "Name": data.iloc[idx]["Program Name"],
                            "Owner": data.iloc[idx]["Program Owner"],
                            "Start Date": f"{data.iloc[idx]['Program Year']}-01-01",
                            "End Date": f"{data.iloc[idx]['Program Year']}-12-31",
                            "Segment": data.iloc[idx]["Segment"]
                        },
                        "Incentives": [],
                        "Status": data.iloc[idx]["Status"]
                    }
                else:
                    unverified_idx = idx - len(data)
                    selected_program = unverified_programs[unverified_idx]
                st.write(f"Debug: Navigating to program_details with program: {selected_program['Program']['Name']}")
                navigate_to("program_details", selected_program)
            cols[2].write(row["Program Owner"])
            cols[3].write(row["Segment"])
            cols[4].write(row["Earnings $"])
            cols[5].write(row["Earnings %"])

    st.markdown("---")
    if st.button("➕ Create Program"):
        st.write("Debug: Create Program button clicked")
        navigate_to("program_upload")