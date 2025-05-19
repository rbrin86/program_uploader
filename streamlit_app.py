import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "do_rerun" not in st.session_state:
    st.session_state.do_rerun = False

def navigate_to(page):
    st.session_state.page = page
    st.session_state.do_rerun = True

# Render pages
if st.session_state.page == "we_earn":
    from we_earn import render_we_earn
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    from program_upload import render_program_upload
    render_program_upload(navigate_to)

# Call rerun only if flagged, and then clear the flag
if st.session_state.do_rerun:
    st.session_state.do_rerun = False
    st.experimental_rerun()
