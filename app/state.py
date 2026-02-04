'''from datetime import datetime
from typing import Dict, List


class ConversationState:
    def __init__(self):
        self.started_at = datetime.utcnow()
        self.total_turns = 0
        self.agent_turns = 0
        self.scam_detected = False
        self.scam_confidence = 0.0
        self.agent_engaged = False
        self.messages = []

        self.extracted_intelligence = {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }


conversation_store: Dict[str, ConversationState] = {}


def get_conversation(conversation_id: str) -> ConversationState:
    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = ConversationState()
    return conversation_store[conversation_id]


def update_turn(conversation: ConversationState, sender: str):
    conversation.total_turns += 1
    if sender == "agent":
        conversation.agent_turns += 1


def record_message(conversation: ConversationState, sender: str, message: str):
    conversation.messages.append({
        "sender": sender,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })


def engagement_duration_seconds(conversation: ConversationState) -> int:
    return int((datetime.utcnow() - conversation.started_at).total_seconds())


def add_intelligence(conversation: ConversationState, new_data: dict):
    for key in conversation.extracted_intelligence:
        conversation.extracted_intelligence[key].extend(new_data.get(key, []))'''

from datetime import datetime

sessions = {}

session_store = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "startedAt": datetime.utcnow(),
            "scamDetected": False,
            "confidence": 0.0,
            "callbackSent": False,
            "totalMessages": 0,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    sessions[session_id]["totalMessages"] += 1
    return sessions[session_id]


def update_session(session, extracted):
    for k in session["intelligence"]:
        for item in extracted.get(k, []):
            if item not in session["intelligence"][k]:
                session["intelligence"][k].append(item)

