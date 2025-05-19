import streamlit as st
import pandas as pd
import pdfplumber

# Session state to manage page transitions
if "page" not in st.session_state:
    st.session_state.page = "we_earn"

# Dummy data for "We Earn" page
data = pd.DataFrame([
    {"Program Name": "2025 Growth Rebate", "Program Owner": "CropStrong", "Segment": "Ag Chem", "Earnings $": 24000, "Earnings %": 12, "Year": 2025, "Originator": "Published by Supplier"},
    {"Program Name": "Seed Launch Bonus", "Program Owner": "GrowPro", "Segment": "Seed", "Earnings $": 15000, "Earnings %": 8, "Year": 2025, "Originator": "Created by My Org"},
    {"Program Name": "Promarket Winter Promo", "Program Owner": "CropStrong", "Segment": "Promarket", "Earnings $": 8000, "Earnings %": 5, "Year": 2024, "Originator": "Published by Supplier"},
])

# ---- PAGE: We Earn ----
if st.session_state.page == "we_earn":
    st.title("We Earn")
    st.markdown("View and manage your active rebate programs.")

    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("➕ Create Program"):
            st.session_state.page = "upload"
            st.experimental_rerun()

    with st.expander("🔍 Filters"):
        search = st.text_input("Search Program Name")
        year = st.selectbox("Program Year", options=[None, 2025, 2024])
        segment = st.selectbox("Segment", options=[None, "Ag Chem", "Seed", "Promarket", "Fertilizer", "Seed Treatment"])
        owner = st.selectbox("Program Owner", options=[None] + sorted(data["Program Owner"].unique()))
        origin = st.selectbox("Originator", options=[None, "Published by Supplier", "Created by My Org"])

    df = data.copy()
    if search:
        df = df[df["Program Name"].str.contains(search, case=False)]
    if year:
        df = df[df["Year"] == year]
    if segment:
        df = df[df["Segment"] == segment]
    if owner:
        df = df[df["Program Owner"] == owner]
    if origin:
        df = df[df["Originator"] == origin]

    st.dataframe(df[["Program Name", "Program Owner", "Segment", "Earnings $", "Earnings %"]], use_container_width=True)

# ---- PAGE: Upload PDF and Extract ----
elif st.session_state.page == "upload":
    st.title("Create Unverified Program")
    st.markdown("Upload a PDF to extract program details.")

    uploaded_file = st.file_uploader("Upload rebate program PDF", type="pdf")
    extracted_text = ""

    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        st.success("✅ Extracted text from PDF.")
        st.text_area("📄 Raw Extracted Text", extracted_text, height=300)

        # Simulate parsing values
        st.subheader("📝 Review Extracted Fields")
        program_name = st.text_input("Program Name", value="(try pulling from PDF text)")
        program_owner = st.text_input("Program Owner", value="(e.g., CropStrong)")
        segment = st.selectbox("Segment", options=["Ag Chem", "Seed", "Promarket", "Fertilizer", "Seed Treatment"])
        year = st.selectbox("Program Year", options=[2024, 2025])
        region = st.text_input("Region", value="(Optional)")
        incentive = st.text_area("Incentive Details", value="(e.g., $5/unit if > 100 units)")

st.markdown("---")
if st.button("⬅️ Back to Programs"):
    st.session_state.page = "we_earn"
    st.experimental_rerun()

# Submit Button with Safe Rerun Handling
if st.button("✅ Submit Program"):
    st.session_state.page = "we_earn"
    st.session_state.show_success = True
    st.experimental_rerun()

# Show success message on return
if st.session_state.get("show_success"):
    st.success("✅ Program submitted as Unverified. It will now appear in your table.")
    st.session_state.show_success = False

