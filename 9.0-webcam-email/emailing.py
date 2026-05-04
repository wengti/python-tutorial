from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from glob import glob
import os
import smtplib
import ssl

from dotenv import load_dotenv

load_dotenv()


def send_email():
    subject = "[Python Object Detector] An object has been detected."
    body = "Python Object Detector has detected an object."
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("PASSWORD")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Find the file to be sent
    all_images_paths = glob("images/*.png")
    selected_idx = int(len(all_images_paths) / 2)
    selected_image_path = all_images_paths[selected_idx]

    # Open image file in binary mode
    with open(selected_image_path, "rb") as attachment:
        part = MIMEImage(attachment.read(), _subtype="png")

    # Attach the file to be sent
    message.attach(part)

    # Send the email
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    # Clear the folder after email is sent successfully
    for path in all_images_paths:
        if os.path.exists(path):
            os.remove(path)
