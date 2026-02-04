'''import re

BANK_ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b")
UPI_REGEX = re.compile(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b")
URL_REGEX = re.compile(r"https?://[^\s]+")


def extract_intelligence(message: str, turn: int) -> dict:
    results = {
        "bank_accounts": [],
        "upi_ids": [],
        "phishing_links": []
    }

    for match in BANK_ACCOUNT_REGEX.findall(message):
        results["bank_accounts"].append({
            "value": match,
            "confidence": 0.9,
            "source_turn": turn
        })

    for match in UPI_REGEX.findall(message):
        results["upi_ids"].append({
            "value": match,
            "confidence": 0.95,
            "source_turn": turn
        })

    for match in URL_REGEX.findall(message):
        results["phishing_links"].append({
            "value": match,
            "confidence": 0.95,
            "source_turn": turn
        })

    return results'''

import re

BANK = re.compile(r"\b(?:\d[\s-]?){9,18}\b")
UPI = re.compile(r"\b[a-z0-9.\-_]{2,}@[a-z]{2,}\b", re.I)
URL = re.compile(r"https?://\S+")
PHONE = re.compile(r"\b(?:\+91|0)?[6-9]\d{9}\b")
KEYWORDS = ["urgent", "verify now", "account blocked", "otp", "refund"]


def extract_intelligence(text):
    return {
        "bankAccounts": BANK.findall(text),
        "upiIds": UPI.findall(text),
        "phishingLinks": URL.findall(text),
        "phoneNumbers": PHONE.findall(text),
        "suspiciousKeywords": [k for k in KEYWORDS if k in text.lower()]
    }

