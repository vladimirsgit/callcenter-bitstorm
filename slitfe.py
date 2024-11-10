import streamlit as st
from datetime import datetime
import requests

# Sample Data for Conversation History
conversations = [
    {
        "summary": "Discussed loan options and interest rates.",
        "avg_sentiment": "Positive",
        "ai_suggestions": "Explore lower interest rates",
        "created_at": datetime(2023, 11, 1, 10, 30)
    },
    {
        "summary": "Inquired about account opening procedures.",
        "avg_sentiment": "Neutral",
        "ai_suggestions": "Send welcome guide",
        "created_at": datetime(2023, 10, 28, 15, 45)
    },
]

# Setting Page Configuration
st.set_page_config(page_title="Raiffeisen Call Sights", page_icon="🏦", layout="wide")

# Custom CSS to hide the sidebar
st.markdown(
    """
    <style>
        /* Hide sidebar completely */
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main area header
st.markdown("<h1 style='color: #FFCC00;'>Raiffeisen Call Sights</h1>", unsafe_allow_html=True)

# Fetch conversations
conversations = requests.get('http://localhost:8000/convos').json()

# Display each conversation in an expander in the main area
for idx, conversation in enumerate(conversations):
    with st.expander(f"🟡 {conversation['title']}", expanded=False):
        st.markdown(
            f"""
            <div style='background-color: #FFCC00; color: black; border: 1px solid black; padding: 10px; border-radius: 5px;'>
                <p><strong>Summary:</strong> {conversation['summary']}</p>
                <p><strong>Avg Sentiment:</strong> {conversation['avg_sentiment']}</p>
                <p><strong>AI Suggestions:</strong> {conversation['ai_suggestions']}</p>
                <p><strong>Date:</strong> {conversation['created_at']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
