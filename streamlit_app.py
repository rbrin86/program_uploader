import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload
from content_queue import render_content_queue
from program_details import render_program_details

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "selected_program" not in st.session_state:
    st.session_state.selected_program = None

# Navigation sidebar
visible_pages = ["we_earn", "program_upload", "content_queue"]
page_options = visible_pages + ["program_details"]

selected_page = st.sidebar.selectbox("Go to", visible_pages, index=visible_pages.index(st.session_state.page) if st.session_state.page in visible_pages else 0)

default_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0

# Update page state if changed
if selected_page != st.session_state.page:
    st.write(f"Debug: Sidebar navigation to {selected_page}")
    st.session_state.page = selected_page
    st.session_state.selected_program = None  # Reset on page change
    st.rerun()

# Render the selected page
if st.session_state.page == "we_earn":
    render_we_earn(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "program_upload":
    render_program_upload(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "content_queue":
    render_content_queue(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "program_details":
    render_program_details(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))