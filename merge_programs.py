import streamlit as st
import pandas as pd

def render_merge_programs(navigate_to):
    st.title("🔗 Merge Program Submissions")

    # Simulated near-duplicate programs
    program_a = {
        "Program Name": "Early Order Bonus 2025",
        "Submitted By": "Wilbur",
        "Segment": "Ag Chem",
        "Region": "Midwest",
        "Incentives": [
            {
                "Product": "Atrazine 4L",
                "Rebate Amount": "5%",
                "Incentive Type": "Volume Rebate",
                "Region": "Midwest"
            },
            {
                "Product": "Harness Xtra",
                "Rebate Amount": "$10/gal",
                "Incentive Type": "Early Order Discount",
                "Region": "Midwest"
            }
        ]
    }

    program_b = {
        "Program Name": "Early Order Bonus 2025 ",
        "Submitted By": "CHS",
        "Segment": "Ag Chem",
        "Region": "Central",
        "Incentives": [
            {
                "Product": "Atrazine 4L",
                "Rebate Amount": "5%",
                "Incentive Type": "Volume Rebate",
                "Region": "Central"
            },
            {
                "Product": "Balance Flexx",
                "Rebate Amount": "$7/gal",
                "Incentive Type": "New Product Launch",
                "Region": "Central"
            }
        ]
    }

    st.subheader("🧾 Program Details Comparison")
    meta_data = {
        "Program Name": [program_a["Program Name"], program_b["Program Name"]],
        "Submitted By": [program_a["Submitted By"], program_b["Submitted By"]],
        "Segment": [program_a["Segment"], program_b["Segment"]],
        "Region": [program_a["Region"], program_b["Region"]],
    }
    meta_df = pd.DataFrame(meta_data, index=["Program A", "Program B"]).T
    st.table(meta_df)

    st.subheader("🎯 Incentives Comparison")

    incentive_a = pd.DataFrame(program_a["Incentives"])
    incentive_b = pd.DataFrame(program_b["Incentives"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Program A – Wilbur**")
        st.table(incentive_a)
    with col2:
        st.markdown("**Program B – CHS**")
        st.table(incentive_b)

    st.markdown("---")
    st.subheader("🤔 What would you like to do?")

    cols = st.columns(3)
    if cols[0].button("🔗 Merge as One Program"):
        st.success("Programs merged into a single verified program.")
        navigate_to("content_queue")

    if cols[1].button("✅ Accept Both as Separate"):
        st.info("Both programs accepted as unique entries.")
        navigate_to("content_queue")

    if cols[2].button("❌ Reject Program B (CHS)"):
        st.warning("Program B rejected.")
        navigate_to("content_queue")

    st.markdown("---")
    if st.button("🔙 Back to Content Queue"):
        navigate_to("content_queue")
