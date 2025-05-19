import streamlit as st
import sqlite3
import pandas as pd

def render_content_queue(navigate_to):
    st.title("📋 Content Team Queue")

    conn = sqlite3.connect("programs.db")
    c = conn.cursor()

    # Fetch unverified programs
    c.execute("SELECT id, name, owner, segment, status FROM Programs WHERE status IN ('Unverified', 'In Review')")
    programs = pd.DataFrame(c.fetchall(), columns=["ID", "Name", "Owner", "Segment", "Status"])

    st.dataframe(programs, use_container_width=True)

    # Filter by program ID for review
    program_id = st.number_input("Enter Program ID to Review", min_value=1, step=1)
    if program_id:
        c.execute("SELECT * FROM Programs WHERE id = ?", (program_id,))
        program = c.fetchone()
        if program:
            st.subheader(f"Review Program: {program[1]}")
            status = st.selectbox("Status", ["Unverified", "In Review", "Verified", "Rejected"])
            feedback = st.text_area("Feedback (if Rejected)")
            if st.button("Save Changes"):
                c.execute("UPDATE Programs SET status = ?, feedback = ? WHERE id = ?", (status, feedback, program_id))
                conn.commit()
                st.success("Changes saved.")
                if status == "Verified":
                    st.write("Program published as live.")

    conn.close()
    if st.button("🔙 Back to Programs"):
        navigate_to("we_earn")