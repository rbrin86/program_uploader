import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "rerun_requested" not in st.session_state:
    st.session_state.rerun_requested = False

def navigate_to(page):
    st.session_state.page = page
    st.session_state.rerun_requested = True

# Render the appropriate page
if st.session_state.page == "we_earn":
    from we_earn import render_we_earn
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    from program_upload import render_program_upload
    render_program_upload(navigate_to)

# Now conditionally rerun, then reset flag
if st.session_state.rerun_requested:
    st.session_state.rerun_requested = False
    st.experimental_rerun()
