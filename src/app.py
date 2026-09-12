import json
import pickle
from pathlib import Path

import streamlit as st

from agent_logic import create_empty_state, update_conversation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "restaurant_intent_model.pkl"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"


@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    return model, metadata


def predict_intent(text, model, metadata):
    prediction = model.predict([text])[0]
    confidence = model.predict_proba([text]).max()

    threshold = metadata["confidence_threshold"]
    responses = metadata["responses"]

    if confidence < threshold:
        return {
            "intent": "clarify",
            "confidence": confidence,
            "response": (
                "I'm not fully sure I understood. Are you asking about an order, "
                "reservation, restaurant information, cancellation, or complaint?"
            ),
        }

    return {
        "intent": prediction,
        "confidence": confidence,
        "response": responses.get(prediction, "How can I help you today?"),
    }


st.set_page_config(
    page_title="AI Restaurant Calling Agent",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️ AI Restaurant Calling Agent")
st.caption("Multi-turn restaurant phone-call simulation using NLP intent classification")

model, metadata = load_model()

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
    st.header("Project Info")
    st.write("**Model:** TF-IDF + Logistic Regression")
    st.write("**Task:** Restaurant intent classification")
    st.write(f"**Confidence threshold:** {metadata['confidence_threshold']:.0%}")

    st.subheader("Conversation State")
    st.json(st.session_state.conversation_state)

    st.subheader("Try a reservation flow")
    st.code("I want to make a reservation")
    st.code("For two people")
    st.code("Tomorrow")
    st.code("At 7 pm")

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

    model_result = predict_intent(user_input, model, metadata)

    st.session_state.conversation_state, agent_response = update_conversation(
        user_input,
        model_result,
        st.session_state.conversation_state,
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": agent_response,
            "intent": model_result["intent"],
            "confidence": model_result["confidence"],
        }
    )

    st.rerun()
