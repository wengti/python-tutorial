from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
import time

from dotenv import load_dotenv
from selectorlib import Extractor
import requests
import sqlite3
import uuid

# load environment variables
load_dotenv()

# URL to be scraped
URL = "https://programmer100.pythonanywhere.com/tours/"

# Extractor instance
YAML_FILE = "Tours.yml"
extractor = Extractor.from_yaml_file(YAML_FILE)

# Connection to database
DATABASE_NAME = "scraped_entries.db"
con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()


# Scrape
def scrape(url: str) -> str:
    try:
        response = requests.get(url)
        if response.raise_for_status() is not None:
            raise response.raise_for_status()
        data = extractor.extract(response.text)["data"]
        return data
    except requests.exceptions.HTTPError as error:
        print(f"Error: {error.response.status_code} | {error.response.reason}")
        return ""


# Store data
def db_store(data) -> None:
    entry_id = uuid.uuid4()
    inserted_data = (str(entry_id), *data)

    cur.execute("INSERT INTO scraped_entries VALUES(?, ?, ?, ?)", inserted_data)
    con.commit()
    return None


# Read data
def db_read(data: tuple[str, str, str]) -> list[tuple[str, str, str]]:
    cur.execute(
        "SELECT * FROM scraped_entries WHERE band = ? AND city = ? AND date = ?", data
    )
    return cur.fetchall()


# Send email
def send_email(data: tuple[str, str, str]):

    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Python Scraper] New entries"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"New entries: {data[0]}, {data[1]}, {data[2]}"
    message.attach(MIMEText(text, "plain"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


try:
    while True:
        scraped_data = scrape(URL)
        print(scraped_data)
        if scraped_data and scraped_data != "No upcoming tours":
            scraped_data = tuple(entry.strip() for entry in scraped_data.split(","))

            if not db_read(scraped_data):
                db_store(scraped_data)
                send_email(scraped_data)
        time.sleep(2)
except KeyboardInterrupt:
    con.close()
