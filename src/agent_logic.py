import re


NUMBER_WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}

# Default empty state
def create_empty_state():
    return {
        "active_intent": None,
        "slots": {
            "party_size": None,
            "date": None,
            "time": None,
            "order_items": None,
            "cancel_type": None,
            "complaint_detail": None,
        },
    }

# Party size
def extract_party_size(text):
    text_lower = text.lower()

    # Common patterns
    patterns = [
        r"table for (\d+)", # "table for 4" -> 4
        r"for (\d+) people", # "reservation for 6 people" -> 6
        r"for (\d+)", # "book for 3" -> 3
        r"party of (\d+)", # "party of 8" → 8
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1)

    for word, number in NUMBER_WORDS.items():
        if f"for {word}" in text_lower or f"party of {word}" in text_lower:
            return number

    return None

# date
def extract_date(text):
    text_lower = text.lower()

    if "tonight" in text_lower:
        return "tonight"
    if "today" in text_lower:
        return "today"
    if "tomorrow" in text_lower:
        return "tomorrow"
    if "weekend" in text_lower:
        return "this weekend"

    return None


def extract_time(text):
    text_lower = text.lower()

    match = re.search(r"\b(\d{1,2})(:\d{2})?\s?(am|pm)\b", text_lower)
    if match:
        return match.group(0)

    match = re.search(r"\bat\s+(\d{1,2})(:\d{2})?\b", text_lower)
    if match:
        return match.group(1)

    return None


def extract_order_items(text):
    text_lower = text.lower()

    order_keywords = ["order", "get", "want", "have"]
    if any(word in text_lower for word in order_keywords):
        return text

    return None


def handle_reservation(text, state):
    slots = state["slots"]

    party_size = extract_party_size(text)
    date = extract_date(text)
    time = extract_time(text)

    if party_size:
        slots["party_size"] = party_size
    if date:
        slots["date"] = date
    if time:
        slots["time"] = time

    missing = []

    if not slots["party_size"]:
        missing.append("party size")
    if not slots["date"]:
        missing.append("date")
    if not slots["time"]:
        missing.append("time")

    if missing:
        state["active_intent"] = "reservation"
        return (
            state,
            "Sure, I can help with your reservation. "
            f"Could you tell me the {', '.join(missing)}?"
        )

    response = (
        f"Great. I have your reservation for {slots['party_size']} people "
        f"{slots['date']} at {slots['time']}."
    )

    state["active_intent"] = None
    return state, response


def handle_order(text, state):
    slots = state["slots"]

    order_items = extract_order_items(text)

    if order_items:
        slots["order_items"] = order_items
        state["active_intent"] = None
        return state, "Got it. I can help place that order. Would you like anything else?"

    state["active_intent"] = "order"
    return state, "Sure, what would you like to order?"


def handle_cancel(text, state):
    state["active_intent"] = "cancel"
    return state, "I can help cancel that. Is this for an order or a reservation?"


def handle_complaint(text, state):
    state["slots"]["complaint_detail"] = text
    state["active_intent"] = None
    return state, "I'm sorry about that. I will pass this complaint to the restaurant manager."


def handle_query(text, state):
    state["active_intent"] = None
    return state, "Of course. What would you like to know about the restaurant?"


def handle_greeting(text, state):
    state["active_intent"] = None
    return state, "Hi, thanks for calling. How can I help you today?"


def update_conversation(text, model_result, state):
    intent = model_result["intent"]

    if intent == "clarify":
        return state, model_result["response"]

    active_intent = state.get("active_intent")

    if active_intent == "reservation":
        return handle_reservation(text, state)

    if active_intent == "order":
        return handle_order(text, state)

    if intent == "reservation":
        return handle_reservation(text, state)

    if intent == "order":
        return handle_order(text, state)

    if intent == "cancel":
        return handle_cancel(text, state)

    if intent == "complaint":
        return handle_complaint(text, state)

    if intent == "query":
        return handle_query(text, state)

    if intent == "greeting":
        return handle_greeting(text, state)

    return state, model_result["response"]
