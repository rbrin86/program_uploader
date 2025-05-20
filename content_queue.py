import streamlit as st

def render_content_queue(navigate_to):
    st.title("📋 Content Queue")
    st.write("### Unverified Programs")

    # Initialize with sample programs if the queue is empty
    if "unverified_programs" not in st.session_state or not st.session_state.unverified_programs:
        st.session_state.unverified_programs = [
            {
                "Program": {
                    "Name": "2025 Opportunity",
                    "Owner": "BASF",
                    "Start Date": "2024-10-01",
                    "End Date": "2025-09-30",
                    "Segment": "Ag Chem"
                },
                "Incentives": [
                    {
                        "Name": "Q1 Rebate",
                        "Region": "Southwest",
                        "Incentive Type": "Fixed % Rebate",
                        "Amount": "1%",
                        "Paid On": "Net Purchases",
                        "Products": ["Armezon Pro"]
                    }
                ],
                "Status": "Unverified"
            },
            {
                "Program": {
                    "Name": "Harvest Boost 2025",
                    "Owner": "Bayer",
                    "Start Date": "2025-01-01",
                    "End Date": "2025-12-31",
                    "Segment": "Fertilizer"
                },
                "Incentives": [
                    {
                        "Name": "Early Season Bonus",
                        "Region": "Midwest",
                        "Incentive Type": "Volume Discount",
                        "Amount": "750",
                        "Paid On": "Unit Volume",
                        "Products": ["Roundup PowerMAX"]
                    }
                ],
                "Status": "Unverified"
            },
            {
                "Program": {
                    "Name": "Yield Max 2024",
                    "Owner": "Syngenta",
                    "Start Date": "2024-03-01",
                    "End Date": "2024-11-30",
                    "Segment": "Seed"
                },
                "Incentives": [
                    {
                        "Name": "Growth Incentive",
                        "Region": "Northeast",
                        "Incentive Type": "Cash Rebate",
                        "Amount": "1000",
                        "Paid On": "Gross Sales",
                        "Products": ["Acuron"]
                    }
                ],
                "Status": "In Review"
            },
            {
                "Program": {
                    "Name": "Spring Advantage",
                    "Owner": "BASF",
                    "Start Date": "2025-02-01",
                    "End Date": "2025-10-31",
                    "Segment": "Ag Chem"
                },
                "Incentives": [
                    {
                        "Name": "Seasonal Rebate",
                        "Region": "West",
                        "Incentive Type": "Fixed % Rebate",
                        "Amount": "2.5%",
                        "Paid On": "Net Purchases",
                        "Products": ["Liberty"]
                    }
                ],
                "Status": "Unverified"
            }
        ]

    programs = st.session_state.unverified_programs

    if not programs:
        st.write("No unverified programs in the queue.")
    else:
        # Prepare data for the table
        table_data = []
        for i, program in enumerate(programs):
            row = {
                "Program Name": program["Program"]["Name"],
                "Owner": program["Program"]["Owner"],
                "Segment": program["Program"]["Segment"],
                "Status": program["Status"],
                "Verify": ""  # Placeholder for the Verify button
            }
            table_data.append(row)

        # Display the table
        st.write("#### Programs Queue")
        for i, row in enumerate(table_data):
            cols = st.columns([2, 1, 1, 1, 1])
            cols[0].write(row["Program Name"])
            cols[1].write(row["Owner"])
            cols[2].write(row["Segment"])
            cols[3].write(row["Status"])
            if row["Status"] == "Unverified":
                if cols[4].button("Verify", key=f"verify_{i}"):
                    programs[i]["Status"] = "Verified"
                    st.rerun()
            else:
                cols[4].write("—")

    st.markdown("---")
    if st.button("🔙 Back to Programs"):
        navigate_to("we_earn")