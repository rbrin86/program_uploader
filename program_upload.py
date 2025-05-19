import streamlit as st

def render_program_upload(navigate_to):
    st.title("📄 Upload a Program PDF")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        st.success("✅ PDF uploaded successfully (simulated parsing).")

        # Simulated extracted data
        st.subheader("Extracted Details (Review & Edit):")
        st.text_input("Program Name", value="Q3 Partner Growth")
        st.selectbox("Segment", ["Ag Chem", "Seed", "Fertilizer"], index=0)
        st.date_input("Start Date")
        st.date_input("End Date")
        st.text_area("Incentive Details", value="5% bonus_
