'''from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class IncomingMessage(BaseModel):
    conversation_id: str
    message_id: str
    sender: str   # "scammer"
    message: str
    timestamp: datetime

    # optional / flexible fields
    message_id: Optional[str] = None
    sender: Optional[str] = "scammer"
    timestamp: Optional[str] = None
    
class IntelligenceItem(BaseModel):
    value: str
    confidence: float
    source_turn: int


class ExtractedIntelligence(BaseModel):
    bank_accounts: List[IntelligenceItem] = []
    upi_ids: List[IntelligenceItem] = []
    phishing_links: List[IntelligenceItem] = []


class ConversationMetrics(BaseModel):
    total_turns: int
    agent_turns: int
    engagement_duration_seconds: int


class APIResponse(BaseModel):
    scam_detected: bool
    confidence: float
    agent_engaged: bool
    agent_response: Optional[str]
    conversation_metrics: ConversationMetrics
    extracted_intelligence: ExtractedIntelligence'''

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Message(BaseModel):
    sender: str
    text: str
    timestamp: int


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Dict[str, Any]] = {}


class APIResponse(BaseModel):
    status: str
    scamDetected: bool
    confidence: float
    reply: Optional[str] = None
    extractedIntelligence: Dict[str, List[str]] = {}
    totalMessagesExchanged: int


