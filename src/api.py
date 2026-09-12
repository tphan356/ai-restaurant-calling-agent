import json
import pickle
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from src.agent_logic import create_empty_state, update_conversation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "restaurant_intent_model.pkl"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"


app = FastAPI(title="AI Restaurant Calling Agent API")


class ChatRequest(BaseModel):
    message: str
    conversation_state: dict | None = None


def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    return model, metadata


model, metadata = load_model()


def rule_based_intent(text):
    text_lower = text.lower()

    if any(word in text_lower for word in ["reservation", "reserve", "book a table", "booking"]):
        return "reservation"

    if any(word in text_lower for word in ["order", "takeout", "burger", "pizza", "food", "drink"]):
        return "order"

    if "cancel" in text_lower:
        return "cancel"

    if any(word in text_lower for word in ["complaint", "complain", "cold", "wrong", "rude", "refund"]):
        return "complaint"

    if any(word in text_lower for word in ["hours", "close", "open", "menu", "location", "address"]):
        return "query"

    return None


def predict_intent(text, conversation_state):
    prediction = model.predict([text])[0]
    confidence = model.predict_proba([text]).max()

    threshold = metadata.get("confidence_threshold", 0.60)
    responses = metadata.get("responses", {})

    active_intent = conversation_state.get("active_intent")
    rule_intent = rule_based_intent(text)

    if active_intent is not None:
        intent = active_intent
    elif confidence < threshold and rule_intent is not None:
        intent = rule_intent
    elif confidence < threshold:
        intent = "clarify"
    else:
        intent = prediction

    response = responses.get(
        intent,
        "I'm not fully sure I understood. Are you asking about an order, reservation, restaurant information, cancellation, or complaint?"
    )

    return {
        "intent": intent,
        "confidence": float(confidence),
        "response": response
    }


@app.get("/")
def home():
    return {"message": "AI Restaurant Calling Agent API is running."}


@app.post("/chat")
def chat(request: ChatRequest):
    state = request.conversation_state or create_empty_state()

    model_result = predict_intent(request.message, state)

    new_state, agent_response = update_conversation(
        request.message,
        model_result,
        state
    )

    return {
        "customer_message": request.message,
        "intent": model_result["intent"],
        "confidence": model_result["confidence"],
        "agent_response": agent_response,
        "conversation_state": new_state
    }