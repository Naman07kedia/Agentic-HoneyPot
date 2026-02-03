'''import random

AGENT_PERSONA = """
You are a normal, slightly confused person.
You are NOT tech savvy.
You believe the sender is legitimate.
You want to resolve the issue.
Never accuse or question legitimacy.
Ask for details one at a time.
Be polite and human.
"""

FOLLOW_UP_QUESTIONS = [
    "Okay, I understand. What should I do next?",
    "Can you please tell me where I need to make the payment?",
    "The app is asking for payment details. What should I enter?",
    "Can you resend the details? I want to be sure.",
    "Is there a specific account or UPI I should use?",
    "I’m a bit confused, can you guide me step by step?"
]


def generate_agent_response(conversation) -> str:
    """
    Very simple agent logic for now.
    Later we can replace this with an LLM.
    """

    # If agent already asked something recently, vary it
    return random.choice(FOLLOW_UP_QUESTIONS)'''

from app.state import ConversationState
from app.extractor import extract_intelligence
from app.state import add_intelligence
import openai
import os

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.6  # Human-like variability

def format_history(messages):
    """
    Converts conversation messages to a formatted string for LLM context
    """
    formatted = ""
    for msg in messages:
        formatted += f"{msg['sender']}: {msg['message']}\n"
    return formatted

def generate_agent_response(conversation: ConversationState) -> str:
    """
    Generate a human-like agent response using LLM and update extracted intelligence.
    """
    history_str = format_history(conversation.messages)

    # Optimized prompt for maximum engagement + intelligence extraction
    prompt = f"""
You are a human-like agent engaging with a scammer. Your goal is to:
- Keep the conversation believable and natural.
- Subtly obtain UPI IDs, bank accounts, and phishing URLs without revealing scam detection.
- Avoid repeating any information already obtained.
- Be adaptive, polite, and strategically guide the scammer to provide missing details.
- Reference prior messages naturally to appear human.
- Avoid exposing that this is a simulation or you know about scams.

Conversation history:
{history_str}

Write your next reply as if you are continuing the conversation naturally, trying to extract any missing scam intelligence if possible.
"""

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=120
        )

        agent_reply = response.choices[0].message.content.strip()

        # Extract intelligence from the agent reply too
        extracted = extract_intelligence(agent_reply, conversation.total_turns)
        add_intelligence(conversation, extracted)

        return agent_reply

    except Exception as e:
        print("LLM agent error:", e)
        return "I'm sorry, could you clarify that?"
