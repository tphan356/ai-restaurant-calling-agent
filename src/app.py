import json
import pickle
from pathlib import Path

import streamlit as st


# Project paths
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
            )
        }

    return {
        "intent": prediction,
        "confidence": confidence,
        "response": responses.get(prediction, "How can I help you today?")
    }


st.set_page_config(
    page_title="AI Restaurant Calling Agent",
    page_icon="🍽️",
    layout="centered"
)

st.title("🍽️ AI Restaurant Calling Agent")
st.write(
    "This app simulates a restaurant phone assistant. "
    "Type a customer message and the model will predict the intent."
)

model, metadata = load_model()

st.subheader("Customer Message")

user_input = st.text_area(
    "Enter what the customer says:",
    placeholder="Example: Hi, can I reserve a table for two tonight?"
)

if st.button("Predict Intent"):
    if user_input.strip() == "":
        st.warning("Please enter a customer message.")
    else:
        result = predict_intent(user_input, model, metadata)

        st.subheader("Prediction Result")
        st.write(f"**Intent:** {result['intent']}")
        st.write(f"**Confidence:** {result['confidence']:.2%}")

        st.subheader("Agent Response")
        st.success(result["response"])

st.divider()

st.subheader("Try These Examples")

examples = [
    "Hi, can I order two burgers?",
    "Can I reserve a table for four tonight?",
    "What time do you close?",
    "I want to cancel my reservation.",
    "The food was cold and the service was bad."
]

for example in examples:
    st.code(example)
