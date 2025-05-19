import streamlit as st

def render_program_upload(navigate_to):
    st.title("📤 Upload Unverified Program")

    uploaded_file = st.file_uploader("Upload a PDF of your rebate program", type="pdf")

    if uploaded_file:
        st.success("✅ File uploaded successfully (simulated parsing).")
        st.text("Here are the extracted fields (example):")
        st.write({
            "Program Name": "Early Order Discount 2025",
            "Start Date": "2025-01-01",
            "End Date": "2025-06-30",
            "Incentive": "5% on qualifying products",
            "Region": "Northwest"
        })

        st.markdown("---")
        if st.button("✅ Submit Program"):
            st.success("🎉 Program submitted successfully as Unverified.")
            if st.button("🔙 Back to Programs"):
                navigate_to("we_earn")
    else:
        if st.button("🔙 Back to Programs"):
            navigate_to("we_earn")
