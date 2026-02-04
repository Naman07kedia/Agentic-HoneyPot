'''import re

SCAM_KEYWORDS = [
    "account blocked",
    "account suspended",
    "kyc",
    "urgent",
    "immediately",
    "verify now",
    "click link",
    "otp",
    "upi",
    "bank account",
    "refund",
    "payment failed",
    "lottery",
    "prize won",
]

URL_PATTERN = re.compile(r"https?://\S+")


def detect_scam(message: str) -> tuple[bool, float]:
    """
    Returns:
      (is_scam, confidence)
    """
    message_lower = message.lower()
    score = 0.0

    # keyword hits
    for keyword in SCAM_KEYWORDS:
        if keyword in message_lower:
            score += 0.12

    # url present
    if URL_PATTERN.search(message):
        score += 0.25

    # money symbols
    if any(sym in message for sym in ["₹", "$", "rs", "inr"]):
        score += 0.15

    # cap confidence
    confidence = min(score, 1.0)

    return confidence >= 0.5, confidence'''

import re

KEYWORDS = [
    "otp", "urgent", "blocked", "verify", "payment",
    "refund", "won", "lottery", "kyc", "upi", "account",
    "suspended", "limited time", "act now", "immediately"
]

URL = re.compile(r"https?://")
MONEY = re.compile(r"(₹|rs|inr|\$)")
PAY = re.compile(r"(pay|send|transfer)")
PHONE = re.compile(r"\b\d{10}\b")


def detect_scam(text):
    text = text.lower()
    score = 0.0
    hits = []

    # Keyword scoring
    for k in KEYWORDS:
        if k in text:
            score += 0.12
            hits.append(k)

    # URL detection
    if URL.search(text):
        score += 0.25
        hits.append("url")

    # Money mention
    if MONEY.search(text):
        score += 0.2
        hits.append("money")

    # Payment intent
    if PAY.search(text):
        score += 0.2
        hits.append("payment")

    # Phone number
    if PHONE.search(text):
        score += 0.15
        hits.append("phone")

    # Urgency boost
    if "immediately" in text or "urgent" in text or "now" in text:
        score += 0.15
        hits.append("urgency")

    confidence = min(score, 1.0)

    # LOWER threshold = better recall for hackathon
    is_scam = confidence >= 0.30

    return is_scam, confidence, hits
