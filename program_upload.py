import streamlit as st
from pdfminer.high_level import extract_text
import re

# -------------------
# Utils for extraction
# -------------------
def extract_program_info(text):
    program = {
        "Program Name": extract_field(text, r"Program Name[:\s]+(.+?)\n"),
        "Program Owner": extract_field(text, r"Program Owner[:\s]+(.+?)\n"),
        "Start Date": extract_field(text, r"Start Date[:\s]+(.+?)\n"),
        "End Date": extract_field(text, r"End Date[:\s]+(.+?)\n"),
        "Segment": extract_field(text, r"Segment[:\s]+(.+?)\n"),
        "Region": extract_field(text, r"Region[:\s]+(.+?)\n")
    }
    return program

def extract_incentives(text):
    incentives = []
    blocks = re.split(r"(?i)Incentive Name[:\s]", text)[1:]  # naive split
    for block in blocks:
        fields = {
            "Incentive Name": block.split('\n')[0].strip(),
            "Region": extract_field(block, r"Region[:\s]+(.+?)\n"),
            "Incentive Type": extract_field(block, r"Type[:\s]+(.+?)\n"),
            "Amount": extract_field(block, r"Amount[:\s\$%]+([\d\.,]+)")
        }
        incentives.append(fields)
    return incentives

def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

# -------------------
# Streamlit App
# -------------------
def main():
    st.title("Program Upload")
    st.markdown("Upload a Program PDF to extract both Program details and Incentives")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        text = extract_text(uploaded_file)
        program_info = extract_program_info(text)
        incentives = extract_incentives(text)

        st.subheader("Program Details")
        for field, value in program_info.items():
            st.text_input(field, value)

        st.subheader("Incentives")
        for i, inc in enumerate(incentives):
            with st.expander(f"Incentive {i+1}: {inc['Incentive Name']}"):
                for field, value in inc.items():
                    st.text_input(f"{field} (Incentive {i+1})", value)

        st.subheader("Missing Fields")
        missing = []
        for field, value in program_info.items():
            if not value:
                missing.append(field)
        for i, inc in enumerate(incentives):
            for field, value in inc.items():
                if not value:
                    missing.append(f"{field} in Incentive {i+1}")

        if missing:
            st.warning("Missing Fields:")
            for field in missing:
                st.write(f"- {field}")

        if st.button("Submit Program"):
            st.success("Program and incentives submitted successfully (simulated)")

if __name__ == "__main__":
    main()
