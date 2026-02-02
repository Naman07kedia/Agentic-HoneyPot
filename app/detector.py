import re

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

    return confidence >= 0.5, confidence
