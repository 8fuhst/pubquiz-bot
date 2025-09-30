#!/usr/bin/env python3

import logging
import os
import requests as r
import schedule
import sys

from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Redirect logging to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Starting bot...")

# Load config and set constants
load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
PUB_PHONE_NUMBER = os.getenv("PUB_PHONE_NUMBER")
POLL_TIME = os.getenv("POLL_TIME")
CHECK_TIME = os.getenv("CHECK_TIME")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_poll():
    resp = r.post(URL + "sendPoll", json={
        "chat_id": CHAT_ID, 
        "question": "Bist du heute beim Pubquiz dabei?",
        "options": [
            "Ja",
            "Nein"
        ],
        "is_anonymous": False
    }, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        logger.error(f"Failed to send poll: {resp.text}")
    else:
        logger.info("Poll sent successfully")

def check_answers():
    # Get updates
    resp = r.post(URL + "getUpdates")
    if resp.status_code != 200:
        logger.error(f"Failed to get updates: {resp.text}")
    
    # Check which users want to participate in the quiz
    appearing = []
    count = 0
    for answer in resp.json().get("result"):
        if "poll_answer" in answer.keys():
            if answer["poll_answer"]["option_ids"] == [0]:
                count += 1
                if "username" in answer["poll_answer"]["user"].keys():
                    appearing.append(answer["poll_answer"]["user"]["username"])
    if count > 2:
        resp = r.post(URL + "sendMessage", json={
            "chat_id": CHAT_ID,
            "text": "Cool! Scheint so als wenn ihr genug fürs Quiz seid. Viel Spaß!"
        }, headers={"Content-Type": "application/json"})
    elif count > 0:
        text = f"Hm, das sind wenige Meldungen für heute. Sagt bitte telefonisch ab wenn ihr nicht kommt! Die Telefonnummer ist {PUB_PHONE_NUMBER}."
        for username in appearing:
            text += (f" @{username}")
    else:
        text = f"Anscheinend hat sich für heute niemand gemeldet :( Denkt dran, dass wer anruft und absagt! Die Telefonnummer ist {PUB_PHONE_NUMBER}. Meldet euch bitte kurz wenn ihr das getan habt."
    resp = r.post(URL + "sendMessage", json={
        "chat_id": CHAT_ID,
        "text": text
    }, headers={"Content-Type": "application/json"})
    logger.info("Parsed answers successfully")

def main() -> None:
    """Run the bot to send messages regularly."""
    logger.info("Starting bot...")
    schedule.every().monday.at(POLL_TIME).do(send_poll)
    schedule.every().monday.at(CHECK_TIME).do(check_answers)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()