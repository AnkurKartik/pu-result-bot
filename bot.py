import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://results.puexam.in"

TARGET_TEXT = "Master of Engineering Civil Engineering (Construction Technology and Management) 7th Spell Examination, 2025"

CHECK_INTERVAL = 300
START_TIME = "09:30"
END_TIME = "20:00"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def send_document(file_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    requests.post(url, data={"chat_id": CHAT_ID, "document": file_url})


def is_within_time():
    now = datetime.now().time()
    start = datetime.strptime(START_TIME, "%H:%M").time()
    end = datetime.strptime(END_TIME, "%H:%M").time()
    return start <= now <= end


def check_result():
    print("Checking...")

    try:
        response = requests.get(URL, timeout=10)
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
    send_message("🤖 Bot started")

    while True:
        if is_within_time():
            found = check_result()
            if found:
                send_message("✅ Done")
                break
        else:
            print("Outside time")

        time.sleep(CHECK_INTERVAL)