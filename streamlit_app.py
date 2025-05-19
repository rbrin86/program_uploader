import streamlit as st

def render_content_queue(navigate_to):
    st.title("📋 Content Queue")
    st.write("### Unverified Programs")

    # Hardcoded fallback data (used if session state is empty)
    hardcoded_programs = [
        {
            "Program": {
                "Name": "Sample Program 2025",
                "Owner": "BASF",
                "Segment": "Ag Chem"
            },
            "Incentives": [
                {"Name": "Sample Incentive", "Region": "North"}
            ],
            "Status": "Unverified"
        }
    ]

    # Use session state data if available, otherwise use hardcoded data
    programs = st.session_state.get("unverified_programs", hardcoded_programs)

    if not programs:
        st.write("No unverified programs in the queue.")
    else:
        for i, program in enumerate(programs):
            with st.expander(f"Program {i+1}: {program['Program']['Name']}"):
                st.write(f"**Owner:** {program['Program']['Owner']}")
                st.write(f"**Segment:** {program['Program']['Segment']}")
                st.write(f"**Status:** {program['Status']}")
                if program['Status'] == "Unverified":
                    if st.button("Mark as Verified", key=f"verify_{i}"):
                        program['Status'] = "Verified"
                        st.rerun()
                st.write("**Incentives:**")
                for j, incentive in enumerate(program['Incentives']):
                    st.write(f"- {incentive['Name']} (Region: {incentive['Region']})")
    
    st.markdown("---")
    if st.button("🔙 Back to Programs"):
        navigate_to("we_earn")