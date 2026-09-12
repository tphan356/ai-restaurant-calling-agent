# import json
# import pickle
# from pathlib import Path

# import streamlit as st

# from agent_logic import create_empty_state, update_conversation


# # -----------------------------
# # File paths
# # -----------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# MODEL_PATH = PROJECT_ROOT / "models" / "restaurant_intent_model.pkl"
# METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"


# # -----------------------------
# # Load model and metadata
# # -----------------------------
# @st.cache_resource
# def load_model():
#     with open(MODEL_PATH, "rb") as f:
#         model = pickle.load(f)

#     with open(METADATA_PATH, "r") as f:
#         metadata = json.load(f)

#     return model, metadata


# # -----------------------------
# # Rule-based guardrail
# # -----------------------------
# def rule_based_intent(text):
#     text_lower = text.lower()

#     reservation_keywords = [
#         "reservation",
#         "reserve",
#         "book a table",
#         "book table",
#         "table for",
#         "make a booking",
#         "booking",
#     ]

#     order_keywords = [
#         "order",
#         "takeout",
#         "take out",
#         "to go",
#         "burger",
#         "pizza",
#         "food",
#         "drink",
#     ]

#     cancel_keywords = [
#         "cancel",
#         "cancellation",
#         "remove my booking",
#         "change my booking",
#     ]

#     complaint_keywords = [
#         "complaint",
#         "complain",
#         "cold",
#         "wrong",
#         "bad service",
#         "rude",
#         "late",
#         "refund",
#     ]

#     query_keywords = [
#         "hours",
#         "close",
#         "open",
#         "menu",
#         "location",
#         "address",
#         "parking",
#         "delivery",
#     ]

#     if any(keyword in text_lower for keyword in reservation_keywords):
#         return "reservation"

#     if any(keyword in text_lower for keyword in order_keywords):
#         return "order"

#     if any(keyword in text_lower for keyword in cancel_keywords):
#         return "cancel"

#     if any(keyword in text_lower for keyword in complaint_keywords):
#         return "complaint"

#     if any(keyword in text_lower for keyword in query_keywords):
#         return "query"

#     return None


# # -----------------------------
# # Model prediction
# # -----------------------------
# def predict_intent(text, model, metadata, conversation_state):
#     prediction = model.predict([text])[0]
#     confidence = model.predict_proba([text]).max()

#     threshold = metadata.get("confidence_threshold", 0.60)
#     responses = metadata.get("responses", {})

#     rule_intent = rule_based_intent(text)
#     active_intent = conversation_state.get("active_intent")

#     # If we are already collecting details for an intent,
#     # keep the conversation in that flow instead of clarifying.
#     if active_intent is not None:
#         return {
#             "intent": active_intent,
#             "confidence": confidence,
#             "response": responses.get(active_intent, "How can I help you today?"),
#         }

#     # If model confidence is low but the text has clear keywords,
#     # use the rule-based intent instead of forcing clarify.
#     if confidence < threshold and rule_intent is not None:
#         return {
#             "intent": rule_intent,
#             "confidence": confidence,
#             "response": responses.get(rule_intent, "How can I help you today?"),
#         }

#     # If confidence is low and no rule helps, ask the customer to clarify.
#     if confidence < threshold:
#         return {
#             "intent": "clarify",
#             "confidence": confidence,
#             "response": (
#                 "I'm not fully sure I understood. Are you asking about an order, "
#                 "reservation, restaurant information, cancellation, or complaint?"
#             ),
#         }

#     return {
#         "intent": prediction,
#         "confidence": confidence,
#         "response": responses.get(prediction, "How can I help you today?"),
#     }


# # -----------------------------
# # Streamlit page setup
# # -----------------------------
# st.set_page_config(
#     page_title="AI Restaurant Calling Agent",
#     page_icon="🍽️",
#     layout="centered",
# )

# st.title("🍽️ AI Restaurant Calling Agent")
# st.caption("Multi-turn restaurant phone-call simulation using NLP intent classification")


