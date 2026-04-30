from datetime import datetime, date
import os
from dotenv import load_dotenv
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Set up url link
api_key = os.getenv("API_KEY")
topic = "tesla"
target_url = (
    "https://newsapi.org/v2/everything"
    f"?q={topic}"
    "&from=2026-03-30"
    "&sortBy=publishedAt"
    f"&apiKey={api_key}"
    "&language=en"
)

# Hit the API
response = requests.get(target_url)
content = response.json()

# Format the message
message_content = ""
for item in content["articles"][:5]:
    date_obj = datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    message_content += (
        f"Published at: {date_obj.year}/{date_obj.month}/{date_obj.day}\n"
        f"Title: {item["title"]}\n"
        f"Description: {item["description"]}\n"
        f"url: {item["url"]}\n\n"
    )

# Preparing to send the message
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("SENDER_PASSWORD")

message = MIMEMultipart("alternative")
message["Subject"] = f"Python News on {date.today()}"
message["From"] = sender_email
message["To"] = receiver_email
message.attach(MIMEText(message_content, "plain"))


context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.send_message(message)
