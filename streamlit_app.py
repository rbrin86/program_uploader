import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload  # Kept in case needed later
from program_details import render_program_details

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "selected_program" not in st.session_state:
    st.session_state.selected_program = None

# Define available pages
visible_pages = {
    "we_earn": "📊 Programs – We Earn",
    # Future pages can be added here
    # "program_upload": "➕ Create Program",
    # "content_queue": "📥 Review Queue",
}
hidden_pages = ["program_details"]

# Sidebar Navigation (Menu-style)
st.sidebar.title("🧭 Menu")

for key, label in visible_pages.items():
    if st.sidebar.button(label, key=f"nav_{key}"):
        st.session_state.page = key
        st.session_state.selected_program = None
        st.rerun()

# Show page label if on a hidden route like program_details
if st.session_state.page in hidden_pages:
    st.sidebar.markdown(f"**Viewing:** Program Details")

# Render the current page
if st.session_state.page == "we_earn":
    render_we_earn(lambda page, program=None: (
        st.session_state.update({"page": page, "selected_program": program}),
        st.rerun()
    ))
elif st.session_state.page == "program_upload":
    render_program_upload(lambda page, program=None: (
        st.session_state.update({"page": page, "selected_program": program}),
        st.rerun()
    ))
elif st.session_state.page == "program_details":
    render_program_details(lambda page, program=None: (
        st.session_state.update({"page": page, "selected_program": program}),
        st.rerun()
    ))
