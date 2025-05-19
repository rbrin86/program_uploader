import streamlit as st

def render_program_upload(navigate_to):
    st.title("📤 Upload Unverified Program")

    uploaded_file = st.file_uploader("Upload a PDF of your rebate program", type="pdf")

    # Simulated field extraction from PDF
    if uploaded_file:
        st.success("✅ File uploaded successfully. Extracting program details...")

        # Simulated extracted data
        extracted_data = {
            "Program Name": "2025 Opportunity",
            "Program Owner": "BASF",
            "Start Date": "2024-10-01",
            "End Date": "2025-09-30",
            "Products/Brands": None,  # Missing
            "Incentive Amount": "1%",
            "Incentive Type": "Fixed % Rebate",
            "Paid On": "Net Purchases",
            "Region": None  # Missing
        }

        st.subheader("🔍 Extracted Program Details")
        missing_fields = []

        for field, value in extracted_data.items():
            if value is None:
                missing_fields.append(field)
                new_value = st.text_input(f"❗ Missing: {field}", placeholder="Enter value")
                extracted_data[field] = new_value
            else:
                st.text_input(field, value, disabled=True)

        if st.button("✅ Submit Program"):
            if any(not extracted_data[field] for field in missing_fields):
                st.error("Please complete all missing fields before submitting.")
            else:
                st.success("🎉 Program submitted successfully as Unverified.")
                if st.button("🔙 Back to Programs"):
                    navigate_to("we_earn")

    else:
        if st.button("🔙 Back to Programs"):
            navigate_to("we_earn")