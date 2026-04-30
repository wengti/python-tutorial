from datetime import datetime, date
import os
from dotenv import load_dotenv
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.chat_models import init_chat_model

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

# Hit the news API
response = requests.get(target_url)
content = response.json()

# Format the message for AI
message_content = ""
for item in content["articles"][:5]:
    date_obj = datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    message_content += (
        f"Title: {item["title"]}\n" f"Description: {item["description"]}\n\n"
    )


# Send the message to AI
model = init_chat_model(model="gemini-3-flash-preview", model_provider="google_genai")
conversation = [
    {
        "role": "system",
        "content": "You are a helpful and friendly assistant that summarizes news. Provide a short paragraph of about 100 words to sum up the news provided by the user.",
    },
    {
        "role": "user",
        "content": message_content,
    },
]
response = model.invoke(conversation)
ai_summary = response.content[0]["text"]

# Preparing to send the email
email_content = "AI Summary: \n" f"{ai_summary}\n\n" "Sources: \n" f"{message_content}"


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("SENDER_PASSWORD")

message = MIMEMultipart("alternative")
message["Subject"] = f"Python News on {date.today()}"
message["From"] = sender_email
message["To"] = receiver_email
message.attach(MIMEText(email_content, "plain"))


context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.send_message(message)
