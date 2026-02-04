from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse

from app.schemas import IncomingRequest, APIResponse
from app.state import get_session, update_session, session_store
from app.detector import detect_scam
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence
from app.callback import send_final_callback
from app.config import API_KEY
from app.evaluation import evaluate_session


# ✅ CREATE APP FIRST
app = FastAPI(title="GUVI Agentic Honey-Pot")


# ---------------- HOME PAGE ----------------
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



# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    total_sessions = len(session_store)
    scam_sessions = sum(1 for s in session_store.values() if s["scamDetected"])
    total_messages = sum(len(s["messages"]) for s in session_store.values())

    return f"""
    <html>
    <body style="font-family:Arial;background:#020617;color:white;padding:30px;">
        <h1>📡 GUVI Honeypot Dashboard</h1>
        <p>Total Sessions: {total_sessions}</p>
        <p>Scam Sessions: {scam_sessions}</p>
        <p>Total Messages: {total_messages}</p>
        <p><a style="color:#22c55e" href="/sessions">View Sessions</a></p>
        <p><a style="color:#38bdf8" href="/docs">Docs</a></p>
    </body>
    </html>
    """


# ---------------- SESSION VIEWER ----------------
@app.get("/sessions", response_class=HTMLResponse)
def view_sessions():
    html = "<html><body style='background:#020617;color:white;padding:30px;'>"
    html += "<h1>🕵️ Honeypot Session Viewer</h1>"

    for session_id, session in session_store.items():
        html += f"<hr><h3>Session: {session_id}</h3>"
        html += f"<p>Scam Detected: {session['scamDetected']}</p>"

        for msg in session["messages"]:
            sender = msg.get("sender")
            text = msg.get("text")
            color = "#22c55e" if sender == "user" else "#ef4444"
            html += f"<p style='color:{color}'><b>{sender}:</b> {text}</p>"

    html += "</body></html>"
    return html


# ---------------- INTELLIGENCE PANEL ----------------
@app.get("/intelligence", response_class=HTMLResponse)
def intelligence_panel():
    html = "<html><body style='background:#020617;color:white;padding:30px;'>"
    html += "<h1>💰 Extracted Scam Intelligence</h1>"

    for session_id, session in session_store.items():
        intel = session["intelligence"]
        html += f"<hr><h3>Session {session_id}</h3>"
        html += f"<p>Bank Accounts: {intel.get('bankAccounts')}</p>"
        html += f"<p>UPI IDs: {intel.get('upiIds')}</p>"
        html += f"<p>Phishing Links: {intel.get('phishingLinks')}</p>"
        html += f"<p>Phone Numbers: {intel.get('phoneNumbers')}</p>"
        html += f"<p>Keywords: {intel.get('suspiciousKeywords')}</p>"

    html += "</body></html>"
    return html


# ---------------- ANALYTICS ----------------
@app.get("/analytics")
def analytics():
    keywords = {}

    for session in session_store.values():
        for k in session["intelligence"].get("suspiciousKeywords", []):
            keywords[k] = keywords.get(k, 0) + 1

    return {
        "total_sessions": len(session_store),
        "scam_sessions": sum(s["scamDetected"] for s in session_store.values()),
        "top_scam_keywords": keywords
    }


# ---------------- API KEY AUTH ----------------
def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "live", "service": "GUVI Agentic Honey-Pot"}


# ---------------- EVALUATION ----------------
@app.get("/evaluate/{session_id}")
def get_evaluation(session_id: str, _: None = Depends(verify_key)):
    return evaluate_session(session_id)


# ---------------- MAIN MESSAGE API ----------------
@app.post("/message", response_model=APIResponse)
async def handle_message(payload: IncomingRequest, _: None = Depends(verify_key)):

    session = get_session(payload.sessionId)

    # Store incoming message
    session["messages"].append(payload.message.dict())
    session["totalMessages"] += 1

    # Scam detection (once)
    if not session["scamDetected"]:
        scam, confidence, keywords = detect_scam(payload.message.text)

        session["scamDetected"] = scam
        session["confidence"] = confidence
        session["intelligence"]["suspiciousKeywords"].extend(keywords)

    # Extract intelligence
    extracted = extract_intelligence(payload.message.text)
    update_session(session, extracted)

    agent_reply = None

    # Agent responds if scam detected
    if session["scamDetected"]:
        agent_reply = generate_agent_reply(session)
        session["messages"].append({
            "sender": "user",
            "text": agent_reply
        })
        session["totalMessages"] += 1

    # GUVI Final Callback Trigger
    if (
        session["scamDetected"]
        and session["totalMessages"] >= 6
        and not session["callbackSent"]
    ):
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
