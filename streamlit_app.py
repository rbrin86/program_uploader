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

# Debug: Display session state in sidebar
st.sidebar.title("Navigation")
st.sidebar.write(f"Debug: Current page: {st.session_state.page}")
st.sidebar.write(f"Debug: Selected program: {st.session_state.selected_program}")

# Navigation sidebar
page_options = ["we_earn", "program_upload", "content_queue"]
default_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
selected_page = st.sidebar.selectbox("Go to", page_options, index=default_index)

# Update page state if changed
if selected_page != st.session_state.page:
    st.write(f"Debug: Sidebar navigation to {selected_page}")
    st.session_state.page = selected_page
    st.session_state.selected_program = None  # Reset on page change
    st.rerun()

# Render the selected page
st.write(f"Debug: Rendering page: {st.session_state.page}")
if st.session_state.page == "we_earn":
    render_we_earn(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "program_upload":
    render_program_upload(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "content_queue":
    render_content_queue(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))
elif st.session_state.page == "program_details":
    render_program_details(lambda page, program=None: (st.session_state.update({"page": page, "selected_program": program}), st.rerun()))