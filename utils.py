import smtplib
from email.mime.text import MIMEText
from models import Student, Session
from datetime import datetime
from openpyxl import load_workbook  # Added for Excel handling

def update_fee_status(session, student_id, amount_paid):
    student = session.query(Student).get(student_id)
    if student:
        student.fee_due -= amount_paid
        student.last_payment = datetime.now()
        student.is_paid = student.fee_due <= 0
        session.commit()
        return True
    return False

def get_student(session, student_id):
    return session.query(Student).get(student_id)

def send_notification(student_email, message):
    msg = MIMEText(message)
    msg['Subject'] = "Fee Notification"
    msg['From'] = "your-email@example.com"
    msg['To'] = student_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-password")  # Use env variables in production
            server.send_message(msg)
        print("Successfully sent email")
    except Exception as e:
        print(f"Failed to send email: {e}")

def import_students_from_excel(session, file_path):
    wb = load_workbook(filename=file_path)
    sheet = wb.active
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming header in row 1
        if all(row):  # Check if any cell in the row is not empty
            name, email, fee_due = row[:3]  # Assuming these are the first three columns
            new_student = Student(name=name, email=email, fee_due=fee_due)
            session.add(new_student)
    session.commit()
    return True
