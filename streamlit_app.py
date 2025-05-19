import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload
from content_queue import render_content_queue
from program_details import render_program_details  # New import

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "we_earn"

# Initialize selected program state
if "selected_program" not in st.session_state:
    st.session_state.selected_program = None

# Navigation sidebar
st.sidebar.title("Navigation")
page_options = ["we_earn", "program_upload", "content_queue", "program_details"]  # Added program_details
selected_page = st.sidebar.selectbox("Go to", page_options, index=page_options.index(st.session_state.page))

# Update page state if the selection changes
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# Function to navigate between pages
def navigate_to(page, program=None):
    st.session_state.page = page
    st.session_state.selected_program = program
    st.rerun()

# Render the selected page
if st.session_state.page == "we_earn":
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    render_program_upload(navigate_to)
elif st.session_state.page == "content_queue":
    render_content_queue(navigate_to)
elif st.session_state.page == "program_details":
    render_program_details(navigate_to)