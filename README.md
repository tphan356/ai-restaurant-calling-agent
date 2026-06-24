# AI Restaurant Calling Agent

This is a personal NLP/AI agent project that simulates a restaurant phone assistant. The goal is to classify customer requests into restaurant-related intents and generate appropriate responses in a multi-turn conversation.

## Project Goal

The system will classify customer messages into intents such as:

- greeting
- order
- reservation
- query
- cancel
- complaint
- mixed request

The first version will use a traditional NLP pipeline with TF-IDF and Logistic Regression. Later versions will add confidence-based fallback logic, a Streamlit demo, and a FastAPI/Twilio-ready voice-agent design.

## Planned Features

- Text preprocessing for customer messages
- Intent classification model
- Model evaluation with accuracy, macro F1, and confusion matrix
- Confidence threshold for uncertain predictions
- Streamlit chat demo
- FastAPI endpoint for future voice integration
- Twilio-ready architecture for speech-to-text and text-to-speech workflows

## Tech Stack

Python, Pandas, Scikit-learn, Streamlit, FastAPI, Twilio

## Status

Fresh-start project. I am building this project step by step from the ground up.

## Data Source

The initial restaurant intent dataset comes from the Kaggle dataset **AI Restaurant Calling Agent** by `shanza30

Dataset: https://www.kaggle.com/datasets/shanza30/ai-caller-agent

I use this dataset as a learning/reference dataset and build my own preprocessing, modeling, evaluation, and deployment workflow.
