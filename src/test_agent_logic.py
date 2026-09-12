from agent_logic import create_empty_state, update_conversation


def fake_model_result(intent):
    return {
        "intent": intent,
        "confidence": 0.95,
        "response": "Default model response."
    }


print("Reservation Flow")
print("=" * 60)

state = create_empty_state()

reservation_conversation = [
    ("I want to make a reservation", "reservation"),
    ("For two people", "reservation"),
    ("Tomorrow", "reservation"),
    ("At 7 pm", "reservation"),
]

for customer_message, intent in reservation_conversation:
    model_result = fake_model_result(intent)

    state, agent_response = update_conversation(
        customer_message,
        model_result,
        state
    )

    print("Customer:", customer_message)
    print("Agent:", agent_response)
    print("State:", state)
    print("-" * 60)


print("\nOrder Flow")
print("=" * 60)

state = create_empty_state()

order_conversation = [
    ("I want to order", "order"),
    ("Two burgers and one coke", "order"),
]

for customer_message, intent in order_conversation:
    model_result = fake_model_result(intent)

    state, agent_response = update_conversation(
        customer_message,
        model_result,
        state
    )

    print("Customer:", customer_message)
    print("Agent:", agent_response)
    print("State:", state)
    print("-" * 60)