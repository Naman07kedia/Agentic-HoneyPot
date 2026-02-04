import requests
from app.config import GUVI_CALLBACK_URL


def send_final_callback(session_id, session):
    payload = {
        "sessionId": session_id,
        "scamDetected": session["scamDetected"],
        "totalMessagesExchanged": session["totalMessages"],
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Scammer used urgency and payment redirection tactics"
    }

    try:
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)

        if response.status_code != 200:
            print("GUVI callback failed:", response.text)

    except Exception as e:
        print("GUVI callback unreachable:", e)
