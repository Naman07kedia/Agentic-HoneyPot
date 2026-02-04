'''from app.state import conversation_store
from datetime import datetime

def summarize_conversation(conversation_id: str) -> dict:
    """
    Returns structured evaluation metrics for a conversation.
    """
    if conversation_id not in conversation_store:
        return {"error": "Conversation not found"}

    conv = conversation_store[conversation_id]

    # Unique intelligence counts
    unique_bank_accounts = len(set([b['value'] for b in conv.extracted_intelligence["bank_accounts"]]))
    unique_upi_ids = len(set([u['value'] for u in conv.extracted_intelligence["upi_ids"]]))
    unique_phishing_links = len(set([p['value'] for p in conv.extracted_intelligence["phishing_links"]]))

    metrics = {
        "conversation_id": conversation_id,
        "total_turns": conv.total_turns,
        "agent_turns": conv.agent_turns,
        "engagement_duration_seconds": int((datetime.utcnow() - conv.started_at).total_seconds()),
        "scam_detected": conv.scam_detected,
        "scam_confidence": conv.scam_confidence,
        "agent_engaged": conv.agent_engaged,
        "unique_intelligence": {
            "bank_accounts": unique_bank_accounts,
            "upi_ids": unique_upi_ids,
            "phishing_links": unique_phishing_links
        }
    }

    return metrics'''

from datetime import datetime
from app.state import sessions


def evaluate_session(session_id):
    if session_id not in sessions:
        return {"error": "Session not found"}

    s = sessions[session_id]

    metrics = {
        "sessionId": session_id,
        "scamDetected": s["scamDetected"],
        "confidence": s["confidence"],
        "totalMessages": s["totalMessages"],
        "engagementDepth": len(s["messages"]),
        "uniqueIntelligenceCount": {
            "bankAccounts": len(set(s["intelligence"]["bankAccounts"])),
            "upiIds": len(set(s["intelligence"]["upiIds"])),
            "phishingLinks": len(set(s["intelligence"]["phishingLinks"])),
            "phoneNumbers": len(set(s["intelligence"]["phoneNumbers"]))
        },
        "engagementDurationSeconds": int((datetime.utcnow() - s["startedAt"]).total_seconds()),
        "agentEffectivenessScore": compute_agent_score(s)
    }

    return metrics


def compute_agent_score(session):
    score = 0

    score += min(session["totalMessages"] / 10, 1.0) * 0.4
    score += min(len(session["intelligence"]["upiIds"]) * 0.2, 0.3)
    score += min(len(session["intelligence"]["phishingLinks"]) * 0.2, 0.3)

    return round(min(score, 1.0), 2)

