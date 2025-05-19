import streamlit as st

# Set up session state on first load
if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "do_rerun" not in st.session_state:
    st.session_state.do_rerun = False
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# Navigation helper
def navigate_to(page):
    st.session_state.page = page
    st.session_state.do_rerun = True

# Load appropriate page
if st.session_state.page == "we_earn":
    from we_earn import render_we_earn
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    from program_upload import render_program_upload
    render_program_upload(navigate_to)

# Safe rerun at the end
if st.session_state.do_rerun:
    st.session_state.do_rerun = False
    st.experimental_rerun()
