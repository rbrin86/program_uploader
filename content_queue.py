import streamlit as st
import pandas as pd

def render_content_queue(navigate_to):
    st.title("📥 Review Unverified Programs")

    st.markdown("These programs were submitted by Receivers and need review by your team to approve, reject, or merge potential duplicates.")

    # Dummy unverified programs (with potential duplicates)
    queue = [
        {
            "Program Name": "Early Order Bonus 2025",
            "Customer": "Wilbur",
            "AI Confidence": "92%",
            "Status": "Needs Review"
        },
        {
            "Program Name": "Early Order Bonus 2025 ",
            "Customer": "CHS",
            "AI Confidence": "89%",
            "Status": "Needs Review"
        },
        {
            "Program Name": "Spring Start-Up Rebate",
            "Customer": "Simplot",
            "AI Confidence": "76%",
            "Status": "Needs Review"
        }
    ]

    df = pd.DataFrame(queue)

    st.subheader("Unverified Program Submissions")
    st.table(df)

    # Simulated review actions (simple for now)
    st.subheader("Actions")
    for i, row in df.iterrows():
        st.markdown(f"**{row['Program Name']}** – from {row['Customer']} (Confidence: {row['AI Confidence']})")
        cols = st.columns(4)
        if cols[0].button("✅ Approve", key=f"approve_{i}"):
            st.success(f"{row['Program Name']} from {row['Customer']} approved.")
        if cols[1].button("❌ Reject", key=f"reject_{i}"):
            st.warning(f"{row['Program Name']} from {row['Customer']} rejected.")
        if cols[2].button("🔄 Update", key=f"update_{i}"):
            st.info(f"{row['Program Name']} from {row['Customer']} queued for update.")
        if cols[3].button("🔗 Merge", key=f"merge_{i}"):
            # For now, hardcode the two programs to compare
            st.session_state.programs_to_merge = ["Wilbur", "CHS"]
            navigate_to("merge_programs")
    
    st.markdown("---")
    if st.button("🔙 Back to Dashboard"):
        navigate_to("we_earn", None)