# # -----------------------------
# # Initialize app
# # -----------------------------
# model, metadata = load_model()

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {
#             "role": "assistant",
#             "content": "Thanks for calling our restaurant. How can I help you today?",
#             "intent": None,
#             "confidence": None,
#         }
#     ]

# if "conversation_state" not in st.session_state:
#     st.session_state.conversation_state = create_empty_state()


# # -----------------------------
# # Sidebar
# # -----------------------------
# with st.sidebar:
#     st.header("Project Info")
#     st.write("**Model:** TF-IDF + Logistic Regression")
#     st.write("**Task:** Restaurant intent classification")
#     st.write(f"**Confidence threshold:** {metadata.get('confidence_threshold', 0.60):.0%}")

#     st.subheader("Supported Intents")
#     for intent in metadata.get("intents", []):
#         st.write(f"- {intent}")

#     st.subheader("Conversation State")
#     st.json(st.session_state.conversation_state)

#     st.subheader("Try a reservation flow")
#     st.code("I want to make a reservation")
#     st.code("For two people")
#     st.code("Tomorrow")
#     st.code("At 7 pm")

#     st.subheader("Other examples")
#     st.code("I want to order two burgers")
#     st.code("What time do you close?")
#     st.code("I want to cancel my reservation")
#     st.code("The food was cold")

#     if st.button("Reset Conversation"):
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "Thanks for calling our restaurant. How can I help you today?",
#                 "intent": None,
#                 "confidence": None,
#             }
#         ]
#         st.session_state.conversation_state = create_empty_state()
#         st.rerun()


# # -----------------------------
# # Display conversation
# # -----------------------------
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

#         if message["intent"] is not None:
#             st.caption(
#                 f"Detected intent: **{message['intent']}** | "
#                 f"Confidence: **{message['confidence']:.2%}**"
#             )


# # -----------------------------
# # User input
# # -----------------------------
# user_input = st.chat_input("Type what the customer says...")

# if user_input:
#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": user_input,
#             "intent": None,
#             "confidence": None,
#         }
#     )

#     model_result = predict_intent(
#         user_input,
#         model,
#         metadata,
#         st.session_state.conversation_state,
#     )

#     st.session_state.conversation_state, agent_response = update_conversation(
#         user_input,
#         model_result,
#         st.session_state.conversation_state,
#     )

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": agent_response,
#             "intent": model_result["intent"],
#             "confidence": model_result["confidence"],
#         }
#     )

#     st.rerun()
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


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


def send_message_to_api(message, conversation_state):
    payload = {
        "message": message,
        "conversation_state": conversation_state,
    }

    response = requests.post(API_URL, json=payload, timeout=10)
    response.raise_for_status()

    return response.json()


st.set_page_config(
    page_title="AI Restaurant Calling Agent",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️ AI Restaurant Calling Agent")
st.caption("Streamlit UI connected to FastAPI backend")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Thanks for calling our restaurant. How can I help you today?",
            "intent": None,
            "confidence": None,
        }
    ]

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = create_empty_state()


with st.sidebar:
    st.header("Project Architecture")
    st.write("**Frontend:** Streamlit")
    st.write("**Backend:** FastAPI")
    st.write("**Model:** TF-IDF + Logistic Regression")
    st.write("**API URL:**")
    st.code(API_URL)

    st.subheader("Conversation State")
    st.json(st.session_state.conversation_state)

    st.subheader("Try Reservation Flow")
    st.code("I want to make a reservation")
    st.code("For two people")
    st.code("Tomorrow")
    st.code("At 7 pm")

    st.subheader("Try Order Flow")
    st.code("I want to order")
    st.code("Two burgers and one coke")

    if st.button("Reset Conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Thanks for calling our restaurant. How can I help you today?",
                "intent": None,
                "confidence": None,
            }
        ]
        st.session_state.conversation_state = create_empty_state()
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["intent"] is not None:
            st.caption(
                f"Detected intent: **{message['intent']}** | "
                f"Confidence: **{message['confidence']:.2%}**"
            )


user_input = st.chat_input("Type what the customer says...")

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "intent": None,
            "confidence": None,
        }
    )

    try:
        api_result = send_message_to_api(
            user_input,
            st.session_state.conversation_state,
        )

        st.session_state.conversation_state = api_result["conversation_state"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": api_result["agent_response"],
                "intent": api_result["intent"],
                "confidence": api_result["confidence"],
            }
        )

    except requests.exceptions.ConnectionError:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "Backend API is not running. Please start FastAPI with: "
                    "`uvicorn src.api:app --reload`"
                ),
                "intent": None,
                "confidence": None,
            }
        )

    except requests.exceptions.RequestException as error:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"API error: {error}",
                "intent": None,
                "confidence": None,
            }
        )

    st.rerun()