import streamlit as st
import pandas as pd

def render_program_details(navigate_to):
    st.write("Debug: Entering Program Details page")
    st.write(f"Debug: Selected program: {st.session_state.get('selected_program')}")
    st.title("📋 Program Details")
    selected_program = st.session_state.get("selected_program")

    if not selected_program:
        st.error("No program selected. Please select a program from the 'We Earn' page.")
        if st.button("🔙 Back to We Earn", key="back_to_we_earn"):
            st.write("Debug: Back to We Earn clicked")
            navigate_to("we_earn", None)
        return

    # Tabbed layout
    tab1, tab2, tab3 = st.tabs(["Program Summary", "Cases", "Accommodations"])

    # Tab 1: Program Summary
    with tab1:
        st.subheader("Program Summary")
        with st.container():
            col1, col2 = st.columns(2)
            col1.write(f"**Name:** {selected_program['Program']['Name']}")
            col1.write(f"**Program Year:** {selected_program['Program'].get('Start Date', 'N/A')[:4]}")
            col1.write(f"**Previous Years Program:** T&O Marketing Program 2024")
            col2.write(f"**Effective Dates:** {selected_program['Program'].get('Start Date', 'N/A')} - {selected_program['Program'].get('End Date', 'N/A')}")
            col2.write(f"**Attachments:** [Program Document](https://example.com)")
            col1.write(f"**Segment:** {selected_program['Program']['Segment']}")
        st.write(f"**YTD Earnings:** $5,994.16 (0.18% of YTD earnings)")

        # Incentives/Price Rules Table
        st.subheader("Incentives")
        incentives = selected_program.get("Incentives", [])
        if not incentives:
            incentives = [
                {
                    "Name": "Additional Rebate - 10 brands",
                    "Start Date": "2024-09-01",
                    "End Date": "2025-08-31",
                    "Incentive Type": "Fixed % Rebate",
                    "Amount": "5%",
                    "Current Earnings": "$0"
                },
                {
                    "Name": "Volume Discount Q1",
                    "Start Date": "2025-01-01",
                    "End Date": "2025-03-31",
                    "Incentive Type": "Volume Discount",
                    "Amount": "$500",
                    "Current Earnings": "$0"
                },
                {
                    "Name": "Early Payment Bonus",
                    "Start Date": "2024-10-01",
                    "End Date": "2024-12-31",
                    "Incentive Type": "Cash Rebate",
                    "Amount": "$1000",
                    "Current Earnings": "$0"
                }
            ]
        data = {
            "Name": [inc["Name"] for inc in incentives],
            "Transaction Eligibility Period": [f"{inc.get('Start Date', 'N/A')} - {inc.get('End Date', 'N/A')}" for inc in incentives],
            "Incentive Type": [inc.get("Incentive Type", "N/A") for inc in incentives],
            "Rebate Amount": [inc.get("Amount", "N/A") for inc in incentives],
            "Current Earnings": [inc.get("Current Earnings", "$0") for inc in incentives]
        }
        df = pd.DataFrame(data)
        st.table(df)

    # Tab 2: Cases
    with tab2:
        st.subheader("Cases")
        with st.container():
            st.write("No cases associated with this program yet.")

    # Tab 3: Accommodations
    with tab3:
        st.subheader("Accommodations")
        with st.container():
            st.write("This tab is reserved for future accommodations data.")

    st.markdown("---")
    if st.button("🔙 Back to We Earn", key="back_to_we_earn_details"):
        st.write("Debug: Back to We Earn clicked")
        navigate_to("we_earn", None)