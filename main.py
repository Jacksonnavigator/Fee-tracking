import streamlit as st
from models import Student, Session
from utils import update_fee_status, get_student, send_notification
from sqlalchemy import create_engine

# Setup database connection
engine = create_engine('sqlite:///students.db')
Session.configure(bind=engine)

st.title("Student Fee Tracking System")

# Example of Streamlit form
with st.form("student_fee"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    amount_paid = st.number_input("Amount Paid", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Update Fee")

    if submitted:
        if update_fee_status(student_id, amount_paid):
            st.success(f"Fee updated successfully for student ID: {student_id}")
            student = get_student(student_id)
            if student:
                send_notification(student.email, f"Payment of ${amount_paid} received. Remaining due: ${student.fee_due}")
        else:
            st.error("Failed to update fee. Check student ID.")

# Additional features like adding new students, viewing all students etc. can be added here.
