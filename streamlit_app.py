import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload
from content_queue import render_content_queue  # New import

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "we_earn"

# Navigation sidebar
st.sidebar.title("Navigation")
page_options = ["we_earn", "program_upload", "content_queue"]  # Added content_queue
selected_page = st.sidebar.selectbox("Go to", page_options, index=page_options.index(st.session_state.page))

# Function to navigate between pages
def navigate_to(page):
    st.session_state.page = page
    st.experimental_rerun()

# Render the selected page
if st.session_state.page == "we_earn":
    render_we_earn(navigate_to)
elif st.session_state.page == "program_upload":
    render_program_upload(navigate_to)
elif st.session_state.page == "content_queue":
    render_content_queue(navigate_to)