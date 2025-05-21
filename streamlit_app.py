import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload
from program_details import render_program_details
from content_queue import render_content_queue  # Manufacturer only

# --- Role-based state management ---
if "role" not in st.session_state:
    st.session_state.role = "Receiver"  # Default role

# Set initial landing page based on role
if "page" not in st.session_state:
    st.session_state.page = "we_earn" if st.session_state.role == "Receiver" else "content_queue"

# Check if role was changed, and reset page accordingly
previous_role = st.session_state.get("previous_role")
if previous_role and previous_role != st.session_state.role:
    st.session_state.page = "we_earn" if st.session_state.role == "Receiver" else "content_queue"
st.session_state.previous_role = st.session_state.role

if "selected_program" not in st.session_state:
    st.session_state.selected_program = None

# --- Sidebar UI ---
st.sidebar.title("🧭 Navigation")
st.sidebar.radio("Select Role", ["Receiver", "Manufacturer"], key="role", horizontal=True)

# --- Role-based menu definitions ---
receiver_pages = {
    "we_earn": "📊 Programs – We Earn",
}

manufacturer_pages = {
    "content_queue": "📥 Review Unverified Programs",
    # "program_upload": "➕ Create Program",  # Enable later if needed
}

visible_pages = receiver_pages if st.session_state.role == "Receiver" else manufacturer_pages
hidden_pages = ["program_details"]

# --- Sidebar Menu Navigation ---
for page_key, page_label in visible_pages.items():
    if st.sidebar.button(page_label, key=f"nav_{page_key}"):
        st.session_state.page = page_key
        st.session_state.selected_program = None
        st.rerun()

# Show indicator if on a hidden/internal page like program_details
if st.session_state.page in hidden_pages:
    st.sidebar.markdown(f"**Viewing:** Program Details")

# --- Page Routing ---
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
elif st.session_state.page == "content_queue":
    render_content_queue(lambda page, program=None: (
        st.session_state.update({"page": page, "selected_program": program}),
        st.rerun()
    ))
elif st.session_state.page == "program_details":
    render_program_details(lambda page, program=None: (
        st.session_state.update({"page": page, "selected_program": program}),
        st.rerun()
    ))
