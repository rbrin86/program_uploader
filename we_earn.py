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

    # 🧾 Display table with Status in Column A
    display_columns = ["Status", "Program Name", "Program Owner", "Segment", "Earnings $", "Earnings %"]
    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        column_config={"Status": st.column_config.TextColumn("Status", width="small")},
        hide_index=True
    )

    # Add custom JavaScript to make rows clickable
    st.markdown("""
        <style>
            div[data-testid="stDataFrame"] tr:hover {
                cursor: pointer;
                background-color: #f0f0f0;
            }
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const rows = document.querySelectorAll('div[data-testid="stDataFrame"] tbody tr');
                rows.forEach((row, index) => {
                    row.addEventListener('click', () => {
                        window.parent.location.hash = 'program_' + index;
                    });
                });
            });
        </script>
    """, unsafe_allow_html=True)

    # Handle row click navigation
    selected_program_idx = st.query_params.get("program", None)
    if selected_program_idx:
        idx = int(selected_program_idx.replace("program_", ""))
        if 0 <= idx < len(filtered):
            global_idx = filtered.index[idx]
            if global_idx < len(data):  # Sample data program
                selected_program = {
                    "Program": {
                        "Name": data.iloc[global_idx]["Program Name"],
                        "Owner": data.iloc[global_idx]["Program Owner"],
                        "Start Date": f"{data.iloc[global_idx]['Program Year']}-01-01",
                        "End Date": f"{data.iloc[global_idx]['Program Year']}-12-31",
                        "Segment": data.iloc[global_idx]["Segment"]
                    },
                    "Incentives": [],  # Placeholder
                    "Status": data.iloc[global_idx]["Status"]
                }
            else:  # Unverified program
                unverified_idx = global_idx - len(data)
                selected_program = unverified_programs[unverified_idx]
            navigate_to("program_details", selected_program)
        st.query_params.clear()

    st.markdown("---")
    if st.button("➕ Create Program"):
        navigate_to("program_upload")