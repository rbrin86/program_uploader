import streamlit as st

def render_program_upload(navigate_to):
    st.title("📤 Upload Unverified Program")

    # Hardcoded system values
    PRODUCT_CATALOG = ["Armezon Pro", "Basagran 5L", "Beyond Xtra", "Caramba", "Distinct", "Headline Amp"]
    PROGRAM_OWNERS = ["BASF", "Bayer", "Syngenta"]
    INCENTIVE_TYPES = ["Fixed % Rebate", "Volume Discount", "Cash Rebate"]
    PAID_ON_OPTIONS = ["Net Purchases", "Gross Sales", "Unit Volume"]

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
            "Incentives": [
                {
                    "Name": "Q1 Rebate",
                    "Region": None,
                    "Incentive Type": "Fixed % Rebate",
                    "Amount": "1%",
                    "Paid On": "Net Purchases",
                    "Products": ["Armezon Pro"]
                },
                {
                    "Name": "Q2 Growth Incentive",
                    "Region": "Midwest",
                    "Incentive Type": "Volume Discount",
                    "Amount": "500",
                    "Paid On": None,
                    "Products": ["Basagran 5L"]
                }
            ]
        }

        st.subheader("🔍 Extracted Program Details")
        program_form = st.form(key="program_form")
        with program_form:
            # Program details
            required_program_fields = ["Name", "Owner", "Start Date", "End Date", "Segment"]
            for field in required_program_fields:
                value = extracted_data["Program"][field]
                if field == "Owner":
                    # Show dropdown for Program Owner with validation
                    selected_owner = st.selectbox(
                        field,
                        PROGRAM_OWNERS,
                        index=PROGRAM_OWNERS.index(value) if value in PROGRAM_OWNERS else 0,
                        help="Required: Must match a system owner.",
                        key=f"program_{field}"
                    )
                    extracted_data["Program"][field] = selected_owner
                    if selected_owner in PROGRAM_OWNERS:
                        st.markdown(f":white_check_mark: Valid owner")
                else:
                    # Highlight empty required fields in red
                    label = f"{field} (Required)" if not value else field
                    style = "color: red;" if not value else ""
                    extracted_data["Program"][field] = st.text_input(
                        label,
                        value or "",
                        disabled=value is not None,
                        key=f"program_{field}",
                        help="Required" if not value else None
                    )
                    if not value:
                        st.markdown(f"<span style='{style}'>Please fill this field</span>", unsafe_allow_html=True)

            # Incentive details
            st.subheader("Incentives")
            required_incentive_fields = ["Name", "Region", "Incentive Type", "Amount", "Paid On"]
            for i, incentive in enumerate(extracted_data["Incentives"]):
                st.write(f"Incentive {i+1}")
                for field in required_incentive_fields:
                    value = incentive[field]
                    if field in ["Incentive Type", "Paid On"]:
                        # Show extracted value with validation checkmark
                        options = INCENTIVE_TYPES if field == "Incentive Type" else PAID_ON_OPTIONS
                        selected_value = st.selectbox(
                            f"{field} (Incentive {i+1})",
                            options,
                            index=options.index(value) if value in options else 0,
                            disabled=value is not None,
                            key=f"incentive_{i}_{field}"
                        )
                        incentive[field] = selected_value
                        if selected_value in options:
                            st.markdown(f":white_check_mark: Valid {field.lower()}")
                    else:
                        # Highlight empty required fields in red
                        label = f"{field} (Incentive {i+1}) (Required)" if not value else f"{field} (Incentive {i+1})"
                        style = "color: red;" if not value else ""
                        incentive[field] = st.text_input(
                            label,
                            value or "",
                            disabled=value is not None,
                            key=f"incentive_{i}_{field}",
                            help="Required" if not value else None
                        )
                        if not value:
                            st.markdown(f"<span style='{style}'>Please fill this field</span>", unsafe_allow_html=True)

                # Multi-select product mapping
                st.subheader(f"Product Mapping for Incentive {i+1}")
                selected_products = st.multiselect(
                    f"Select products for Incentive {i+1}",
                    PRODUCT_CATALOG,
                    default=[p for p in incentive["Products"] if p in PRODUCT_CATALOG],
                    key=f"products_{i}"
                )
                incentive["Products"] = selected_products if selected_products else []

            # Check if all required fields are filled
            all_fields_filled = (
                all(extracted_data["Program"][f] for f in required_program_fields) and
                extracted_data["Program"]["Owner"] in PROGRAM_OWNERS and
                all(all(incentive[f] for f in required_incentive_fields) for incentive in extracted_data["Incentives"]) and
                all(incentive["Incentive Type"] in INCENTIVE_TYPES for incentive in extracted_data["Incentives"]) and
                all(incentive["Paid On"] in PAID_ON_OPTIONS for incentive in extracted_data["Incentives"]) and
                all(len(incentive["Products"]) > 0 for incentive in extracted_data["Incentives"])
            )

            # Submit button, disabled until all fields are valid
            if st.form_submit_button("✅ Submit Program", disabled=not all_fields_filled):
                if all_fields_filled:
                    st.session_state.unverified_programs.append({
                        "Program": extracted_data["Program"],
                        "Incentives": extracted_data["Incentives"],
                        "Status": "Unverified"
                    })
                    st.success("🎉 Program submitted as Unverified.")
                    if st.button("🔙 Back to Programs"):
                        navigate_to("we_earn")
                else:
                    st.error("Please complete all required fields and ensure valid selections.")

    else:
        if st.button("🔙 Back to Programs"):
            navigate_to("we_earn")