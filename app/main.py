'''from app.config import API_KEY
from fastapi import Query
from datetime import datetime
from app.evaluation import summarize_conversation
from fastapi import FastAPI, Header, HTTPException, Depends
from app.schemas import (
    IncomingMessage,
    APIResponse,
    ConversationMetrics,
    ExtractedIntelligence,
)

from app.state import (
    get_conversation,
    update_turn,
    record_message,
    engagement_duration_seconds,
    add_intelligence,
)

from app.detector import detect_scam
from app.agent import generate_agent_response
from app.extractor import extract_intelligence

app = FastAPI(title="Agentic Honey-Pot")


# ---------------- API KEY AUTH ----------------
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
def root():
    return {
        "status": "Agentic Honey-Pot is live",
        "docs": "/docs",
        "message_endpoint": "/message"
    }

# ---------------- REQUIRED ENDPOINT ----------------
@app.post("/message", response_model=APIResponse)
async def receive_message(
    payload: IncomingMessage,
    _: None = Depends(verify_api_key)
):
    conversation = get_conversation(payload.conversation_id)

    # Record incoming scammer message
    record_message(conversation, sender, payload.message)
    update_turn(conversation, sender)

    # Extract intelligence from incoming message
    extracted = extract_intelligence(
        payload.message,
        conversation.total_turns
    )
    add_intelligence(conversation, extracted)

    agent_response = None

    # Scam detection (only once)
    if not conversation.scam_detected:
        is_scam, confidence = detect_scam(payload.message)
        if is_scam:
            conversation.scam_detected = True
            conversation.scam_confidence = confidence
            conversation.agent_engaged = True

    # Agent handoff
    if conversation.scam_detected:
        agent_response = generate_agent_response(conversation)
        record_message(conversation, "agent", agent_response)
        update_turn(conversation, "agent")

    metrics = ConversationMetrics(
        total_turns=conversation.total_turns,
        agent_turns=conversation.agent_turns,
        engagement_duration_seconds=engagement_duration_seconds(conversation)
    )

    return APIResponse(
        scam_detected=conversation.scam_detected,
        confidence=conversation.scam_confidence,
        agent_engaged=conversation.agent_engaged,
        agent_response=agent_response,
        conversation_metrics=metrics,
        extracted_intelligence=ExtractedIntelligence(
            bank_accounts=conversation.extracted_intelligence["bank_accounts"],
            upi_ids=conversation.extracted_intelligence["upi_ids"],
            phishing_links=conversation.extracted_intelligence["phishing_links"],
        )
    )
@app.get("/evaluate/{conversation_id}")
async def evaluate(conversation_id: str, _: None = Depends(verify_api_key)):
    """
    Returns structured evaluation metrics for a given conversation.
    """
    return summarize_conversation(conversation_id)

@app.get("/")
def health():
    return {
        "status": "live",
        "service": "Agentic Honey-Pot",
        "docs": "/docs"
    }
'''
from fastapi import FastAPI, Header, HTTPException, Depends
from app.schemas import IncomingRequest, APIResponse
from app.state import get_session, update_session
from app.detector import detect_scam
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence
from app.callback import send_final_callback
from app.config import API_KEY

app = FastAPI(title="GUVI Agentic Honey-Pot")


def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.get("/health")
def health():
    return {"status": "live", "service": "GUVI Agentic Honey-Pot"}


@app.post("/message", response_model=APIResponse)
async def handle_message(payload: IncomingRequest, _: None = Depends(verify_key)):

    session = get_session(payload.sessionId)

    # Add new message to history
    session["messages"].append(payload.message.dict())

    # Detect scam intent
    if not session["scamDetected"]:
        scam, confidence = detect_scam(payload.message.text)
        session["scamDetected"] = scam
        session["confidence"] = confidence

    # Extract intelligence from scammer message
    extracted = extract_intelligence(payload.message.text)
    update_session(session, extracted)

    agent_reply = None

    # Activate AI Agent if scam detected
    if session["scamDetected"]:
        agent_reply = generate_agent_reply(session)
        session["messages"].append({"sender": "user", "text": agent_reply})

    # Send GUVI callback only once when enough engagement done
    if session["scamDetected"] and session["totalMessages"] >= 6 and not session["callbackSent"]:
        send_final_callback(payload.sessionId, session)
        session["callbackSent"] = True

    return {
        "status": "success",
        "scamDetected": session["scamDetected"],
        "confidence": session["confidence"],
        "reply": agent_reply,
        "extractedIntelligence": session["intelligence"],
        "totalMessagesExchanged": session["totalMessages"]
    }
