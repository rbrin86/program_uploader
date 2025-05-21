import streamlit as st
from we_earn import render_we_earn
from program_upload import render_program_upload
from program_details import render_program_details
from content_queue import render_content_queue  # Optional: only shown for Manufacturer role

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "we_earn"
if "selected_program" not in st.session_state:
    st.session_state.selected_program = None
if "role" not in st.session_state:
    st.session_state.role = "Receiver"  # Default role

# --- Sidebar Role Selector ---
st.sidebar.title("🧭 Navigation")
st.sidebar.radio("Select Role", ["Receiver", "Manufacturer"], key="role", horizontal=True)

# --- Define menus for each role ---
receiver_pages = {
    "we_earn": "📊 Programs – We Earn",
    # Future receiver-specific options
}

manufacturer_pages = {
    "content_queue": "📥 Review Unverified Programs",
    # Future manufacturer-specific options
}

# --- Combine visible pages based on role ---
visible_pages = receiver_pages if st.session_state.role == "Receiver" else manufacturer_pages
hidden_pages = ["program_details"]

# --- Sidebar Menu ---
for key, label in visible_pages.items():
    if st.sidebar.button(label, key=f"nav_{key}"):
        st.session_state.page = key
        st.session_state.selected_program = None
        st.rerun()

# Show label for hidden/internal pages
if st.session_state.page in hidden_pages:
    st.sidebar.markdown(f"**Viewing:** Program Details")

# --- Render Pages ---
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
