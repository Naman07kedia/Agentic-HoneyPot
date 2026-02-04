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
from app.evaluation import evaluate_session

# ✅ CREATE APP FIRST
app = FastAPI(title="GUVI Agentic Honey-Pot")

from fastapi.responses import HTMLResponse
from app.state import session_store

@app.get("/", response_class=HTMLResponse)
def home():
    total_sessions = len(session_store)
    scam_sessions = sum(1 for s in session_store.values() if s["scamDetected"])

    return f"""
    <html>
    <head>
        <title>GUVI Agentic Honey-Pot</title>
        <style>
            body {{
                font-family: Inter, Arial;
                background: linear-gradient(135deg, #020617, #020617);
                color: white;
                padding: 40px;
            }}
            .container {{
                max-width: 900px;
                background: #020617;
                padding: 30px;
                border-radius: 18px;
                box-shadow: 0 0 40px rgba(56,189,248,0.15);
            }}
            h1 {{ color: #38bdf8; }}
            .badge {{
                background: #22c55e;
                color: black;
                padding: 6px 12px;
                border-radius: 8px;
                font-weight: bold;
                display: inline-block;
            }}
            a {{
                color: #38bdf8;
                text-decoration: none;
                font-weight: bold;
            }}
            .stats {{
                margin-top: 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
            }}
            .card {{
                background: #020617;
                padding: 16px;
                border-radius: 12px;
                border: 1px solid #1e293b;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 GUVI Agentic Honey-Pot API</h1>
            <p>AI-powered system that detects scam messages, autonomously engages scammers, extracts financial intelligence, and reports results to GUVI.</p>

            <span class="badge">LIVE • Hackathon Ready</span>

            <div class="stats">
                <div class="card">
                    <b>Total Sessions</b><br>{total_sessions}
                </div>
                <div class="card">
                    <b>Scam Sessions Detected</b><br>{scam_sessions}
                </div>
                <div class="card">
                    <b>Status</b><br>Operational
                </div>
            </div>

            <br>

            <p>📘 API Documentation → <a href="/docs">Open Swagger UI</a></p>
            <p>📡 Health Check → <a href="/health">/health</a></p>
            <p>🧠 Evaluation → <a href="/evaluate/demo-session">/evaluate/{'{session_id}'}</a></p>

            <hr style="border-color:#1e293b">

            <p>🏆 Built for GUVI AI Summit Hackathon</p>
            <p>🔐 Secure API Key Enabled</p>
            <p>🤖 Autonomous Scam Engagement Engine</p>
        </div>
    </body>
    </html>
    """


def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.get("/health")
def health():
    return {"status": "live", "service": "GUVI Agentic Honey-Pot"}


@app.get("/evaluate/{session_id}")
def get_evaluation(session_id: str, _: None = Depends(verify_key)):
    return evaluate_session(session_id)


@app.post("/message", response_model=APIResponse)
async def handle_message(payload: IncomingRequest, _: None = Depends(verify_key)):

    session = get_session(payload.sessionId)

    # Add new message to history
    session["messages"].append(payload.message.dict())
    session["totalMessages"] += 1

    # Detect scam intent
    if not session["scamDetected"]:
        scam, confidence = detect_scam(payload.message.text)
        session["scamDetected"] = scam
        session["confidence"] = confidence

    # Extract intelligence
    extracted = extract_intelligence(payload.message.text)
    update_session(session, extracted)

    agent_reply = None

    # Agent activates if scam detected
    if session["scamDetected"]:
        agent_reply = generate_agent_reply(session)
        session["messages"].append({"sender": "user", "text": agent_reply})
        session["totalMessages"] += 1

    # Send GUVI callback after engagement threshold
    if session["scamDetected"] and session["totalMessages"] >= 6 and not session["callbackSent"]:
        send_final_callback(payload.sessionId, session)
        session["callbackSent"] = True

    return APIResponse(
        status="success",
        scamDetected=session["scamDetected"],
        confidence=session["confidence"],
        reply=agent_reply,
        extractedIntelligence=session["intelligence"],
        totalMessagesExchanged=session["totalMessages"]
    )

