import re

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

    return results
