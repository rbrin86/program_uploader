import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "we_earn"

# Navigation handler
def navigate_to(page):
    st.session_state.page = page

# Page router
if st.session_state.page == "we_earn":
    from we_earn import render_we_earn
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    from program_upload import render_program_upload
    render_program_upload(navigate_to)
