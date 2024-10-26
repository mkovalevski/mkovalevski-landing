import smtplib
import ssl
import os

from flask import Blueprint, render_template, request, redirect, url_for
from cryptography.fernet import Fernet

main = Blueprint('main', __name__)

key = os.getenv("SECRET_KEY").encode()
cipher_suite = Fernet(key)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/submit_form", methods=["POST"])
def submit_form():
    name = request.form.get("name").encode('utf-8')
    email = request.form.get("email").encode('utf-8')
    message = request.form.get("message").encode('utf-8')
    send_email(name, email, message)
    return redirect(url_for("main.home"))

def send_email(name, email, message):
    sender_email = cipher_suite.decrypt(os.getenv("EMAIL_USER").encode()).decode()
    receiver_email = cipher_suite.decrypt(os.getenv("EMAIL_RECEIVER").encode()).decode()
    password = cipher_suite.decrypt(os.getenv("EMAIL_PASS").encode()).decode()
    subject = f"New message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    email_text = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_text)
