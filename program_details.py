import streamlit as st
import pandas as pd

def render_program_details(navigate_to):
    st.title("📋 Program Details")
    selected_program = st.session_state.get("selected_program")

    if not selected_program:
        st.write("No program selected. Please select a program from the 'We Earn' page.")
        if st.button("🔙 Back to We Earn"):
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
            col1.write(f"**Program Year:** {selected_program['Program'].get('Start Date', 'N/A')[:4]}")  # Extract year from Start Date
            col1.write(f"**Previous Years Program:** T&O Marketing Program 2024")  # Placeholder
            col2.write(f"**Effective Dates:** {selected_program['Program'].get('Start Date', 'N/A')} - {selected_program['Program'].get('End Date', 'N/A')}")
            col2.write(f"**Attachments:** [Program Document](https://example.com)")  # Placeholder link
            col1.write(f"**Segment:** {selected_program['Program']['Segment']}")
        st.write(f"**YTD Earnings:** $5,994.16 (0.18% of YTD earnings)")  # Placeholder, to be updated with actual data

    # Tab 2: Cases
    with tab2:
        st.subheader("Cases")
        with st.container():
            st.write("No cases associated with this program yet.")  # Placeholder

    # Tab 3: Accommodations
    with tab3:
        st.subheader("Accommodations")
        with st.container():
            st.write("This tab is reserved for future accommodations data.")  # Placeholder

    st.markdown("---")
    if st.button("🔙 Back to We Earn"):
        navigate_to("we_earn", None)