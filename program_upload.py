import streamlit as st

def render_program_upload(navigate_to):
    st.title("📤 Upload Unverified Program")

    # Hardcoded product catalog
    PRODUCT_CATALOG = ["Acme Fert 123-A", "Acme Fert 123-B", "Acme Seed 456"]

    # Initialize session state to store submitted programs
    if "unverified_programs" not in st.session_state:
        st.session_state.unverified_programs = []

    uploaded_file = st.file_uploader("Upload a PDF of your rebate program", type="pdf")

    if uploaded_file:
        st.success("✅ File uploaded successfully. Extracting program details...")

        # Hardcoded extracted data (replace with actual OCR logic later)
        extracted_data = {
            "Program": {
                "Name": "2025 Opportunity",
                "Owner": "BASF",
                "Start Date": "2024-10-01",
                "End Date": "2025-09-30",
                "Segment": "Ag Chem"
            },
            "Price Rules": [
                {
                    "Name": "Q1 Rebate",
                    "Region": None,
                    "Price Rules Type": "Fixed % Rebate",
                    "Amount": "1%",
                    "Paid On": "Net Purchases",
                    "Products": ["Acme Fertilizer 123"]
                }
            ]
        }

        st.subheader("🔍 Extracted Program Details")
        program_form = st.form(key="program_form")
        with program_form:
            # Program details
            for field, value in extracted_data["Program"].items():
                extracted_data["Program"][field] = st.text_input(field, value or "", disabled=value is not None)

            # Incentive details
            st.subheader("Price Rules")
            for i, incentive in enumerate(extracted_data["Price Rules"]):
                st.write(f"Price Rules {i+1}")
                for field, value in incentive.items():
                    if field != "Products":
                        incentive[field] = st.text_input(f"{field} (Incentive {i+1})", value or "", disabled=value is not None)
                st.subheader(f"Product Mapping for Incentive {i+1}")
                for j, product in enumerate(incentive["Products"]):
                    selected_product = st.selectbox(
                        f"Map '{product}'",
                        ["Unmapped"] + PRODUCT_CATALOG,
                        index=0,
                        key=f"product_{i}_{j}"
                    )
                    incentive["Products"][j] = selected_product if selected_product != "Unmapped" else None

            if st.form_submit_button("✅ Submit Program"):
                missing_fields = [f for f, v in extracted_data["Program"].items() if not v] + \
                                [f for i in extracted_data["Price Rules"] for f, v in i.items() if f != "Products" and not v] + \
                                [p for i in extracted_data["Price Rules"] for p in i["Products"] if not p]
                if missing_fields:
                    st.error(f"Please complete missing fields: {', '.join(missing_fields)}")
                else:
                    # Store in session state instead of database
                    st.session_state.unverified_programs.append({
                        "Program": extracted_data["Program"],
                        "Price Rules": extracted_data["Price Rules"],
                        "Status": "Unverified"
                    })
                    st.success("🎉 Program submitted as Unverified.")
                    if st.button("🔙 Back to Programs"):
                        navigate_to("we_earn")

    else:
        if st.button("🔙 Back to Programs"):
            navigate_to("we_earn")