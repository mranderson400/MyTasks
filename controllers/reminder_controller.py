from config.database import tasks_collection, users_collection
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def check_and_send_reminders():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"🔍 Looking for tasks due on {today}...")

    users = users_collection.find()
    for user in users:
        user_id = user["_id"]
        email = user.get("email")
        print(f"👤 Checking user: {email} (ID: {user_id})")

        tasks = tasks_collection.find({
            "user_id": ObjectId(user_id),
            "due_date": today
        })

        tasks_found = False
        for task in tasks:
            tasks_found = True
            subject = f"Task Reminder: {task['title']}"
            body = f"Hi {user.get('first_name', 'there')},\n\nYou have a task due today: {task['title']}.\n\nDescription: {task['description']}\nStatus: {task['status']}\nDue Date: {task['due_date']}"
            print(f"📧 Sending email to {email} for task: {task['title']}")
            send_email(email, subject, body)

        if not tasks_found:
            print(f"📭 No tasks due today for {email}")

if __name__ == "__main__":
    check_and_send_reminders()
