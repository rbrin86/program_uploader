import streamlit as st
import sqlite3
from fuzzywuzzy import fuzz  # For product matching

def render_program_upload(navigate_to):
    st.title("📤 Upload Unverified Program")

    # Database connection
    conn = sqlite3.connect("programs.db")
    c = conn.cursor()

    uploaded_file = st.file_uploader("Upload a PDF of your rebate program", type="pdf")

    if uploaded_file:
        st.success("✅ File uploaded successfully. Extracting program details...")

        # Simulated OCR extraction (replace with actual OCR logic)
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
                    "Products": ["Acme Fertilizer 123"]
                }
            ]
        }

        st.subheader("🔍 Extracted Program Details")
        program_form = st.form(key="program_form")
        with program_form:
            for field, value in extracted_data["Program"].items():
                extracted_data["Program"][field] = st.text_input(field, value or "", disabled=value is not None)
            st.subheader("Incentives")
            for i, incentive in enumerate(extracted_data["Incentives"]):
                st.write(f"Incentive {i+1}")
                for field, value in incentive.items():
                    if field != "Products":
                        incentive[field] = st.text_input(f"{field} (Incentive {i+1})", value or "", disabled=value is not None)
                st.subheader(f"Product Mapping for Incentive {i+1}")
                for product in incentive["Products"]:
                    # Simulated master catalog
                    catalog = ["Acme Fert 123-A", "Acme Fert 123-B", "Acme Seed 456"]
                    match = max(catalog, key=lambda x: fuzz.ratio(x.lower(), product.lower()), default=None)
                    selected_product = st.selectbox(f"Map '{product}'", ["Unmapped"] + catalog, index=catalog.index(match) + 1 if match else 0)
                    incentive["Products"][incentive["Products"].index(product)] = selected_product if selected_product != "Unmapped" else None

            if st.form_submit_button("✅ Submit Program"):
                missing_fields = [f for f, v in extracted_data["Program"].items() if not v] + \
                                [f for i in extracted_data["Incentives"] for f, v in i.items() if f != "Products" and not v] + \
                                [p for i in extracted_data["Incentives"] for p in i["Products"] if not p]
                if missing_fields:
                    st.error(f"Please complete missing fields: {', '.join(missing_fields)}")
                else:
                    # Save to database
                    c.execute("INSERT INTO Programs (name, owner, start_date, end_date, segment, status) VALUES (?, ?, ?, ?, ?, ?)",
                              (extracted_data["Program"]["Name"], extracted_data["Program"]["Owner"],
                               extracted_data["Program"]["Start Date"], extracted_data["Program"]["End Date"],
                               extracted_data["Program"]["Segment"], "Unverified"))
                    program_id = c.lastrowid
                    for incentive in extracted_data["Incentives"]:
                        c.execute("INSERT INTO Incentives (program_id, name, region, type, amount, paid_on) VALUES (?, ?, ?, ?, ?, ?)",
                                  (program_id, incentive["Name"], incentive["Region"], incentive["Incentive Type"],
                                   incentive["Amount"], incentive["Paid On"]))
                        incentive_id = c.lastrowid
                        for product in incentive["Products"]:
                            c.execute("INSERT INTO ProductMappings (incentive_id, extracted_name, mapped_product) VALUES (?, ?, ?)",
                                      (incentive_id, product or "", product or ""))
                    conn.commit()
                    st.success("🎉 Program submitted as Unverified.")
                    if st.button("🔙 Back to Programs"):
                        navigate_to("we_earn")

    conn.close()
    if st.button("🔙 Back to Programs"):
        navigate_to("we_earn")