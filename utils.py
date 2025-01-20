import smtplib
from email.mime.text import MIMEText

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
    # Note: Use environment variables for email credentials in production
    msg = MIMEText(message)
    msg['Subject'] = "Fee Notification"
    msg['From'] = "your-email@example.com"
    msg['To'] = student_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-password")  # Use environment variables in production
            server.send_message(msg)
        print("Successfully sent email")
    except Exception as e:
        print(f"Failed to send email: {e}")
