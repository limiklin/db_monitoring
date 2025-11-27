import requests
from config.settings import DOORAY_CONFIG

def send_dooray(message: str):
    payload = {
        "botName": "DB-Monitor",
        "text": message
    }

    try:
        resp = requests.post(DOORAY_CONFIG["webhook_url"], json=payload)
        resp.raise_for_status()
    except Exception as e:
        print("Dooray 전송 실패:", e)
