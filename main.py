import streamlit as st
from models import Student, Session, engine
from utils import update_fee_status, get_student, send_notification, import_students_from_excel

Session.configure(bind=engine)

st.title("Student Fee Tracking System")

# Upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file with student data", type="xlsx")

if uploaded_file:
    with Session() as session:
        if import_students_from_excel(session, uploaded_file):
            st.write("Students data has been imported/updated successfully.")
        else:
            st.error("Failed to import or update student data. Check for duplicate emails or data issues.")

# Update fee form
with st.form("student_fee"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    amount_paid = st.number_input("Amount Paid", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Update Fee")

    if submitted:
        with Session() as session:
            if update_fee_status(session, student_id, amount_paid):
                st.success(f"Fee updated successfully for student ID: {student_id}")
                student = get_student(session, student_id)
                if student:
                    st.write(f"Notification would be sent: Payment of ${amount_paid} received. Remaining due: ${student.fee_due}")
                    # Uncomment the following line when you have email setup configured
                    # send_notification(student.email, f"Payment of ${amount_paid} received. Remaining due: ${student.fee_due}")
            else:
                st.error("Failed to update fee. Check student ID.")
