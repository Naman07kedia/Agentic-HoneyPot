from app.state import conversation_store
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

    return metrics
