import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pytz

FLAG_FILE = "done.txt"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://results.puexam.in"

TARGET_TEXT = "Master of Engineering Civil Engineering (Construction Technology and Management) 7th Spell Examination, 2025"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def send_document(file_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    requests.post(url, data={"chat_id": CHAT_ID, "document": file_url})


def is_within_time():
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()

    start = datetime.strptime("09:30", "%H:%M").time()
    end = datetime.strptime("20:00", "%H:%M").time()

    return start <= now <= end


def check_result():
    print("Checking...")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        for link in links:
            text = link.get_text(strip=True)

            if TARGET_TEXT.lower() in text.lower() and "december 2025" in text.lower():
                pdf_url = link.get("href")

                if not pdf_url.startswith("http"):
                    pdf_url = URL + "/" + pdf_url.lstrip("/")

                send_message("🎉 RESULT DECLARED!")
                send_document(pdf_url)

                return True

        print("Not found")
        return False

    except Exception as e:
        print("Error:", e)
        return False


if __name__ == "__main__":
    if is_within_time():
        check_result()
    else:
        print("Outside time")